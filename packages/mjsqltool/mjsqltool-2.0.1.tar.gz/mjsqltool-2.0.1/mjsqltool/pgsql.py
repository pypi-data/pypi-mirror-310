import pandas as pd
from sqlalchemy import inspect, text, MetaData
import sqlalchemy.exc
from sqlalchemy.exc import NoSuchTableError, SQLAlchemyError
from typing import List, Literal, Union

from mjsqltool.package import DataConvert

def wdata_topgsql(conn:sqlalchemy.engine.base.Connection, 
    df:pd.DataFrame, 
    table_name:str, 
    schema:str, 
    if_exists:Literal['fail','replace', 'append']='fail', 
    on_conflict:Literal['ignore', 'update']='ignore', 
    batch_size=1000,
    is_clear_data:bool=True)->int:
    """
    将DataFrame写入PostgreSQL指定的模式和表中，可以处理主键冲突，并返回成功写入的行数。

    参数:
        conn: 数据库连接对象。
        df (pd.DataFrame): 要写入的数据框。
        table_name (str): 数据库中的表名。
        schema (str): 数据库中的模式名。
        if_exists (str): 如果表已存在，行为选项为 {'fail', 'replace', 'append'}。
        on_conflict (str): 主键冲突时的行为，可选值为 {'ignore', 'update'}。
        batch_size (int): 分批写入的数据量，默认为1000。
        is_clear_data: bool: 是否清理数据，默认为True。
    返回:
        int: 成功写入的行数。
    """
    if is_clear_data:
        # 清理数据
        df = DataConvert().convert_to_cleandata(df)
    # 清理列名
    df.columns = df.columns.str.strip().str.replace('\n', '')
    
    for col in df.select_dtypes(include=['datetime64']).columns:
        # 使用指定的格式转换日期时间列到字符串
        df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S')

    # 动态处理无效值
    df = df.where(pd.notna(df), other=None)
    
    # 检查表是否存在
    inspector = inspect(conn.engine)
    if not inspector.has_table(table_name, schema=schema):
        if if_exists == 'fail':
            raise ValueError(f"表 {schema}.{table_name} 不存在，并且if_exists设置为'fail'。")
        elif if_exists == 'replace':
            # 如果表不存在，则创建新表
            try:
                df.to_sql(name=table_name, con=conn.engine, schema=schema, if_exists='replace', index=False)
                print(f"创建表 {schema}.{table_name} 成功。")
                return len(df)
            except SQLAlchemyError as e:
                raise ValueError(f"创建表 {schema}.{table_name} 时出错: {e}")
        elif if_exists == 'append':
            # 如果表不存在，则创建新表
            try:
                df.to_sql(name=table_name, con=conn.engine, schema=schema, if_exists='append', index=False)
                print(f"创建表 {schema}.{table_name} 成功。")
                return len(df)
            except SQLAlchemyError as e:
                raise ValueError(f"创建表 {schema}.{table_name} 时出错: {e}")

    # 获取表的主键列表和列名列表
    meta = MetaData()
    meta.reflect(bind=conn.engine, schema=schema)
    try:
        primary_keys = [c.name for c in meta.tables[f'{schema}.{table_name}'].primary_key.columns]
        table_columns = [c.name for c in meta.tables[f'{schema}.{table_name}'].columns]
    except NoSuchTableError:
        raise ValueError(f"无法找到表 {schema}.{table_name} 的定义。")

    # 检查 DataFrame 的列是否都在数据库表中
    missing_columns = set(df.columns) - set(table_columns)
    if missing_columns:
        raise ValueError(f"以下列不在数据库表 {schema}.{table_name} 中: {missing_columns}")

    # 构建SQL语句
    columns = ', '.join([f'"{col}"' for col in df.columns])
    values = ', '.join([f':{col}' for col in df.columns])

    if primary_keys:
        update_set = ', '.join([f'"{col}" = EXCLUDED."{col}"' for col in df.columns if col not in primary_keys])
        sql = f"""
        INSERT INTO "{schema}"."{table_name}" ({columns})
        VALUES ({values})
        ON CONFLICT ({', '.join([f'"{pk}"' for pk in primary_keys])})
        DO {on_conflict.upper()}
        """
        if on_conflict == 'update':
            sql += f" SET {update_set}"
        elif on_conflict == 'ignore':
            sql = sql.replace('DO IGNORE', 'DO NOTHING')
    else:
        # 表没有主键，直接插入数据
        print(f"表 {schema}.{table_name} 没有主键，直接在末尾插入数据。")
        sql = f"""
        INSERT INTO "{schema}"."{table_name}" ({columns})
        VALUES ({values})
        """

    # 分批写入数据并记录成功写入的行数
    total_rows_written = 0
    total_rows = len(df)
    for start in range(0, total_rows, batch_size):
        end = min(start + batch_size, total_rows)
        batch_df = df.iloc[start:end]
        with conn.engine.begin() as trans:
            try:
                for _, row in batch_df.iterrows():
                    params = row.to_dict()
                    result = trans.execute(text(sql), params)
                    if result.rowcount > 0:
                        total_rows_written += 1
            except SQLAlchemyError as e:
                print(f"执行SQL语句时出错: {e}")

    return total_rows_written






