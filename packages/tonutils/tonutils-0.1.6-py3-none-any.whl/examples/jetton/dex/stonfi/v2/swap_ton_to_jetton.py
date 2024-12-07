from tonutils.client import TonapiClient
from tonutils.jetton import JettonMaster
from tonutils.jetton.dex.stonfi.addresses import *
from tonutils.jetton.dex.stonfi.contract.v2 import StonfiRouterV2
from tonutils.utils import to_nano
from tonutils.wallet import WalletV4R2

# API key for accessing the Tonapi (obtainable from https://tonconsole.com)
API_KEY = "AE33EX7D5SZGV2IAAAAI5DEWPLH5OBGVWJ6SUZTUI735PRHOP2C3ALDHIWH4X7VK2AO3FYQ"

# Set to True for the test network, False for the main network
IS_TESTNET = True

# Mnemonic phrase used to connect the wallet
MNEMONIC = "unknown receive logic boring turkey dolphin tape lock hammer protect shield upgrade ecology system front attack mercy damage poet enlist settle universe manage lunar"  # noqa

# Address of the Jetton Master contract
JETTON_MASTER_ADDRESS = "kQB_TOJSB7q3-Jm1O8s0jKFtqLElZDPjATs5uJGsujcjznq3"

# Amount of TON to swap
SWAP_TON_AMOUNT = 0.1


async def main() -> None:
    client = TonapiClient(api_key=API_KEY, is_testnet=IS_TESTNET)
    wallet, _, _, _ = WalletV4R2.from_mnemonic(client, MNEMONIC)

    router_address = TESTNET_V2_ROUTER_ADDRESS if IS_TESTNET else V2_ROUTER_ADDRESS
    proxy_address = TESTNET_PTON_V2_ADDRESS if IS_TESTNET else PTON_V2_ADDRESS

    offer_address = await JettonMaster.get_wallet_address(
        client=client,
        owner_address=router_address,
        jetton_master_address=proxy_address,
    )
    ask_jetton_wallet_address = await JettonMaster.get_wallet_address(
        client=wallet.client,
        owner_address=router_address,
        jetton_master_address=JETTON_MASTER_ADDRESS,
    )

    body = StonfiRouterV2.build_swap_body(
        jetton_amount=to_nano(SWAP_TON_AMOUNT),
        recipient_address=router_address,
        forward_amount=to_nano(0.3),
        user_wallet_address=wallet.address,
        min_amount=1,
        ask_jetton_wallet_address=ask_jetton_wallet_address,
    )

    tx_hash = await wallet.transfer(
        destination=offer_address,
        amount=SWAP_TON_AMOUNT + 0.3,
        body=body,
    )

    print("Successfully swapped TON to Jetton!")
    print(f"Transaction hash: {tx_hash}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
