#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import json
import time
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from pandas.core.series import Series
from pdcool.database import DBUtil


def generate_simple_dataframe():
    """生成一个dataframe"""
    simple_dictlist = [
        {"name": "alice", "age": 18, "gender": "female"},
        {"name": "bob", "age": 8, "gender": "male"},
        {"name": "jack", "age": 13, "gender": "male"},
    ]
    return pd.DataFrame(simple_dictlist)


def dataframe_from_dictlist(dictlist):
    """获取dataframe(读取dictlist)"""
    return pd.DataFrame(dictlist)


def dataframe_to_dictlist(df):
    """保存dataframe(写入dictlist)"""
    json_text = df.to_json(orient="records")
    json_data = json.loads(json_text)
    return json_data


def dataframe_from_listdict(listdict, dict_type="columns", column_name=None):
    """获取dataframe(读取listdict)"""
    if dict_type not in ("columns", "index"):
        raise ValueError(f"invalid dict_type: {dict_type}")

    if dict_type in ("columns"):
        df = pd.DataFrame.from_dict(
            listdict, orient=dict_type
        )  # 如果dict_type="columns", 则不使用column_name
        return df

    if dict_type in ("index"):
        df = pd.DataFrame.from_dict(listdict, orient=dict_type)
        df.reset_index(level=0, inplace=True)
        if column_name:
            df = dataframe_rename(df, column_name)
        return df


def dataframe_from_csv(path, column_name=None, column_type=None, encoding="utf-8"):
    """获取dataframe(读取csv文件)"""
    if not isinstance(path, str) and not isinstance(path, list):
        raise ValueError(f"invalid path: {path}")

    if isinstance(path, str):
        if not column_name:
            return pd.read_csv(path, dtype=column_type, encoding=encoding)
        else:
            return pd.read_csv(
                path,
                names=column_name,
                dtype=column_type,
                encoding=encoding,
                skiprows=1,
            )

    if isinstance(path, list):
        df_list = []
        for item in path:
            item_df = dataframe_from_csv(
                item,
                column_name=column_name,
                column_type=column_type,
                encoding=encoding,
            )
            df_list.append(item_df)
        df = pd.concat(df_list)
        return df


def dataframe_to_csv(df, path):
    """保存dataframe(写入csv文件)"""
    df.to_csv(path, index=False)


def dataframe_from_excel(path, sheet=0, column_name=None, column_type=None):
    """获取dataframe(读取excel文件)"""
    return pd.read_excel(path, sheet_name=sheet, names=column_name, dtype=column_type)


def dataframe_to_excel(df, path):
    """保存dataframe(写入excel文件)"""
    df.to_excel(path, index=False)


def dataframe_from_sql(sql):
    """获取dataframe(读取sql)"""
    username = os.getenv("MYSQL_USERNAME")
    password = os.getenv("MYSQL_PASSWORD")
    host = os.getenv("MYSQL_HOST")
    port = os.getenv("MYSQL_PORT")
    database = os.getenv("MYSQL_DATABASE")
    database_url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
    df = pd.read_sql(sql, database_url)
    return df


def dataframe_to_table(dataframe, table, primary_key=[], delete_key=[], mode="append"):
    """保存dataframe(写入数据库table)
    mode:
        - append        : 插入
        - delete_append : 根据主键删除, 再插入
        - merge         : 根据主键合并, 以新值为准
        - merge_vaild   : 根据主键合并, 以新值为准, 如果新值为空则保留老值
    """
    if mode not in ("append", "delete_append", "merge", "merge_valid"):
        raise ValueError(f"invalid mode: {mode}")

    username = os.getenv("MYSQL_USERNAME")
    password = os.getenv("MYSQL_PASSWORD")
    host = os.getenv("MYSQL_HOST")
    port = os.getenv("MYSQL_PORT")
    database = os.getenv("MYSQL_DATABASE")
    database_url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"

    if mode in ("append"):
        engine = create_engine(database_url)
        dataframe.to_sql(table, engine, if_exists="append", index=False)

    elif mode in ("delete_append"):
        deletekey_df = dataframe[delete_key]
        deletekey_df = deletekey_df.drop_duplicates()
        db = DBUtil()
        for idx, item in deletekey_df.iterrows():
            delete_condition = " and ".join(map(lambda x, y: f"{x} = '{y}'", delete_key, list(item)))
            sql = f"delete from {table} where {delete_condition}"
            print(sql)
            db.execute(sql)

        engine = create_engine(database_url)
        dataframe.to_sql(table, engine, if_exists="append", index=False)

    elif mode in ("merge"):
        timestamp = int(time.time())
        temptable = f"{table}_{timestamp}"
        engine = create_engine(database_url)
        dataframe.to_sql(temptable, engine, if_exists="replace", index=False)

        db = DBUtil()
        columns = list(dataframe)
        insert_content = ", ".join(columns)
        select_content = ", ".join(columns)
        update_columns = [x for x in columns if x not in primary_key and x != "create_time"]
        update_content = ", ".join(map(lambda x: f"{x} = values({x})", update_columns))
        sql = f"insert into {table}({insert_content}) select {select_content} from {temptable} on duplicate key update {update_content}"
        db.execute(sql)
        db.execute(f"drop table {temptable}")

    else:
        timestamp = int(time.time())
        temptable = f"{table}_{timestamp}"
        engine = create_engine(database_url)
        dataframe.to_sql(temptable, engine, if_exists="replace", index=False)

        db = DBUtil()
        columns = list(dataframe)
        insert_content = ", ".join(columns)
        select_content = ", ".join(columns)
        update_columns = [x for x in columns if x not in primary_key and x != "create_time"]
        update_content = ", ".join(map(lambda x: f"t.{x} = ifnull(s.{x},t.{x})", update_columns))
        update_condition = " and ".join(map(lambda x: f"t.{x} = s.{x}", primary_key))
        update_sql = f"update {table} t, {temptable} s set {update_content} where {update_condition}"
        db.execute(update_sql)
        insert_sql = f"insert ignore into {table}({insert_content}) select {select_content} from {temptable}"
        print(insert_sql)
        db.execute(insert_sql)
        db.execute(f"drop table {temptable}")


def show_dataframe(df, show_type="normal"):
    """显示dataframe"""
    if show_type not in ("normal", "dictlist"):
        raise ValueError(f"invalid show_type: {show_type}")

    if show_type == "normal":
        pd.set_option("display.unicode.east_asian_width", True)  # 设置命令行输出右对齐
        print(df)
        return

    if show_type == "dictlist":
        distlist = dataframe_to_dictlist(df)
        for item in distlist:
            print(item)
        return


def dataframe_rename(df, column):
    """dataframe重命名列名"""
    if not isinstance(column, list) and not isinstance(column, dict):
        raise ValueError(f"invalid column: {column}")

    if isinstance(column, list):
        return df.set_axis(column, axis="columns")

    if isinstance(column, dict):
        return df.rename(columns=column)


def dataframe_empty_none(df):
    """dataframe清空空字符串"""
    df = df.replace("", np.nan)  # 替换空字符串
    df = df.replace(to_replace=r"^\s*?$", value=np.nan)  # 替换空白符
    df = df.fillna(value=np.nan)  # 替换None值
    return df


def dataframe_fill_none(df, val=""):
    """dataframe填充空值的值"""
    return df.fillna(val)


def dataframe_transform_dict(df, column_name, dict):
    """dataframe翻译字典值"""
    df[column_name].replace(dict, inplace=True)
    return df


def dataframe_union(df_list):
    """dataframe纵向拼接"""
    return pd.concat(df_list)


def dataframe_join(df1, df2):
    """dataframe横向拼接"""
    return pd.merge(df1, df2)


def dataframe_count(df, count_type="row"):
    """dataframe行数/列数/单元格数"""
    if count_type not in ("row", "column", "cell"):
        raise ValueError(f"invaild count_type: {count_type}")

    if count_type == "row":
        return len(df)

    if count_type == "column":
        return len(df.columns)

    if count_type == "cell":
        return df.size


def dataframe_first_value(df):
    """dataframe第一个值"""
    return df.iloc[[0], [0]].values[0][0]


def dataframe_groupby_count(df, column, count_name="count"):
    """dataframe分组计数"""
    if not isinstance(column, str) and not isinstance(column, list):
        raise ValueError(f"invaild column: {column}")

    return df.groupby(column).size().to_frame(count_name).reset_index()


def generate_simple_series():
    """生成一个Series"""
    simple_dict = {"name": "alice", "age": 18, "gender": "female"}
    return pd.Series(simple_dict)


def series_from_dict(d):
    """获取series(读取dict)"""
    return pd.Series(d)


def series_to_dict(s):
    """保存series(写入dict)"""
    return Series.to_dict(s)


def series_to_list(s):
    """保存series(写入list)"""
    return Series.tolist(s)


def series_to_dataframe(s, is_transposition=True):
    """保存series(写入dataframe)"""
    df = pd.DataFrame(s)
    if is_transposition:
        df = df.T  # 转置行列
    return df
