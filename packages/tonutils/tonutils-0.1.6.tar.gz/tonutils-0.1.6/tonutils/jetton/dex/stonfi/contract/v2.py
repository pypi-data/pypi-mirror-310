import time
from typing import Union, Optional

from pytoniq_core import Address, Cell, begin_cell

from tonutils.jetton.dex.stonfi.op_codes import *


class StonfiRouterV2:

    @classmethod
    def build_swap_body(
            cls,
            jetton_amount: int,
            recipient_address: Union[Address, str],
            forward_amount: int,
            user_wallet_address: Union[Address, str],
            min_amount: int,
            ask_jetton_wallet_address: Union[Address, str],
            referral_amount: Optional[int] = None,
            referral_address: Optional[Union[Address, str]] = None,
    ) -> Cell:
        forward_payload = (
            begin_cell()
            .store_uint(SWAP_V2_OPCODE, 32)
            .store_address(ask_jetton_wallet_address)
            .store_address(user_wallet_address)
            .store_address(user_wallet_address)
            .store_uint(int(time.time()), 64)
            .store_ref(
                begin_cell()
                .store_coins(min_amount)
                .store_address(recipient_address)
                .store_coins(0)
                .store_uint(0, 1)
                .store_coins(0)
                .store_uint(0, 1)
                .store_uint(referral_amount or 10, 16)
                .store_address(referral_address)
                .end_cell()
            )
            .end_cell()
        )

        return (
            begin_cell()
            .store_uint(0x1f3835d, 32)
            .store_uint(0, 64)
            .store_coins(jetton_amount)
            .store_address(recipient_address)
            .store_bit(True)
            .store_ref(forward_payload)
            .end_cell()
        )
