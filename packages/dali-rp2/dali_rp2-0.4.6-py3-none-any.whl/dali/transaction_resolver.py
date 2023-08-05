# Copyright 2022 eprbell
# Licensed under the Apache License, Version 2.0 (the "License");
#
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, cast

import pandas as pd
from Historic_Crypto import HistoricalData
from rp2.rp2_decimal import ZERO, RP2Decimal
from rp2.rp2_error import RP2TypeError, RP2ValueError

from dali.abstract_transaction import (
    AbstractTransaction,
    AssetAndTimestamp,
    AssetAndUniqueId,
)
from dali.cache import load_from_cache, save_to_cache
from dali.dali_configuration import Keyword, is_unknown, is_unknown_or_none
from dali.in_transaction import InTransaction
from dali.intra_transaction import IntraTransaction
from dali.logger import LOGGER
from dali.out_transaction import OutTransaction

__RESOLVER: str = "DaLI Resolver"
__HISTORICAL_PRICE_CACHE: str = "coinbase_pro_historical_prices"


def _is_number(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


def _resolve_fields(
    name1: str,
    name2: str,
    value1: str,
    value2: str,
    transaction1: AbstractTransaction,
    transaction2: AbstractTransaction,
    disallow_two_unknown: bool = True,
    if_conflict_override_second_parameter: bool = False,
) -> str:
    if disallow_two_unknown and is_unknown(value1) and is_unknown(value2):
        raise Exception(f"Internal error: {name1} and {name2} are both unknown: {transaction1}\n{transaction2}")
    if value1 and value2 and not is_unknown(value1) and not is_unknown(value2) and value1 != value2:
        if if_conflict_override_second_parameter:
            return value1
        # If values are numeric we need to compare them as numbers, not as strings
        if _is_number(value1) and _is_number(value2):
            if RP2Decimal(value1) != RP2Decimal(value2):
                raise Exception(f"Internal error: {name1} and {name2} are numeric but have different values: {transaction1}\n{transaction2}")
        else:
            raise Exception(f"Internal error: {name1} and {name2} have different values: {transaction1}\n{transaction2}")
    if is_unknown(value1):
        return value2
    if is_unknown(value2):
        return value1
    if not value1:
        return value2
    if not value2:
        return value1
    return value1


def _resolve_optional_fields(
    name1: str,
    name2: str,
    value1: Optional[str],
    value2: Optional[str],
    transaction1: AbstractTransaction,
    transaction2: AbstractTransaction,
    disallow_two_unknown: bool = True,
    if_conflict_override_second_parameter: bool = False,
) -> str:
    if is_unknown_or_none(value1) and is_unknown_or_none(value2):
        value1 = Keyword.UNKNOWN.value
        value2 = Keyword.UNKNOWN.value
    return _resolve_fields(
        name1,
        name2,
        value1 if value1 else "",
        value2 if value2 else "",
        transaction1,
        transaction2,
        disallow_two_unknown,
        if_conflict_override_second_parameter,
    )


def _load_from_historical_price_cache() -> Dict[AssetAndTimestamp, str]:
    result = load_from_cache(__HISTORICAL_PRICE_CACHE)
    return cast(Dict[AssetAndTimestamp, str], result) if result is not None else {}


def _save_to_historical_price_cache(historical_prices: Dict[AssetAndTimestamp, str]) -> None:
    save_to_cache(__HISTORICAL_PRICE_CACHE, historical_prices)


def _update_spot_price_from_web(transaction: AbstractTransaction, historical_price_cache: Dict[AssetAndTimestamp, str]) -> AbstractTransaction:
    init_parameters: Dict[str, Any] = transaction.constructor_parameter_dictionary
    if transaction.spot_price is None:  # type: ignore
        return transaction

    # If the crypto amount is very small (< $0.01), sometimes exchanges (like Coinbase) report the fiat_amount as zero. Since DaLI computes spot_price
    # as fiat amount/crypto amount, if fiat amount is 0, then spot price is 0 as well (see https://github.com/eprbell/dali-rp2/issues/19). This breaks
    # the contract with RP2, which requires spot_price to be > 0. If this situation is detected and the user passed the read_spot_price_from_web, then
    # ignore the 0 and use a price read from the Internet.
    if is_unknown(transaction.spot_price) or RP2Decimal(transaction.spot_price) == ZERO:  # type: ignore
        spot_price: Optional[str] = None
        key: AssetAndTimestamp = AssetAndTimestamp(transaction.asset, transaction.timestamp_value)
        if key in historical_price_cache:
            spot_price = historical_price_cache[key]
            LOGGER.debug("Reading spot_price for %s/%s from cache: %s", key.timestamp, key.asset, spot_price)
        else:
            time_granularity: List[int] = [60, 300, 900, 3600, 21600, 86400]
            # Coinbase API expects UTC timestamps only, see the forum discussion here:
            # https://forums.coinbasecloud.dev/t/invalid-end-on-product-candles-endpoint/320
            transaction_utc_timestamp = transaction.timestamp_value.astimezone(timezone.utc)
            from_timestamp: str = transaction_utc_timestamp.strftime("%Y-%m-%d-%H-%M")
            retry_count: int = 0
            while retry_count < len(time_granularity):
                try:
                    seconds = time_granularity[retry_count]
                    to_timestamp: str = (transaction_utc_timestamp + timedelta(seconds=seconds)).strftime("%Y-%m-%d-%H-%M")
                    df_quotes: pd.DataFrame = HistoricalData(f"{transaction.asset}-USD", seconds, from_timestamp, to_timestamp, verbose=False).retrieve_data()
                    df_quotes.index = df_quotes.index.tz_localize("UTC")  # The returned timestamps in the index are timezone naive
                    first_quote_bar: pd.Series = df_quotes.reset_index().iloc[0]
                    quote_field: str = "high"
                    spot_price = str(first_quote_bar[quote_field])
                    break
                except ValueError:
                    retry_count += 1

            if not spot_price:
                raise Exception("Unable to read spot price from Coinbase Pro")
            LOGGER.debug(
                "Fetched %s spot_price %s for %s/%s from Coinbase Pro %d second bar at %s",
                quote_field,
                spot_price,
                key.timestamp,
                key.asset,
                seconds,
                first_quote_bar.time,  # type: ignore
            )

            historical_price_cache[key] = spot_price
        notes: str = f"spot_price read from Coinbase Pro; {transaction.notes if transaction.notes else ''}"
        init_parameters[Keyword.SPOT_PRICE.value] = spot_price
        init_parameters[Keyword.NOTES.value] = notes
        init_parameters[Keyword.IS_SPOT_PRICE_FROM_WEB.value] = True
        if isinstance(transaction, InTransaction):
            return InTransaction(**init_parameters)
        if isinstance(transaction, OutTransaction):
            return OutTransaction(**init_parameters)
        if isinstance(transaction, IntraTransaction):
            return IntraTransaction(**init_parameters)
        raise Exception(f"Invalid transaction: {transaction}")

    return transaction


# This resolves incomplete transactions. An INTRA transaction from an exchange (e.g. Coinbase) to another
# (e.g. BlockFi) would be represented by two transactions (one created by the Coinbase plugin and the other by
# the BlockFi plugin). These two transactions may have incomplete information (e.g. Coinbase doesn't know the
# receiver address is BlockFi's), so this function matches the two incomplete transactions using their hash
# and/or account-specific id and merges them into one complete transaction.
def resolve_transactions(
    transactions: List[AbstractTransaction],
    global_configuration: Dict[str, Any],
    read_spot_price_from_web: bool,
) -> List[AbstractTransaction]:
    if not isinstance(transactions, List):
        raise Exception(f"Internal error: parameter 'transactions' is not of type List. {transactions}")

    resolved_transactions: List[AbstractTransaction] = []
    unique_id_2_transactions: Dict[AssetAndUniqueId, List[AbstractTransaction]] = {}
    transaction: AbstractTransaction

    historical_price_cache: Dict[AssetAndTimestamp, str] = _load_from_historical_price_cache()

    for transaction in transactions:
        if not isinstance(transaction, AbstractTransaction):
            raise Exception(f"Internal error: Parameter 'transaction' is not a subclass of AbstractTransaction. {transaction}")

        if is_unknown(transaction.unique_id):
            # Cannot resolve further if unique_id is not known
            if read_spot_price_from_web:
                transaction = _update_spot_price_from_web(transaction, historical_price_cache)
            LOGGER.debug("Unresolvable transaction (no %s): %s", Keyword.UNIQUE_ID.value, str(transaction))
            resolved_transactions.append(transaction)
        else:
            transaction_list: List[AbstractTransaction] = unique_id_2_transactions.setdefault(AssetAndUniqueId(transaction.asset, transaction.unique_id), [])
            transaction_list.append(transaction)
            unique_id_2_transactions[AssetAndUniqueId(transaction.asset, transaction.unique_id)] = transaction_list

    for transaction_list in unique_id_2_transactions.values():
        if len(transaction_list) > 2:
            raise Exception(f"Internal error: Attempting to resolve more than two transactions with same {Keyword.UNIQUE_ID.value}: {transaction_list}")
        if len(transaction_list) == 1:
            transaction = _apply_transaction_hint(transaction_list[0], global_configuration)
            if read_spot_price_from_web:
                transaction = _update_spot_price_from_web(transaction, historical_price_cache)
            LOGGER.debug("Self-contained transaction: %s", str(transaction))
            resolved_transactions.append(transaction)
            continue
        if len(transaction_list) == 0:
            raise Exception(f"Internal error: Attempting to resolve zero transactions: {transaction_list}")

        transaction1: AbstractTransaction = transaction_list[0]
        transaction2: AbstractTransaction = transaction_list[1]

        if transaction1.unique_id != transaction2.unique_id:
            raise Exception(f"Internal error: transaction1.{Keyword.UNIQUE_ID.value} != transaction2.{Keyword.UNIQUE_ID.value}: {transaction1}\n{transaction2}")
        if transaction1.asset != transaction2.asset:
            raise Exception(f"Internal error: transaction1.{Keyword.ASSET.value} != transaction2.{Keyword.ASSET.value}: {transaction1}\n{transaction2}")

        if isinstance(transaction1, InTransaction) and isinstance(transaction2, OutTransaction):
            transaction = _resolve_in_out_transaction(transaction1, transaction2, None)
        elif isinstance(transaction1, OutTransaction) and isinstance(transaction2, InTransaction):
            transaction = _resolve_out_in_transaction(transaction1, transaction2, None)
        elif isinstance(transaction1, IntraTransaction) and isinstance(transaction2, IntraTransaction):
            transaction = _resolve_intra_intra_transaction(transaction1, transaction2, None)
        else:
            raise Exception(
                f"Internal error: attempting to resolve two transactions that aren't Intra/Intra, In/Out or Out/In:\n{transaction1}\n{transaction2}"
            )

        if read_spot_price_from_web:
            transaction = _update_spot_price_from_web(transaction, historical_price_cache)

        LOGGER.debug("Resolved transaction: %s", str(transaction))
        resolved_transactions.append(transaction)

    _save_to_historical_price_cache(historical_price_cache)

    return resolved_transactions


def _apply_transaction_hint(
    transaction: AbstractTransaction,
    global_configuration: Dict[str, Any],
) -> AbstractTransaction:
    result: AbstractTransaction

    if Keyword.TRANSACTION_HINTS.value not in global_configuration:
        return transaction
    if transaction.unique_id not in global_configuration[Keyword.TRANSACTION_HINTS.value]:
        return transaction

    direction: str
    transaction_type: str
    notes: str
    (direction, transaction_type, notes) = global_configuration[Keyword.TRANSACTION_HINTS.value][transaction.unique_id]
    transaction_type = transaction_type.capitalize()
    notes = f"{notes}; {transaction.notes if transaction.notes else ''}"
    if direction == Keyword.IN.value:
        if isinstance(transaction, InTransaction):
            result = InTransaction(
                plugin=transaction.plugin,
                unique_id=transaction.unique_id,
                raw_data=f"{Keyword.IN.value}->{Keyword.IN.value}: {transaction.raw_data}",
                timestamp=transaction.timestamp,
                asset=transaction.asset,
                exchange=transaction.exchange,
                holder=transaction.holder,
                transaction_type=transaction_type,
                spot_price=transaction.spot_price if transaction.spot_price else Keyword.UNKNOWN.value,
                crypto_in=transaction.crypto_in,
                crypto_fee=transaction.crypto_fee,
                fiat_in_no_fee=transaction.fiat_in_no_fee,
                fiat_in_with_fee=transaction.fiat_in_with_fee,
                fiat_fee=transaction.fiat_fee,
                notes=notes,
            )
        elif isinstance(transaction, OutTransaction):
            raise RP2TypeError(f"Cannot change OutTransaction to InTransaction: {transaction}")
        elif isinstance(transaction, IntraTransaction):
            if not is_unknown(transaction.from_holder) or not is_unknown(transaction.from_exchange):
                raise RP2ValueError(
                    f"Invalid conversion {Keyword.INTRA.value}->{Keyword.IN.value}: "
                    f"{Keyword.FROM_HOLDER.value}/{Keyword.FROM_EXCHANGE.value} must be unknown: {transaction}"
                )
            result = InTransaction(
                plugin=transaction.plugin,
                unique_id=transaction.unique_id,
                raw_data=f"{Keyword.INTRA.value}->{Keyword.IN.value}: {transaction.raw_data}",
                timestamp=transaction.timestamp,
                asset=transaction.asset,
                exchange=transaction.to_exchange,
                holder=transaction.to_holder,
                transaction_type=transaction_type,
                spot_price=transaction.spot_price if transaction.spot_price else Keyword.UNKNOWN.value,
                crypto_in=transaction.crypto_received,
                notes=notes,
            )
    elif direction == Keyword.OUT.value:
        if isinstance(transaction, InTransaction):
            raise RP2TypeError(f"Cannot change InTransaction to OutTransaction: {transaction}")
        if isinstance(transaction, OutTransaction):
            result = OutTransaction(
                plugin=transaction.plugin,
                unique_id=transaction.unique_id,
                raw_data=f"{Keyword.OUT.value}->{Keyword.OUT.value}: {transaction.raw_data}",
                timestamp=transaction.timestamp,
                asset=transaction.asset,
                exchange=transaction.exchange,
                holder=transaction.holder,
                transaction_type=transaction_type,
                spot_price=transaction.spot_price if transaction.spot_price else Keyword.UNKNOWN.value,
                crypto_out_no_fee=transaction.crypto_out_no_fee,
                crypto_fee=transaction.crypto_fee,
                crypto_out_with_fee=transaction.crypto_out_with_fee,
                fiat_out_no_fee=transaction.fiat_out_no_fee,
                fiat_fee=transaction.fiat_fee,
                notes=notes,
            )
        elif isinstance(transaction, IntraTransaction):
            if not is_unknown(transaction.to_holder) or not is_unknown(transaction.to_exchange):
                raise RP2ValueError(
                    f"Invalid converstion {Keyword.INTRA.value}->{Keyword.OUT.value}: "
                    f"{Keyword.TO_HOLDER.value}/{Keyword.TO_EXCHANGE.value} must be unknown: {transaction}"
                )
            crypto_out_no_fee: RP2Decimal = RP2Decimal(transaction.crypto_sent)
            crypto_fee: RP2Decimal = ZERO
            if not is_unknown(transaction.crypto_received):
                crypto_out_no_fee = RP2Decimal(transaction.crypto_received)
                crypto_fee = RP2Decimal(transaction.crypto_sent) - RP2Decimal(transaction.crypto_received)

            result = OutTransaction(
                plugin=transaction.plugin,
                unique_id=transaction.unique_id,
                raw_data=f"{Keyword.INTRA.value}->{Keyword.OUT.value}: {transaction.raw_data}",
                timestamp=transaction.timestamp,
                asset=transaction.asset,
                exchange=transaction.from_exchange,
                holder=transaction.from_holder,
                transaction_type=transaction_type,
                spot_price=transaction.spot_price if transaction.spot_price else Keyword.UNKNOWN.value,
                crypto_out_no_fee=str(crypto_out_no_fee),
                crypto_fee=str(crypto_fee),
                notes=notes,
            )
    elif direction == Keyword.INTRA.value:
        if isinstance(transaction, InTransaction):
            result = IntraTransaction(
                plugin=transaction.plugin,
                unique_id=transaction.unique_id,
                raw_data=f"{Keyword.IN.value}->{Keyword.INTRA.value}: {transaction.raw_data}",
                timestamp=transaction.timestamp,
                asset=transaction.asset,
                from_exchange=Keyword.UNKNOWN.value,
                from_holder=Keyword.UNKNOWN.value,
                to_exchange=transaction.exchange,
                to_holder=transaction.holder,
                spot_price=transaction.spot_price,
                crypto_sent=Keyword.UNKNOWN.value,
                crypto_received=transaction.crypto_in,
                notes=notes,
            )
        elif isinstance(transaction, OutTransaction):
            if is_unknown(transaction.crypto_out_no_fee) or is_unknown(transaction.crypto_fee):
                raise RP2ValueError(
                    f"Invalid converstion {Keyword.INTRA.value}->{Keyword.OUT.value}: "
                    f"{Keyword.CRYPTO_OUT_NO_FEE.value}/{Keyword.CRYPTO_FEE.value} canot be unknown: {transaction}"
                )
            result = IntraTransaction(
                plugin=transaction.plugin,
                unique_id=transaction.unique_id,
                raw_data=f"{Keyword.OUT.value}->{Keyword.INTRA.value}: {transaction.raw_data}",
                timestamp=transaction.timestamp,
                asset=transaction.asset,
                from_exchange=transaction.exchange,
                from_holder=transaction.holder,
                to_exchange=Keyword.UNKNOWN.value,
                to_holder=Keyword.UNKNOWN.value,
                spot_price=transaction.spot_price,
                crypto_sent=str(RP2Decimal(transaction.crypto_out_no_fee) + RP2Decimal(transaction.crypto_fee)),
                crypto_received=Keyword.UNKNOWN.value,
                notes=notes,
            )
        elif isinstance(transaction, IntraTransaction):
            result = IntraTransaction(
                plugin=transaction.plugin,
                unique_id=transaction.unique_id,
                raw_data=f"{Keyword.INTRA.value}->{Keyword.INTRA.value}: {transaction.raw_data}",
                timestamp=transaction.timestamp,
                asset=transaction.asset,
                from_exchange=transaction.from_exchange,
                from_holder=transaction.from_holder,
                to_exchange=transaction.to_exchange,
                to_holder=transaction.to_holder,
                spot_price=transaction.spot_price,
                crypto_sent=transaction.crypto_sent,
                crypto_received=transaction.crypto_received,
                notes=notes,
            )
    else:
        raise RP2ValueError(f"Invalid direction {direction}")

    return result


def _resolve_intra_intra_transaction(
    transaction1: IntraTransaction,
    transaction2: IntraTransaction,
    notes: Optional[str],
) -> IntraTransaction:

    # Pick the max of the two timestamps as the timestamp of the new resolved transaction
    timestamp: datetime = max(transaction1.timestamp_value, transaction2.timestamp_value)
    from_exchange: str = _resolve_fields(
        f"transaction1.{Keyword.FROM_EXCHANGE.value}",
        f"transaction2.{Keyword.FROM_EXCHANGE.value}",
        transaction1.from_exchange,
        transaction2.from_exchange,
        transaction1,
        transaction2,
    )
    from_holder: str = _resolve_fields(
        f"transaction1.{Keyword.FROM_HOLDER.value}",
        f"transaction2.{Keyword.FROM_HOLDER.value}",
        transaction1.from_holder,
        transaction2.from_holder,
        transaction1,
        transaction2,
    )
    to_exchange: str = _resolve_fields(
        f"transaction1.{Keyword.TO_EXCHANGE.value}",
        f"transaction2.{Keyword.TO_EXCHANGE.value}",
        transaction1.to_exchange,
        transaction2.to_exchange,
        transaction1,
        transaction2,
    )
    to_holder: str = _resolve_fields(
        f"transaction1.{Keyword.TO_HOLDER.value}",
        f"transaction2.{Keyword.TO_HOLDER.value}",
        transaction1.to_holder,
        transaction2.to_holder,
        transaction1,
        transaction2,
    )
    spot_price: str
    # If one of the transaction has spot_price from web, and the other doesn't take the non-web one
    if transaction1.is_spot_price_from_web:
        spot_price = _resolve_optional_fields(
            f"transaction2.{Keyword.SPOT_PRICE.value}",
            f"transaction1.{Keyword.SPOT_PRICE.value}",
            transaction2.spot_price,
            transaction1.spot_price,
            transaction2,
            transaction1,
            disallow_two_unknown=False,
            if_conflict_override_second_parameter=True,
        )
    elif transaction2.is_spot_price_from_web:
        spot_price = _resolve_optional_fields(
            f"transaction1.{Keyword.SPOT_PRICE.value}",
            f"transaction2.{Keyword.SPOT_PRICE.value}",
            transaction1.spot_price,
            transaction2.spot_price,
            transaction1,
            transaction2,
            disallow_two_unknown=False,
            if_conflict_override_second_parameter=True,
        )
    else:
        spot_price = _resolve_optional_fields(
            f"transaction1.{Keyword.SPOT_PRICE.value}",
            f"transaction2.{Keyword.SPOT_PRICE.value}",
            transaction1.spot_price,
            transaction2.spot_price,
            transaction1,
            transaction2,
            disallow_two_unknown=False,
            if_conflict_override_second_parameter=False,
        )
    crypto_sent: str = _resolve_fields(
        f"transaction1.{Keyword.CRYPTO_SENT.value}",
        f"transaction2.{Keyword.CRYPTO_SENT.value}",
        transaction1.crypto_sent,
        transaction2.crypto_sent,
        transaction1,
        transaction2,
    )
    crypto_received: str = _resolve_fields(
        f"transaction1.{Keyword.CRYPTO_RECEIVED.value}",
        f"transaction2.{Keyword.CRYPTO_RECEIVED.value}",
        transaction1.crypto_received,
        transaction2.crypto_received,
        transaction1,
        transaction2,
    )

    notes = f"{notes}; " if notes else ""
    notes += f"{transaction1.notes}; " if transaction1.notes else ""
    notes += f"{transaction2.notes}; " if transaction2.notes else ""

    return IntraTransaction(
        plugin=__RESOLVER,
        unique_id=transaction1.unique_id,
        raw_data=f"{transaction1.raw_data}\n{transaction2.raw_data}",
        asset=transaction1.asset,
        timestamp=str(timestamp),
        from_exchange=from_exchange,
        from_holder=from_holder,
        to_exchange=to_exchange,
        to_holder=to_holder,
        spot_price=spot_price,
        crypto_sent=crypto_sent,
        crypto_received=crypto_received,
        notes=notes,
    )


def _resolve_out_in_transaction(
    out_transaction: OutTransaction,
    in_transaction: InTransaction,
    notes: Optional[str],
) -> IntraTransaction:
    return _resolve_in_out_transaction(in_transaction, out_transaction, notes)


def _resolve_in_out_transaction(
    in_transaction: InTransaction,
    out_transaction: OutTransaction,
    notes: Optional[str],
) -> IntraTransaction:

    timestamp: datetime = in_transaction.timestamp_value
    from_exchange: str = out_transaction.exchange
    from_holder: str = out_transaction.holder
    to_exchange: str = in_transaction.exchange
    to_holder: str = in_transaction.holder
    spot_price: str = _resolve_fields(
        f"out_transaction.{Keyword.SPOT_PRICE.value}",
        f"in_transaction.{Keyword.SPOT_PRICE.value}",
        out_transaction.spot_price,
        in_transaction.spot_price,
        out_transaction,
        in_transaction,
        disallow_two_unknown=False,
    )
    # If one of the transaction has spot_price from web, and the other doesn't take the non-web one
    if out_transaction.is_spot_price_from_web:
        spot_price = _resolve_fields(
            f"in_transaction.{Keyword.SPOT_PRICE.value}",
            f"out_transaction.{Keyword.SPOT_PRICE.value}",
            in_transaction.spot_price,
            out_transaction.spot_price,
            in_transaction,
            out_transaction,
            disallow_two_unknown=False,
            if_conflict_override_second_parameter=True,
        )
    elif in_transaction.is_spot_price_from_web:
        spot_price = _resolve_fields(
            f"out_transaction.{Keyword.SPOT_PRICE.value}",
            f"in_transaction.{Keyword.SPOT_PRICE.value}",
            out_transaction.spot_price,
            in_transaction.spot_price,
            out_transaction,
            in_transaction,
            disallow_two_unknown=False,
            if_conflict_override_second_parameter=True,
        )
    else:
        spot_price = _resolve_fields(
            f"out_transaction.{Keyword.SPOT_PRICE.value}",
            f"in_transaction.{Keyword.SPOT_PRICE.value}",
            out_transaction.spot_price,
            in_transaction.spot_price,
            out_transaction,
            in_transaction,
            disallow_two_unknown=False,
            if_conflict_override_second_parameter=False,
        )

    crypto_sent: str = str(RP2Decimal(out_transaction.crypto_out_no_fee) + RP2Decimal(out_transaction.crypto_fee))
    crypto_received: str = in_transaction.crypto_in

    notes = f"{notes}; " if notes else ""
    notes += f"{in_transaction.notes}; " if in_transaction.notes else ""
    notes += f"{out_transaction.notes}; " if out_transaction.notes else ""

    transaction = IntraTransaction(
        plugin=__RESOLVER,
        unique_id=in_transaction.unique_id,
        raw_data=f"{in_transaction.raw_data}\n{out_transaction.raw_data}",
        asset=in_transaction.asset,
        timestamp=str(timestamp),
        from_exchange=from_exchange,
        from_holder=from_holder,
        to_exchange=to_exchange,
        to_holder=to_holder,
        spot_price=spot_price,
        crypto_sent=crypto_sent,
        crypto_received=crypto_received,
        notes=notes,
    )

    return transaction
