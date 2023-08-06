from cache.holder.RedisCacheHolder import RedisCacheHolder
from core.constants.not_available import NOT_AVAILABLE
from core.options.exception.MissingOptionError import MissingOptionError

from fees.trade.exception.NoTradeFeeError import NoTradeFeeError
from fees.trade.filter.TradeFeeFilter import TradeFeeFilter

ACCOUNT_TRADE_FEE_KEY = 'ACCOUNT_TRADE_FEE_KEY'
INSTRUMENT_TRADE_FEE_KEY = 'INSTRUMENT_TRADE_FEE_KEY'


class TradeFeeProvider:

    def __init__(self, options, trade_fee_filter: TradeFeeFilter):
        self.options = options
        self.__check_options()
        self.cache = RedisCacheHolder()
        self.trade_fee_filter = trade_fee_filter

    def __check_options(self):
        if self.options is None:
            raise MissingOptionError(f'missing option please provide options {ACCOUNT_TRADE_FEE_KEY} and {INSTRUMENT_TRADE_FEE_KEY}')
        if ACCOUNT_TRADE_FEE_KEY not in self.options:
            raise MissingOptionError(f'missing option please provide option {ACCOUNT_TRADE_FEE_KEY}')
        if INSTRUMENT_TRADE_FEE_KEY not in self.options:
            raise MissingOptionError(f'missing option please provide option {INSTRUMENT_TRADE_FEE_KEY}')

    def get_account_trade_fee(self) -> float:
        fee_key = self.options[ACCOUNT_TRADE_FEE_KEY]
        account_fee = self.cache.fetch(fee_key, as_type=float)
        if account_fee is None:
            account_fee = self.trade_fee_filter.obtain_account_trade_fee()
            if account_fee is not None:
                self.cache.store(fee_key, account_fee)
        return self.return_appropriate_value(account_fee, 'account')

    def get_instrument_trade_fee(self, instrument) -> float:
        fee_key = self.options[INSTRUMENT_TRADE_FEE_KEY].format(instrument=instrument)
        instrument_fee = self.cache.fetch(fee_key, as_type=float)
        if instrument_fee is None:
            instrument_fee = self.trade_fee_filter.obtain_instrument_trade_fee(instrument)
            if instrument_fee is not None:
                self.cache.store(fee_key, instrument_fee)
        return self.return_appropriate_value(instrument_fee, f'instrument {instrument}')

    @staticmethod
    def return_appropriate_value(value, trade_fee_ref):
        if value is None:
            raise NoTradeFeeError(f'No trade fee for {trade_fee_ref}')
        return None if value == NOT_AVAILABLE else value
