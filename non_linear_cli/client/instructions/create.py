from __future__ import annotations
import typing
from solders.pubkey import Pubkey
from solders.system_program import ID as SYS_PROGRAM_ID
from solders.sysvar import RENT
from spl.token.constants import TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID
from solders.instruction import Instruction, AccountMeta
import borsh_construct as borsh
from .. import types
from ..program_id import PROGRAM_ID


class CreateArgs(typing.TypedDict):
    ix: types.create_params.CreateParams


layout = borsh.CStruct("ix" / types.create_params.CreateParams.layout)


class CreateAccounts(typing.TypedDict):
    sender: Pubkey
    sender_tokens: Pubkey
    recipient: Pubkey
    recipient_tokens: Pubkey
    proxy_metadata: Pubkey
    proxy_tokens: Pubkey
    stream_metadata: Pubkey
    escrow_tokens: Pubkey
    withdrawor: Pubkey
    partner: Pubkey
    partner_tokens: Pubkey
    mint: Pubkey
    fee_oracle: Pubkey
    streamflow_program: Pubkey


def create(
    args: CreateArgs,
    accounts: CreateAccounts,
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
        AccountMeta(pubkey=accounts["stream_metadata"], is_signer=True, is_writable=True),
        AccountMeta(pubkey=accounts["escrow_tokens"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["withdrawor"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["partner"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["partner_tokens"], is_signer=False, is_writable=True),
        AccountMeta(pubkey=accounts["mint"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["fee_oracle"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=RENT, is_signer=False, is_writable=False),
        AccountMeta(pubkey=accounts["streamflow_program"], is_signer=False, is_writable=False),
        AccountMeta(pubkey=TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=ASSOCIATED_TOKEN_PROGRAM_ID, is_signer=False, is_writable=False),
        AccountMeta(pubkey=SYS_PROGRAM_ID, is_signer=False, is_writable=False),
    ]
    if remaining_accounts is not None:
        keys += remaining_accounts
    identifier = b"\x18\x1e\xc8(\x05\x1c\x07w"
    encoded_args = layout.build(
        {
            "ix": args["ix"].to_encodable(),
        }
    )
    data = identifier + encoded_args
    return Instruction(program_id, data, keys)
