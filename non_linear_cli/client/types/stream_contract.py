from __future__ import annotations
from . import create_stream_params
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class StreamContractJSON(typing.TypedDict):
    magic: int
    version: int
    created_at: int
    amount_withdrawn: int
    canceled_at: int
    end_time: int
    last_withdrawn_at: int
    sender: str
    sender_tokens: str
    recipient: str
    recipient_tokens: str
    mint: str
    escrow_tokens: str
    streamflow_treasury: str
    streamflow_treasury_tokens: str
    streamflow_fee_total: int
    streamflow_fee_withdrawn: int
    streamflow_fee_percent: float
    partner: str
    partner_tokens: str
    partner_fee_total: int
    partner_fee_withdrawn: int
    partner_fee_percent: float
    ix: create_stream_params.CreateStreamParamsJSON
    ix_padding: list[int]
    closed: bool
    current_pause_start: int
    pause_cumulative: int
    last_rate_change_time: int
    funds_unlocked_at_last_rate_change: int


@dataclass
class StreamContract:
    layout: typing.ClassVar = borsh.CStruct(
        "magic" / borsh.U64,
        "version" / borsh.U8,
        "created_at" / borsh.U64,
        "amount_withdrawn" / borsh.U64,
        "canceled_at" / borsh.U64,
        "end_time" / borsh.U64,
        "last_withdrawn_at" / borsh.U64,
        "sender" / BorshPubkey,
        "sender_tokens" / BorshPubkey,
        "recipient" / BorshPubkey,
        "recipient_tokens" / BorshPubkey,
        "mint" / BorshPubkey,
        "escrow_tokens" / BorshPubkey,
        "streamflow_treasury" / BorshPubkey,
        "streamflow_treasury_tokens" / BorshPubkey,
        "streamflow_fee_total" / borsh.U64,
        "streamflow_fee_withdrawn" / borsh.U64,
        "streamflow_fee_percent" / borsh.F32,
        "partner" / BorshPubkey,
        "partner_tokens" / BorshPubkey,
        "partner_fee_total" / borsh.U64,
        "partner_fee_withdrawn" / borsh.U64,
        "partner_fee_percent" / borsh.F32,
        "ix" / create_stream_params.CreateStreamParams.layout,
        "ix_padding" / borsh.Bytes,
        "closed" / borsh.Bool,
        "current_pause_start" / borsh.U64,
        "pause_cumulative" / borsh.U64,
        "last_rate_change_time" / borsh.U64,
        "funds_unlocked_at_last_rate_change" / borsh.U64,
    )
    magic: int
    version: int
    created_at: int
    amount_withdrawn: int
    canceled_at: int
    end_time: int
    last_withdrawn_at: int
    sender: Pubkey
    sender_tokens: Pubkey
    recipient: Pubkey
    recipient_tokens: Pubkey
    mint: Pubkey
    escrow_tokens: Pubkey
    streamflow_treasury: Pubkey
    streamflow_treasury_tokens: Pubkey
    streamflow_fee_total: int
    streamflow_fee_withdrawn: int
    streamflow_fee_percent: float
    partner: Pubkey
    partner_tokens: Pubkey
    partner_fee_total: int
    partner_fee_withdrawn: int
    partner_fee_percent: float
    ix: create_stream_params.CreateStreamParams
    ix_padding: bytes
    closed: bool
    current_pause_start: int
    pause_cumulative: int
    last_rate_change_time: int
    funds_unlocked_at_last_rate_change: int

    @classmethod
    def from_decoded(cls, obj: Container) -> "StreamContract":
        return cls(
            magic=obj.magic,
            version=obj.version,
            created_at=obj.created_at,
            amount_withdrawn=obj.amount_withdrawn,
            canceled_at=obj.canceled_at,
            end_time=obj.end_time,
            last_withdrawn_at=obj.last_withdrawn_at,
            sender=obj.sender,
            sender_tokens=obj.sender_tokens,
            recipient=obj.recipient,
            recipient_tokens=obj.recipient_tokens,
            mint=obj.mint,
            escrow_tokens=obj.escrow_tokens,
            streamflow_treasury=obj.streamflow_treasury,
            streamflow_treasury_tokens=obj.streamflow_treasury_tokens,
            streamflow_fee_total=obj.streamflow_fee_total,
            streamflow_fee_withdrawn=obj.streamflow_fee_withdrawn,
            streamflow_fee_percent=obj.streamflow_fee_percent,
            partner=obj.partner,
            partner_tokens=obj.partner_tokens,
            partner_fee_total=obj.partner_fee_total,
            partner_fee_withdrawn=obj.partner_fee_withdrawn,
            partner_fee_percent=obj.partner_fee_percent,
            ix=create_stream_params.CreateStreamParams.from_decoded(obj.ix),
            ix_padding=obj.ix_padding,
            closed=obj.closed,
            current_pause_start=obj.current_pause_start,
            pause_cumulative=obj.pause_cumulative,
            last_rate_change_time=obj.last_rate_change_time,
            funds_unlocked_at_last_rate_change=obj.funds_unlocked_at_last_rate_change,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "magic": self.magic,
            "version": self.version,
            "created_at": self.created_at,
            "amount_withdrawn": self.amount_withdrawn,
            "canceled_at": self.canceled_at,
            "end_time": self.end_time,
            "last_withdrawn_at": self.last_withdrawn_at,
            "sender": self.sender,
            "sender_tokens": self.sender_tokens,
            "recipient": self.recipient,
            "recipient_tokens": self.recipient_tokens,
            "mint": self.mint,
            "escrow_tokens": self.escrow_tokens,
            "streamflow_treasury": self.streamflow_treasury,
            "streamflow_treasury_tokens": self.streamflow_treasury_tokens,
            "streamflow_fee_total": self.streamflow_fee_total,
            "streamflow_fee_withdrawn": self.streamflow_fee_withdrawn,
            "streamflow_fee_percent": self.streamflow_fee_percent,
            "partner": self.partner,
            "partner_tokens": self.partner_tokens,
            "partner_fee_total": self.partner_fee_total,
            "partner_fee_withdrawn": self.partner_fee_withdrawn,
            "partner_fee_percent": self.partner_fee_percent,
            "ix": self.ix.to_encodable(),
            "ix_padding": self.ix_padding,
            "closed": self.closed,
            "current_pause_start": self.current_pause_start,
            "pause_cumulative": self.pause_cumulative,
            "last_rate_change_time": self.last_rate_change_time,
            "funds_unlocked_at_last_rate_change": self.funds_unlocked_at_last_rate_change,
        }

    def to_json(self) -> StreamContractJSON:
        return {
            "magic": self.magic,
            "version": self.version,
            "created_at": self.created_at,
            "amount_withdrawn": self.amount_withdrawn,
            "canceled_at": self.canceled_at,
            "end_time": self.end_time,
            "last_withdrawn_at": self.last_withdrawn_at,
            "sender": str(self.sender),
            "sender_tokens": str(self.sender_tokens),
            "recipient": str(self.recipient),
            "recipient_tokens": str(self.recipient_tokens),
            "mint": str(self.mint),
            "escrow_tokens": str(self.escrow_tokens),
            "streamflow_treasury": str(self.streamflow_treasury),
            "streamflow_treasury_tokens": str(self.streamflow_treasury_tokens),
            "streamflow_fee_total": self.streamflow_fee_total,
            "streamflow_fee_withdrawn": self.streamflow_fee_withdrawn,
            "streamflow_fee_percent": self.streamflow_fee_percent,
            "partner": str(self.partner),
            "partner_tokens": str(self.partner_tokens),
            "partner_fee_total": self.partner_fee_total,
            "partner_fee_withdrawn": self.partner_fee_withdrawn,
            "partner_fee_percent": self.partner_fee_percent,
            "ix": self.ix.to_json(),
            "ix_padding": list(self.ix_padding),
            "closed": self.closed,
            "current_pause_start": self.current_pause_start,
            "pause_cumulative": self.pause_cumulative,
            "last_rate_change_time": self.last_rate_change_time,
            "funds_unlocked_at_last_rate_change": self.funds_unlocked_at_last_rate_change,
        }

    @classmethod
    def from_json(cls, obj: StreamContractJSON) -> "StreamContract":
        return cls(
            magic=obj["magic"],
            version=obj["version"],
            created_at=obj["created_at"],
            amount_withdrawn=obj["amount_withdrawn"],
            canceled_at=obj["canceled_at"],
            end_time=obj["end_time"],
            last_withdrawn_at=obj["last_withdrawn_at"],
            sender=Pubkey.from_string(obj["sender"]),
            sender_tokens=Pubkey.from_string(obj["sender_tokens"]),
            recipient=Pubkey.from_string(obj["recipient"]),
            recipient_tokens=Pubkey.from_string(obj["recipient_tokens"]),
            mint=Pubkey.from_string(obj["mint"]),
            escrow_tokens=Pubkey.from_string(obj["escrow_tokens"]),
            streamflow_treasury=Pubkey.from_string(obj["streamflow_treasury"]),
            streamflow_treasury_tokens=Pubkey.from_string(obj["streamflow_treasury_tokens"]),
            streamflow_fee_total=obj["streamflow_fee_total"],
            streamflow_fee_withdrawn=obj["streamflow_fee_withdrawn"],
            streamflow_fee_percent=obj["streamflow_fee_percent"],
            partner=Pubkey.from_string(obj["partner"]),
            partner_tokens=Pubkey.from_string(obj["partner_tokens"]),
            partner_fee_total=obj["partner_fee_total"],
            partner_fee_withdrawn=obj["partner_fee_withdrawn"],
            partner_fee_percent=obj["partner_fee_percent"],
            ix=create_stream_params.CreateStreamParams.from_json(obj["ix"]),
            ix_padding=bytes(obj["ix_padding"]),
            closed=obj["closed"],
            current_pause_start=obj["current_pause_start"],
            pause_cumulative=obj["pause_cumulative"],
            last_rate_change_time=obj["last_rate_change_time"],
            funds_unlocked_at_last_rate_change=obj["funds_unlocked_at_last_rate_change"],
        )
