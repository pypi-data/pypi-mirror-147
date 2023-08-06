# -*-coding:utf-8 -*-
import taos
import pandas as pd
import numpy as np
import datetime
from .verify import verify_args
from taos.connection import TDengineConnection

td_columns = {
    "cn_d1":  ["code", "time", "open", "close", "low", "high", "volume", "money",
               "factor", "high_limit", "low_limit", "avg", "pre_close",
               "paused", "update_date"],
    "cn_d1_post":  ["code", "time", "open", "close", "low", "high", "volume", "money",
               "factor", "high_limit", "low_limit", "avg", "pre_close",
               "paused", "update_date"],
    "cn_d1_raw":  ["code", "time", "open", "close", "low", "high", "volume", "money",
               "factor", "high_limit", "low_limit", "avg", "pre_close",
               "paused", "update_date"],
    "cn_m1": ["code", "time", "open", "close", "low", "high", "volume", "money",
              "factor", "high_limit", "low_limit", "avg", "pre_close",
              "paused", "update_date"],
    "cn_m5": ["code", "time", "open", "close", "low", "high", "volume", "money",
              "factor", "high_limit", "low_limit", "avg", "pre_close",
              "paused", "update_date"],
    "cn_m15": ["code", "time", "open", "close", "low", "high", "volume", "money",
               "factor", "high_limit", "low_limit", "avg", "pre_close",
               "paused", "update_date"],
    "cn_m30": ["code", "time", "open", "close", "low", "high", "volume", "money",
               "factor", "high_limit", "low_limit", "avg", "pre_close",
               "paused", "update_date"],
    "cn_m60": ["code", "time", "open", "close", "low", "high", "volume", "money",
               "factor", "high_limit", "low_limit", "avg", "pre_close",
               "paused", "update_date"],
    "cn_tick":  ["code",  "time",  "current",  "high",  "low",  "volume",  "money",
                 "factor", "a1_v", "a2_v", "a3_v", "a4_v", "a5_v", "a1_p", "a2_p",
                 "a3_p", "a4_p", "a5_p",  "b1_v",  "b2_v",  "b3_v",  "b4_v",  "b5_v",
                 "b1_p",  "b2_p",  "b3_p",  "b4_p",  "b5_p"],
    "us_d1": ["code", "time", "open", "high", "low", "close", "pre_close", "avg",
              "volume", "money", "unix_timestamp", "update_date"],
    "us_m1": ["code", "time", "open", "high", "low", "close", "pre_close", "avg",
              "volume", "money", "unix_timestamp", "update_date"],
    "us_m5": ["code", "time", "open", "high", "low", "close", "pre_close", "avg",
              "volume", "money", "unix_timestamp", "update_date"],
    "us_m15": ["code", "time", "open", "high", "low", "close", "pre_close", "avg",
               "volume", "money", "unix_timestamp", "update_date"],
    "us_m30": ["code", "time", "open", "high", "low", "close", "pre_close", "avg",
               "volume", "money", "unix_timestamp", "update_date"],
    "us_m60": ["code", "time", "open", "high", "low", "close", "pre_close", "avg",
               "volume", "money", "unix_timestamp", "update_date"]
}

taos_conn = None

def auth(host, port, user, password):
    global taos_conn
    taos_conn = taos.connect(
        **dict(host=host, port=port, user=user, password=password))
    return taos_conn

def format_date_param(t):
    if isinstance(t, datetime.date) or isinstance(t, str):
        return f"{str(t)} 00:00:00"
    else:
        return t

def get_int_code(code, region):
    if region == 'cn':
        if 'XSHG' in code:
            code_int = int(code.strip('.XSHG')) + 1000000
        else:
            code_int = int(code.strip('.XSHE')) + 2000000
    elif region == 'us':
        code_int = int(code)
    else:
        code_int = int(code)
    return code_int

@verify_args(check={'code': (str, list),
                    'region': str,
                    'frequency': str,
                    'start_date': (datetime.datetime, datetime.date, str),
                    'end_date': (datetime.datetime, datetime.date, str),
                    'columns': list,
                    'limit': int,
                    'connect': TDengineConnection
                    }
             )
def get_price(code, region, frequency, start_date=datetime.datetime(2005, 1, 1),
              end_date=datetime.datetime.today().replace(
                  hour=0, minute=0, second=0, microsecond=0),
              columns=list(), limit=0, connect=taos_conn):
    global taos_conn
    if isinstance(code, str):
        codes = [code]
    else:
        codes = code
    if not columns:
        columns = td_columns.get(f'{region}_{frequency}')
    if not columns:
        columns = ["code", "time", "open", "close", "low", "high", "volume"]
    if not taos_conn:
        if not connect:
            raise Exception('taos connect unset')
        else:
            taos_conn = connect
    conn=taos_conn
    c1 = conn.cursor()
    c1.execute(f'use {region}_{frequency}')
    codes_str = f'code in {tuple([get_int_code(i, region) for i in codes])}'
    select_str = ', '.join(columns)
    start_date = format_date_param(start_date)
    end_date = format_date_param(end_date)

    time_str = f"time between '{start_date}' and '{end_date}'"
    limit_str = f"limit {limit}" if limit else ''
    if frequency in ['d1', 'tick', 'd1_post', 'd1_raw']:
        c1.execute(f"select {select_str} from {region}_st_{frequency} where ({codes_str}) "
                   f"and ({time_str}) {limit_str};")
    else:
        year_str = f"year_int between {start_date[:4]} and '{end_date[:4]}'"
        c1.execute(f"select {select_str} from {region}_st_{frequency} where ({codes_str}) "
                   f"and ({year_str}) and ({time_str}) {limit_str};")
    
    d = c1.fetchall()
    if d:
        div = len(d) // 1000000 + 1
        d_list = np.array_split(d, div)
    else:
        return pd.DataFrame(columns=columns)
    df_list = []
    for dd in d_list:
        df_list.append(pd.DataFrame(dd, columns=columns))
    df = pd.concat(df_list)
    if region == 'cn':
        if df.empty:
            return df
        df['code'] = df['code'].apply(lambda x: str(
            x)[1:]+'.XSHG' if x < 2000000 else str(x)[1:]+'.XSHE')
    return df
