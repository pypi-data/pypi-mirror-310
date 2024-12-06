import pytest
from ape_ethereum.transactions import TransactionType
from ethpm_types import MethodABI


@pytest.mark.parametrize(
    "tx_kwargs",
    [
        {},  # Default is type 0 in BSC.
        {"type": 0},
        {"gas_price": 0},
        {"gasPrice": 0},
    ],
)
def test_create_transaction_type_0(bsc, tx_kwargs):
    txn = bsc.create_transaction(**tx_kwargs)
    assert txn.type == TransactionType.STATIC.value


@pytest.mark.parametrize(
    "tx_kwargs",
    [
        {"type": 2},
        {"max_fee": 0},
        {"max_fee_per_gas": 0},
        {"maxFee": 0},
        {"max_priority_fee_per_gas": 0},
        {"max_priority_fee": 0},
        {"maxPriorityFeePerGas": 0},
    ],
)
def test_create_transaction_type_2(bsc, tx_kwargs):
    """
    Show is smart-enough to deduce type 2 transactions.
    """

    txn = bsc.create_transaction(**tx_kwargs)
    assert txn.type == TransactionType.DYNAMIC.value


@pytest.mark.parametrize(
    "tx_type",
    (TransactionType.STATIC.value, TransactionType.DYNAMIC.value),
)
def test_encode_transaction(tx_type, bsc, eth_tester_provider):
    abi = MethodABI.model_validate(
        {
            "type": "function",
            "name": "fooAndBar",
            "stateMutability": "nonpayable",
            "inputs": [],
            "outputs": [],
        }
    )
    address = "0x274b028b03A250cA03644E6c578D81f019eE1323"
    actual = bsc.encode_transaction(address, abi, sender=address, type=tx_type)
    assert actual.gas_limit == eth_tester_provider.max_gas


def test_is_mainnet(bsc):
    assert bsc.mainnet.is_mainnet
    assert bsc.opbnb.is_mainnet
    assert not bsc.testnet.is_mainnet
    assert not bsc.opbnb_testnet.is_mainnet
