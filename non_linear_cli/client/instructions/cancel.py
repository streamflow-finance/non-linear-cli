from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from spl.token.constants import TOKEN_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
from ..program_id import PROGRAM_ID


class CancelAccounts(typing.TypedDict):
    sender: Pubkey
    sender_tokens: Pubkey
    recipient: Pubkey
    recipient_tokens: Pubkey
    proxy_metadata: Pubkey
    proxy_tokens: Pubkey
    stream_metadata: Pubkey
    escrow_tokens: Pubkey
    streamflow_treasury: Pubkey
    streamflow_treasury_tokens: Pubkey
    partner: Pubkey
    partner_tokens: Pubkey
    mint: Pubkey
    streamflow_program: Pubkey


def cancel(
    accounts: CancelAccounts,
    program_id: Pubkey = PROGRAM_ID,
    remaining_accounts: typing.Optional[typing.List[AccountMeta]] = None,
) -> Instruction:
    keys: list[AccountMeta] = [
        AccountMeta(pubkey=accounts["sender"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["sender_tokens"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["recipient"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["recipient_tokens"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["proxy_metadata"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["proxy_tokens"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["stream_metadata"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["escrow_tokens"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["streamflow_treasury"], is_signer=False, is_writable=True),
        AccountMeta(
            pubkey=accounts["streamflow_treasury_tokens"],
            is_signer=False,
            is_writable=True,
        ),
        AccountMeta(pubkey=accounts["partner"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["partner_tokens"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["streamflow_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\xe8\xdb\xdf)\xdb\xec\xdc\xbe"
    encoded_args = b""
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
