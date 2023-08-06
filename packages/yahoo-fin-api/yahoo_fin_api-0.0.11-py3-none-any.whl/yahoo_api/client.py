from __future__ import annotations
from typing import List
import requests
from pathlib import Path
from threading import Thread
import json
import yahoo_api.universe as Universe

modules = [
	"assetProfile",
	"balanceSheetHistory",
	"balanceSheetHistoryQuarterly",
	"calendarEvents",
	"cashflowStatementHistory",
	"cashflowStatementHistoryQuarterly",
	"defaultKeyStatistics",
	"earnings",
	"earningsHistory",
	"earningsTrend",
	"financialData",
	"fundOwnership",
	"incomeStatementHistory",
	"incomeStatementHistoryQuarterly",
	"indexTrend",
	"industryTrend",
	"insiderHolders",
	"insiderTransactions",
	"institutionOwnership",
	"majorDirectHolders",
	"majorHoldersBreakdown",
	"netSharePurchaseActivity",
	"price",
	"quoteType",
	"recommendationTrend",
	"secFilings",
	"sectorTrend",
	"summaryDetail",
	"summaryProfile",
	"symbol",
	"upgradeDowngradeHistory",
	"fundProfile",
	"topHoldings",
	"fundPerformanc"
]

headers = {"User-agent": "Mozilla/5.0"}

dir = Path(__file__).parent.resolve()

class Client:

	def __init__(
		self, 
		cache_response: bool = False, 
		input_csv_file: str = None,
		download_folder_path: str = None)-> None:

		if download_folder_path is None:
			download_folder_path = f"{dir}"

		# check if folder exists
		Path(download_folder_path).mkdir(parents=True, exist_ok=True)

		self.input_csv_file = input_csv_file
		self.download_folder_path = download_folder_path
		self.cache_response = cache_response

	def __cache_file(self, symbol: str)-> str:
		return f"{self.download_folder_path}/{symbol}.json"

	def __is_cached(self, symbol: str)-> bool:
		return Path(self.__cache_file(symbol)).is_file()

	def __from_cache(self, symbol: str)-> dict:
		with open(self.__cache_file(symbol), "r") as file:
			return json.loads(file.read())

	def __to_cache(self, symbol: str, body: dict)-> None:
		with open(self.__cache_file(symbol), "w") as file:
			file.write(json.dumps(body))

	def __get_symbol_async(self, symbol: str, result: dict):
		data = self.get_symbol(symbol)
		if data is None:
			print(f"symbol {symbol} is none")
			exit(1)
		result[symbol] = self.get_symbol(symbol)

	def __is_valid_response(self, body: dict)-> bool:
		keys = ["financialData", "summaryDetail"]
		return len([k for k in keys if k in body]) > 0

	def clear_cache(self, symbol: str)-> bool:
		symbol = symbol.upper()
		if self.__is_cached(symbol) is False:
			return True

		Path(self.__cache_file(symbol)).unlink()

		return True
	
	def get_symbol(self, symbol: str)-> dict | None:
		if isinstance(symbol, str) is False:
			raise Exception("symbol is not string")

		symbol = symbol.upper()

		if self.__is_cached(symbol):
			return self.__from_cache(symbol)

		url = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{symbol}?modules={modules}"
		res = requests.get(
			url.format(symbol=symbol, modules=",".join(modules)), 
			headers=headers,
		)

		if res.status_code != 200:
			return None

		body = res.json()

		if body["quoteSummary"]["error"] is not None:
			return None

		body = body["quoteSummary"]["result"][0]

		if self.__is_valid_response(body) == False:
			return None

		if self.cache_response:
			self.__to_cache(symbol, body)

		return body

	def get_symbols(self, symbols: List[str] = None)-> List[dict]:
		if symbols is None:
			symbols = [ s.get_symbol() for s in Universe.symbols(self.input_csv_file) ]

		threads = []
		results = {}
		for i, symbol in enumerate(symbols, start=1):
			print(f"{i}/{len(symbols)} Processing {symbol}")

			threads.append(
				Thread(target=self.__get_symbol_async, args=(symbol, results,)),
			)
			threads[-1].start()

		for t in threads:
			t.join()

		print(f"Completed {len(results)}/{len(symbols)}")
		return [ ticker for ticker in list(results.values()) if ticker is not None ]
