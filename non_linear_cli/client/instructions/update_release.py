from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
from ..program_id import PROGRAM_ID


class UpdateReleaseAccounts(typing.TypedDict):
    sender: Pubkey
    proxy_metadata: Pubkey
    stream_metadata: Pubkey
    withdrawor: Pubkey
    streamflow_program: Pubkey


def update_release(
    accounts: UpdateReleaseAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["sender"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["proxy_metadata"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["stream_metadata"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["withdrawor"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["streamflow_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"M\xc2<\xe3\x0f\xd4*`"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
