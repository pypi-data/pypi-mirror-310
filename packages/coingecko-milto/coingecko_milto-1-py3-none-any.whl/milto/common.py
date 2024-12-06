import sqlite3

import pandas as pd
import requests


def read_json_from_web_api(api_url: str, headers: dict, params: dict) -> dict:
    return (
        requests
        .get(url=api_url, headers=headers, params=params)
        .json()
    )


def overwrite_sqlite_table(db_name: str, table_name: str, df: pd.DataFrame) -> None:
    with sqlite3.connect(db_name) as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        conn.commit()


def execute_sql(db_name: str, sql: str) -> None:
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        cursor.close()
        conn.commit()


