from __future__ import annotations
from typing import List
import csv
from dataclasses import dataclass


@dataclass
class Symbol:

	title: str

	symbol: str

	industry: str

	curency: str

	isa_eligible: bool

	plus_only: bool

	def from_csv_row(
		title: str, 
		symbol: str, 
		industry: str, 
		currency: str, 
		isa_eligible: str, 
		plus_only: str)-> Symbol:

		symbol = "".join([l for l in symbol if l.upper() == l])

		return Symbol(
			title,
			symbol,
			industry.lower(),
			currency,
			isa_eligible=True if isa_eligible == "TRUE" else False,
			plus_only=True if plus_only == "TRUE" else False
		)

	def get_symbol(self)-> str:
		return self.symbol.upper()


def symbols(input_file: str)-> List[Symbol]:
	with open(input_file) as file:
		csvreader = csv.reader(file)
		next(csvreader, None)
		symbols = [
			Symbol.from_csv_row(r[1], r[7], r[2], r[3], r[4], r[10]) 
			for r in csvreader
		]

		print(f"Found {len(symbols)} symbols in the universe")

		return [symbol for symbol in symbols if symbol.isa_eligible == True]
