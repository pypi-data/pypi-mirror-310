import akshare as ak
from .base_fetcher import BaseFetcher
import pandas as pd
from typing import Any

class StockChipFetcher(BaseFetcher):
    def __init__(self, stock_data: Any):
        self.stock_data = stock_data
        super().__init__(stock_data.code, file_name = "stock_chip")
        
    def fetch_data(self):
        try:
            print("Fetching stock chip data!")
            data = ak.stock_cyq_em(
                symbol=self.stock_data.code, 
                adjust=self.stock_data.adjust
            )
            if data is None or data.empty:
                raise ValueError("No data returned from the API.")
            return data
        except Exception as e:
            print(f"Error fetching data: {e}")
            return pd.DataFrame()
        
