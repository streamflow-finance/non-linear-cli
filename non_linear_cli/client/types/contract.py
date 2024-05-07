from __future__ import annotations
from . import (
    create_params,
)
import typing
from dataclasses import dataclass
from construct import Container
from solders.pubkey import Pubkey
from anchorpy.borsh_extension import BorshPubkey
import borsh_construct as borsh


class ContractJSON(typing.TypedDict):
    magic: int
    version: int
    sender: str
    sender_tokens: str
    recipient: str
    recipient_tokens: str
    mint: str
    stream: str
    end_time: int
    last_available: int
    last_release_update_time: int
    stream_canceled_at: int
    ix: create_params.CreateParamsJSON
    ix_padding: list[int]


@dataclass
class Contract:
    layout: typing.ClassVar = borsh.CStruct(
        "magic" / borsh.U64,
        "version" / borsh.U8,
        "sender" / BorshPubkey,
        "sender_tokens" / BorshPubkey,
        "recipient" / BorshPubkey,
        "recipient_tokens" / BorshPubkey,
        "mint" / BorshPubkey,
        "stream" / BorshPubkey,
        "end_time" / borsh.U64,
        "last_available" / borsh.U64,
        "last_release_update_time" / borsh.U64,
        "stream_canceled_at" / borsh.U64,
        "ix" / create_params.CreateParams.layout,
        "ix_padding" / borsh.Bytes,
    )
    magic: int
    version: int
    sender: Pubkey
    sender_tokens: Pubkey
    recipient: Pubkey
    recipient_tokens: Pubkey
    mint: Pubkey
    stream: Pubkey
    end_time: int
    last_available: int
    last_release_update_time: int
    stream_canceled_at: int
    ix: create_params.CreateParams
    ix_padding: bytes

    @classmethod
    def from_decoded(cls, obj: Container) -> "Contract":
        return cls(
            magic=obj.magic,
            version=obj.version,
            sender=obj.sender,
            sender_tokens=obj.sender_tokens,
            recipient=obj.recipient,
            recipient_tokens=obj.recipient_tokens,
            mint=obj.mint,
            stream=obj.stream,
            end_time=obj.end_time,
            last_available=obj.last_available,
            last_release_update_time=obj.last_release_update_time,
            stream_canceled_at=obj.stream_canceled_at,
            ix=create_params.CreateParams.from_decoded(obj.ix),
            ix_padding=obj.ix_padding,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "magic": self.magic,
            "version": self.version,
            "sender": self.sender,
            "sender_tokens": self.sender_tokens,
            "recipient": self.recipient,
            "recipient_tokens": self.recipient_tokens,
            "mint": self.mint,
            "stream": self.stream,
            "end_time": self.end_time,
            "last_available": self.last_available,
            "last_release_update_time": self.last_release_update_time,
            "stream_canceled_at": self.stream_canceled_at,
            "ix": self.ix.to_encodable(),
            "ix_padding": self.ix_padding,
        }

    def to_json(self) -> ContractJSON:
        return {
            "magic": self.magic,
            "version": self.version,
            "sender": str(self.sender),
            "sender_tokens": str(self.sender_tokens),
            "recipient": str(self.recipient),
            "recipient_tokens": str(self.recipient_tokens),
            "mint": str(self.mint),
            "stream": str(self.stream),
            "end_time": self.end_time,
            "last_available": self.last_available,
            "last_release_update_time": self.last_release_update_time,
            "stream_canceled_at": self.stream_canceled_at,
            "ix": self.ix.to_json(),
            "ix_padding": list(self.ix_padding),
        }

    @classmethod
    def from_json(cls, obj: ContractJSON) -> "Contract":
        return cls(
            magic=obj["magic"],
            version=obj["version"],
            sender=Pubkey.from_string(obj["sender"]),
            sender_tokens=Pubkey.from_string(obj["sender_tokens"]),
            recipient=Pubkey.from_string(obj["recipient"]),
            recipient_tokens=Pubkey.from_string(obj["recipient_tokens"]),
            mint=Pubkey.from_string(obj["mint"]),
            stream=Pubkey.from_string(obj["stream"]),
            end_time=obj["end_time"],
            last_available=obj["last_available"],
            last_release_update_time=obj["last_release_update_time"],
            stream_canceled_at=obj["stream_canceled_at"],
            ix=create_params.CreateParams.from_json(obj["ix"]),
            ix_padding=bytes(obj["ix_padding"]),
        )
