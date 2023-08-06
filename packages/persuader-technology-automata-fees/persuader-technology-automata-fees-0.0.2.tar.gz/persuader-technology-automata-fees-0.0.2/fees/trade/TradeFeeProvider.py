from cache.holder.RedisCacheHolder import RedisCacheHolder
from core.constants.not_available import NOT_AVAILABLE

from fees.trade.filter.TradeFeeFilter import TradeFeeFilter


class TradeFeeProvider:

    def __init__(self, options, trade_fee_filter: TradeFeeFilter):
        self.options = options
        self.cache = RedisCacheHolder()
        self.trade_fee_filter = trade_fee_filter

    def get_account_trade_fee(self) -> float:
        fee_key = self.options['ACCOUNT_TRADE_FEE_KEY']
        account_fee = self.cache.fetch(fee_key, as_type=float)
        if account_fee is None:
            account_fee = self.trade_fee_filter.obtain_account_trade_fee()
            self.cache.store(fee_key, account_fee)
        return self.__return_not_available_value(account_fee)

    def get_instrument_trade_fee(self, instrument) -> float:
        fee_key = self.options['{instrument}_TRADE_FEE_KEY'.format(instrument=instrument)]
        instrument_fee = self.cache.fetch(fee_key, as_type=float)
        if instrument_fee is None:
            instrument_fee = self.trade_fee_filter.obtain_instrument_trade_fee(instrument)
            self.cache.store(fee_key, instrument_fee)
        return self.__return_not_available_value(instrument_fee)

    @staticmethod
    def __return_not_available_value(value):
        return None if value == NOT_AVAILABLE else value
