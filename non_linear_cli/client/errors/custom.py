import typing
from anchorpy.error import ProgramError


class AccountAlreadyInitialized(ProgramError):
    def __init__(self) -> None:
        super().__init__(
            6000,
            "An initialize instruction was sent to an account that has already been initialized",
        )

    code = 6000
    name = "AccountAlreadyInitialized"
    msg = "An initialize instruction was sent to an account that has already been initialized"


class AccountsNotWritable(ProgramError):
    def __init__(self) -> None:
        super().__init__(6001, "Accounts not writable!")

    code = 6001
    name = "AccountsNotWritable"
    msg = "Accounts not writable!"


class ArithmeticError(ProgramError):
    def __init__(self) -> None:
        super().__init__(6002, "Arithmetic error")

    code = 6002
    name = "ArithmeticError"
    msg = "Arithmetic error"


class InvalidEscrowAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6003, "Invalid escrow account")

    code = 6003
    name = "InvalidEscrowAccount"
    msg = "Invalid escrow account"


class InvalidMetadata(ProgramError):
    def __init__(self) -> None:
        super().__init__(6004, "Invalid Metadata!")

    code = 6004
    name = "InvalidMetadata"
    msg = "Invalid Metadata!"


class InvalidMetadataAccount(ProgramError):
    def __init__(self) -> None:
        super().__init__(6005, "Invalid metadata account")

    code = 6005
    name = "InvalidMetadataAccount"
    msg = "Invalid metadata account"


class InvalidMetadataSize(ProgramError):
    def __init__(self) -> None:
        super().__init__(6006, "Metadata account data must be 1104 bytes long")

    code = 6006
    name = "InvalidMetadataSize"
    msg = "Metadata account data must be 1104 bytes long"


class InvalidIncreaseRate(ProgramError):
    def __init__(self) -> None:
        super().__init__(6007, "Invalid increase rate, should be great than 1")

    code = 6007
    name = "InvalidIncreaseRate"
    msg = "Invalid increase rate, should be great than 1"


class InvalidPenaltyRate(ProgramError):
    def __init__(self) -> None:
        super().__init__(6008, "Invalid penalty rate, should be between 0 and 1")

    code = 6008
    name = "InvalidPenaltyRate"
    msg = "Invalid penalty rate, should be between 0 and 1"


class MetadataAccountMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(6009, "Provided accounts don't match the ones in contract.")

    code = 6009
    name = "MetadataAccountMismatch"
    msg = "Provided accounts don't match the ones in contract."


class MintMismatch(ProgramError):
    def __init__(self) -> None:
        super().__init__(6010, "Sender mint does not match accounts mint!")

    code = 6010
    name = "MintMismatch"
    msg = "Sender mint does not match accounts mint!"


class NotAssociated(ProgramError):
    def __init__(self) -> None:
        super().__init__(6011, "Provided account(s) is/are not valid associated token accounts.")

    code = 6011
    name = "NotAssociated"
    msg = "Provided account(s) is/are not valid associated token accounts."


class TransferNotAllowed(ProgramError):
    def __init__(self) -> None:
        super().__init__(6012, "Recipient not transferable for account")

    code = 6012
    name = "TransferNotAllowed"
    msg = "Recipient not transferable for account"


class UninitializedMetadata(ProgramError):
    def __init__(self) -> None:
        super().__init__(6013, "Metadata state account must be initialized")

    code = 6013
    name = "UninitializedMetadata"
    msg = "Metadata state account must be initialized"


class Unauthorized(ProgramError):
    def __init__(self) -> None:
        super().__init__(6014, "Authority does not have permission for this action")

    code = 6014
    name = "Unauthorized"
    msg = "Authority does not have permission for this action"


class AmountAlreadyUpdated(ProgramError):
    def __init__(self) -> None:
        super().__init__(6015, "Release amount has already been updated in this period")

    code = 6015
    name = "AmountAlreadyUpdated"
    msg = "Release amount has already been updated in this period"


class AllFundsUnlocked(ProgramError):
    def __init__(self) -> None:
        super().__init__(6016, "All funds are already unlocked")

    code = 6016
    name = "AllFundsUnlocked"
    msg = "All funds are already unlocked"


CustomError = typing.Union[
    AccountAlreadyInitialized,
    AccountsNotWritable,
    ArithmeticError,
    InvalidEscrowAccount,
    InvalidMetadata,
    InvalidMetadataAccount,
    InvalidMetadataSize,
    InvalidIncreaseRate,
    InvalidPenaltyRate,
    MetadataAccountMismatch,
    MintMismatch,
    NotAssociated,
    TransferNotAllowed,
    UninitializedMetadata,
    Unauthorized,
    AmountAlreadyUpdated,
    AllFundsUnlocked,
]
CUSTOM_ERROR_MAP: dict[int, CustomError] = {
    6000: AccountAlreadyInitialized(),
    6001: AccountsNotWritable(),
    6002: ArithmeticError(),
    6003: InvalidEscrowAccount(),
    6004: InvalidMetadata(),
    6005: InvalidMetadataAccount(),
    6006: InvalidMetadataSize(),
    6007: InvalidIncreaseRate(),
    6008: InvalidPenaltyRate(),
    6009: MetadataAccountMismatch(),
    6010: MintMismatch(),
    6011: NotAssociated(),
    6012: TransferNotAllowed(),
    6013: UninitializedMetadata(),
    6014: Unauthorized(),
    6015: AmountAlreadyUpdated(),
    6016: AllFundsUnlocked(),
}


def from_code(code: int) -> typing.Optional[CustomError]:
    maybe_err = CUSTOM_ERROR_MAP.get(code)
    if maybe_err is None:
        return None
    return maybe_err
