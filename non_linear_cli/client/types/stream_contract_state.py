from __future__ import annotations
import typing
from dataclasses import dataclass
from anchorpy.borsh_extension import EnumForCodegen
import borsh_construct as borsh


class ScheduledJSON(typing.TypedDict):
    kind: typing.Literal["Scheduled"]


class PausedJSON(typing.TypedDict):
    kind: typing.Literal["Paused"]


class ClosedJSON(typing.TypedDict):
    kind: typing.Literal["Closed"]


@dataclass
class Scheduled:
    discriminator: typing.ClassVar = 0
    kind: typing.ClassVar = "Scheduled"

    @classmethod
    def to_json(cls) -> ScheduledJSON:
        return ScheduledJSON(
            kind="Scheduled",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Scheduled": {},
        }


@dataclass
class Paused:
    discriminator: typing.ClassVar = 1
    kind: typing.ClassVar = "Paused"

    @classmethod
    def to_json(cls) -> PausedJSON:
        return PausedJSON(
            kind="Paused",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Paused": {},
        }


@dataclass
class Closed:
    discriminator: typing.ClassVar = 2
    kind: typing.ClassVar = "Closed"

    @classmethod
    def to_json(cls) -> ClosedJSON:
        return ClosedJSON(
            kind="Closed",
        )

    @classmethod
    def to_encodable(cls) -> dict:
        return {
            "Closed": {},
        }


StreamContractStateKind = typing.Union[Scheduled, Paused, Closed]
StreamContractStateJSON = typing.Union[ScheduledJSON, PausedJSON, ClosedJSON]


def from_decoded(obj: dict) -> StreamContractStateKind:
    if not isinstance(obj, dict):
        raise ValueError("Invalid enum object")
    if "Scheduled" in obj:
        return Scheduled()
    if "Paused" in obj:
        return Paused()
    if "Closed" in obj:
        return Closed()
    raise ValueError("Invalid enum object")


def from_json(obj: StreamContractStateJSON) -> StreamContractStateKind:
    if obj["kind"] == "Scheduled":
        return Scheduled()
    if obj["kind"] == "Paused":
        return Paused()
    if obj["kind"] == "Closed":
        return Closed()
    kind = obj["kind"]
    raise ValueError(f"Unrecognized enum kind: {kind}")


layout = EnumForCodegen(
    "Scheduled" / borsh.CStruct(),
    "Paused" / borsh.CStruct(),
    "Closed" / borsh.CStruct(),
)
