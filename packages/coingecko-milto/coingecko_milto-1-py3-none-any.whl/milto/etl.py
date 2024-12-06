from typing import Dict

import pandas as pd

from milto.base import BaseETL
from milto.common import read_json_from_web_api, overwrite_sqlite_table, execute_sql

COINGECKO_GET_COINS_ENDPOINT = 'https://api.coingecko.com/api/v3/coins/markets'


class CoinGeckoETL(BaseETL):
    def __init__(self, db_name):
        super().__init__()
        self.db_name = db_name

    def extract(self) -> Dict[str, pd.DataFrame]:
        self.logger.info(f"Reading from {COINGECKO_GET_COINS_ENDPOINT}")

        top_100_coins_by_market_cap = read_json_from_web_api(
            api_url=COINGECKO_GET_COINS_ENDPOINT,
            headers={},
            params={
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": 100,
                "page": 1
            }
        )

        self.logger.info(f"""
            Successful read from {COINGECKO_GET_COINS_ENDPOINT}. 
            Top 10 rows from response: {top_100_coins_by_market_cap[:10]}"""
        )

        top_100_coins_by_market_cap = pd.DataFrame(top_100_coins_by_market_cap)

        return {
            'top_100_coins_by_market_cap': top_100_coins_by_market_cap
        }

    def transform(self, top_100_coins_by_market_cap: pd.DataFrame):
        self.logger.info('Doing transformations...')

        top_100_coins_by_market_cap = (
            top_100_coins_by_market_cap[
                ["id", "symbol", "name", "current_price", "market_cap"]
            ]
        )

        total_market_cap = top_100_coins_by_market_cap["market_cap"].sum()

        top_100_coins_by_market_cap["market_cap_share"] = (
            top_100_coins_by_market_cap["market_cap"] / total_market_cap * 100
        )

        top_100_coins_by_market_cap["current_price"] = (
            top_100_coins_by_market_cap["current_price"].round(2)
        )

        top_100_coins_by_market_cap["market_cap_share"] = (
            top_100_coins_by_market_cap["market_cap_share"].round(2)
        )

        self.logger.info('Transformations done!')

        return {
            'top_100_coins_by_market_cap': top_100_coins_by_market_cap
        }

    def load(self, top_100_coins_by_market_cap: pd.DataFrame):
        self.logger.info(f"Creating table 'top_100_coins_by_market_cap' in {self.db_name} if not exists...")
        execute_sql(
            db_name=self.db_name,
            sql="""
                CREATE TABLE IF NOT EXISTS top_100_coins_by_market_cap (
                    id TEXT PRIMARY KEY,
                    symbol TEXT,
                    name TEXT,
                    current_price REAL,
                    market_cap REAL,
                    market_cap_share REAL
                )
            """
        )
        self.logger.info(f"Done!")

        self.logger.info(f"Writing to 'top_100_coins_by_market_cap' table in {self.db_name}...")
        overwrite_sqlite_table(
            db_name=self.db_name,
            table_name='top_100_coins_by_market_cap',
            df=top_100_coins_by_market_cap
        )
        self.logger.info(f"Done!")

        self.logger.info(f"Creating view 'top_10_coins_by_market_share' in {self.db_name} if not exists...")
        execute_sql(
            db_name=self.db_name,
            sql="""
                CREATE VIEW IF NOT EXISTS top_10_coins_by_market_share AS 
                    SELECT
                        id,
                        symbol,
                        name,
                        current_price,
                        market_cap,
                        market_cap_share
                    FROM
                        top_100_coins_by_market_cap
                    ORDER BY 
                        market_cap_share DESC
                    LIMIT 10
            """
        )
        self.logger.info(f"Done!")
