import json
from typing import Dict, Union, Optional
from web3.datastructures import AttributeDict
from web3.eth import Contract  # noqa: F401
from web3.types import Address, ChecksumAddress, TxReceipt
from decimal import *

AddressLike = Union[Address, ChecksumAddress]


class Response(object):
    def __init__(self, status_code, err_code, err_msg, data=None, **kwargs):
        self.status_code = status_code
        self.err_msg = err_msg if err_msg else ''
        self.err_code = err_code if err_code else ''
        self.data = data if data else ''

        if 'leverage' in kwargs:
            self._data["leverage"] = kwargs["leverage"]
        if 'margin' in kwargs:
            self._data["margin"] = kwargs["margin"]

    def __str__(self):
        return str({
            'status_code': self.status_code,
            'data': self.data,
            'error': {
                'code': self.err_code,
                'message': self.err_msg
            }
        })

    def __dict__(self):
        return json.loads(self.__str__().replace("'", '"'))


class TraderPosition:
    def __init__(self, symbol, side, size, collateral, leverage, entry_price, margin, unrealized_pnl):
        self._symbol = symbol
        self._side = side
        self._size = abs(size)
        self._collateral = collateral
        self._leverage = leverage
        self._entry_price = abs(entry_price)
        self._margin = margin
        self._unrealized_pnl = unrealized_pnl

    def __str__(self):
        return str({
            "symbol": self._symbol,
            "side": self._side,
            "size": self._size,
            "collateral": self._collateral,
            "leverage": self._leverage,
            "entry_price": self._entry_price,
            "margin": self._margin,
            "unrealized_pnl": self._unrealized_pnl
        })

    def __dict__(self):
        return json.loads(self.__str__().replace("'", '"'))


class OpenPositionRes:
    def __init__(self, price: int, side: str, size: int, leverage: int, collateral_ratio: int, tx: TxReceipt):
        self._price = abs(price)
        self._side = side
        self._size = abs(size)
        self._leverage = leverage
        self._collateral_ratio = collateral_ratio
        self._tx = tx

    def __str__(self):
        return str({
            "price": self._price,
            "side": self._side,
            "size": self._size,
            "leverage": self._leverage,
            "margin_ratio": self._collateral_ratio,
            "tx_hash": self._tx['transactionHash'].hex(),
            "gas_fees": self._tx["gasUsed"]
        })

    def __dict__(self):
        return json.loads(self.__str__().replace("'", '"'))


class MarginRes:
    def __init__(self, collateral: int, leverage: int, collateral_ratio: int, tx: TxReceipt):
        self._leverage = leverage
        self._collateral = collateral
        self._collateral_ratio = collateral_ratio
        self._tx = tx

    def __str__(self):
        return str({
            "leverage": self._leverage,
            "margin": self._collateral,
            "margin_ratio": self._collateral_ratio,
            "tx_hash": self._tx['transactionHash'].hex(),
            "gas_fees": self._tx["gasUsed"]
        })

    def __dict__(self):
        return json.loads(self.__str__().replace("'", '"'))


class FundingRateRes:
    def __init__(
        self,
        longFundingRate: int,
        shortFundingRate: int,
        totalLongPosition: int,
        totalShortPosition: int,
        predictedLongFundingRate: int,
        predictedShortFundingRate: int,
        future: str
    ):

        self._longFundingRate = longFundingRate
        self._shortFundingRate = shortFundingRate
        self._totalLongPosition = totalLongPosition
        self._totalShortPosition = totalShortPosition
        self._predictedLongFundingRate = predictedLongFundingRate
        self._predictedShortFundingRate = predictedShortFundingRate
        self._future = future

    def __str__(self):
        return str({
            "longFundingRate": "{:f}".format(self._longFundingRate),
            "shortFundingRate": "{:f}".format(self._shortFundingRate),
            "totalLongPosition": "{:f}".format(self._totalLongPosition),
            "totalShortPosition": "{:f}".format(self._totalShortPosition),
            "predictedLongFundingRate": "{:f}".format(self._predictedLongFundingRate),
            "predictedShortFundingRate": "{:f}".format(self._predictedShortFundingRate),
            "symbol": self._future
        })

    def __dict__(self):
        return json.loads(self.__str__().replace("'", '"'))
