from __future__ import annotations
import typing
from dataclasses import dataclass
from construct import Container
import borsh_construct as borsh


class CreateParamsJSON(typing.TypedDict):
    start_time: int
    net_amount_deposited: int
    period: int
    amount_per_period: int
    cliff: int
    cliff_amount: int
    cancelable_by_sender: bool
    cancelable_by_recipient: bool
    automatic_withdrawal: bool
    transferable_by_sender: bool
    transferable_by_recipient: bool
    can_topup: bool
    stream_name: list[int]
    withdraw_frequency: int
    pausable: bool
    can_update_rate: bool
    increase_rate: int
    penalty_rate: int
    is_penalized: bool


@dataclass
class CreateParams:
    layout: typing.ClassVar = borsh.CStruct(
        "start_time" / borsh.U64,
        "net_amount_deposited" / borsh.U64,
        "period" / borsh.U64,
        "amount_per_period" / borsh.U64,
        "cliff" / borsh.U64,
        "cliff_amount" / borsh.U64,
        "cancelable_by_sender" / borsh.Bool,
        "cancelable_by_recipient" / borsh.Bool,
        "automatic_withdrawal" / borsh.Bool,
        "transferable_by_sender" / borsh.Bool,
        "transferable_by_recipient" / borsh.Bool,
        "can_topup" / borsh.Bool,
        "stream_name" / borsh.U8[64],
        "withdraw_frequency" / borsh.U64,
        "pausable" / borsh.Bool,
        "can_update_rate" / borsh.Bool,
        "increase_rate" / borsh.U32,
        "penalty_rate" / borsh.U32,
        "is_penalized" / borsh.Bool,
    )
    start_time: int
    net_amount_deposited: int
    period: int
    amount_per_period: int
    cliff: int
    cliff_amount: int
    cancelable_by_sender: bool
    cancelable_by_recipient: bool
    automatic_withdrawal: bool
    transferable_by_sender: bool
    transferable_by_recipient: bool
    can_topup: bool
    stream_name: list[int]
    withdraw_frequency: int
    pausable: bool
    can_update_rate: bool
    increase_rate: int
    penalty_rate: int
    is_penalized: bool

    @classmethod
    def from_decoded(cls, obj: Container) -> "CreateParams":
        return cls(
            start_time=obj.start_time,
            net_amount_deposited=obj.net_amount_deposited,
            period=obj.period,
            amount_per_period=obj.amount_per_period,
            cliff=obj.cliff,
            cliff_amount=obj.cliff_amount,
            cancelable_by_sender=obj.cancelable_by_sender,
            cancelable_by_recipient=obj.cancelable_by_recipient,
            automatic_withdrawal=obj.automatic_withdrawal,
            transferable_by_sender=obj.transferable_by_sender,
            transferable_by_recipient=obj.transferable_by_recipient,
            can_topup=obj.can_topup,
            stream_name=obj.stream_name,
            withdraw_frequency=obj.withdraw_frequency,
            pausable=obj.pausable,
            can_update_rate=obj.can_update_rate,
            increase_rate=obj.increase_rate,
            penalty_rate=obj.penalty_rate,
            is_penalized=obj.is_penalized,
        )

    def to_encodable(self) -> dict[str, typing.Any]:
        return {
            "start_time": self.start_time,
            "net_amount_deposited": self.net_amount_deposited,
            "period": self.period,
            "amount_per_period": self.amount_per_period,
            "cliff": self.cliff,
            "cliff_amount": self.cliff_amount,
            "cancelable_by_sender": self.cancelable_by_sender,
            "cancelable_by_recipient": self.cancelable_by_recipient,
            "automatic_withdrawal": self.automatic_withdrawal,
            "transferable_by_sender": self.transferable_by_sender,
            "transferable_by_recipient": self.transferable_by_recipient,
            "can_topup": self.can_topup,
            "stream_name": self.stream_name,
            "withdraw_frequency": self.withdraw_frequency,
            "pausable": self.pausable,
            "can_update_rate": self.can_update_rate,
            "increase_rate": self.increase_rate,
            "penalty_rate": self.penalty_rate,
            "is_penalized": self.is_penalized,
        }

    def to_json(self) -> CreateParamsJSON:
        return {
            "start_time": self.start_time,
            "net_amount_deposited": self.net_amount_deposited,
            "period": self.period,
            "amount_per_period": self.amount_per_period,
            "cliff": self.cliff,
            "cliff_amount": self.cliff_amount,
            "cancelable_by_sender": self.cancelable_by_sender,
            "cancelable_by_recipient": self.cancelable_by_recipient,
            "automatic_withdrawal": self.automatic_withdrawal,
            "transferable_by_sender": self.transferable_by_sender,
            "transferable_by_recipient": self.transferable_by_recipient,
            "can_topup": self.can_topup,
            "stream_name": self.stream_name,
            "withdraw_frequency": self.withdraw_frequency,
            "pausable": self.pausable,
            "can_update_rate": self.can_update_rate,
            "increase_rate": self.increase_rate,
            "penalty_rate": self.penalty_rate,
            "is_penalized": self.is_penalized,
        }

    @classmethod
    def from_json(cls, obj: CreateParamsJSON) -> "CreateParams":
        return cls(
            start_time=obj["start_time"],
            net_amount_deposited=obj["net_amount_deposited"],
            period=obj["period"],
            amount_per_period=obj["amount_per_period"],
            cliff=obj["cliff"],
            cliff_amount=obj["cliff_amount"],
            cancelable_by_sender=obj["cancelable_by_sender"],
            cancelable_by_recipient=obj["cancelable_by_recipient"],
            automatic_withdrawal=obj["automatic_withdrawal"],
            transferable_by_sender=obj["transferable_by_sender"],
            transferable_by_recipient=obj["transferable_by_recipient"],
            can_topup=obj["can_topup"],
            stream_name=obj["stream_name"],
            withdraw_frequency=obj["withdraw_frequency"],
            pausable=obj["pausable"],
            can_update_rate=obj["can_update_rate"],
            increase_rate=obj["increase_rate"],
            penalty_rate=obj["penalty_rate"],
            is_penalized=obj["is_penalized"],
        )
