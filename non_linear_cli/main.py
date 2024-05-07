import hashlib
import os
from decimal import Decimal, InvalidOperation

import click
from borsh_construct import U64, CStruct
from click import Context
from solana.rpc.api import Client
from solana.transaction import Transaction
from solders.compute_budget import set_compute_unit_limit, set_compute_unit_price
from solders.instruction import AccountMeta, Instruction
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.rpc.responses import RpcConfirmedTransactionStatusWithSignature
from solders.signature import Signature
from spl.token.client import Token
from spl.token.constants import ASSOCIATED_TOKEN_PROGRAM_ID, TOKEN_PROGRAM_ID

from .client.instructions import (
    CancelAccounts,
    CreateAccounts,
    CreateArgs,
)
from .client.instructions import (
    cancel as cancel_instruction,
)
from .client.instructions import (
    create as create_instruction,
)
from .client.types import CreateParams

withdraw_stream_struct = CStruct(
    "amount" / U64,
)

NETWORKS = {True: "https://api.devnet.solana.com", False: "https://api.mainnet-beta.solana.com"}
STREAMFLOW_TREASURY = Pubkey.from_string("5SEpbdjFK5FxwTvfsGMXVQTD2v4M2c5tyRTxhdsPkgDw")
WITHDRAWOR = Pubkey.from_string("wdrwhnCv4pzW8beKsbPa4S2UDZrXenjg16KJdKSpb5u")
FEE_ORACLE = Pubkey.from_string("B743wFVk2pCYhV91cn287e1xY7f1vt4gdY48hhNiuQmT")
RATE_PRECISION = 10**9


def build_create_params(
    net_amount_deposited: int,
    period: int,
    amount_per_period: int,
    name: str,
    increase_rate: Decimal,
    penalty_rate: Decimal,
    is_penalized: bool,
) -> CreateParams:
    encoded_name = name.encode()
    name_byte_array = bytearray(64)
    name_byte_array[0 : len(encoded_name)] = encoded_name
    return CreateParams(
        start_time=0,
        net_amount_deposited=net_amount_deposited,
        period=period,
        amount_per_period=amount_per_period,
        cliff=0,
        cliff_amount=0,
        cancelable_by_sender=True,
        cancelable_by_recipient=True,
        automatic_withdrawal=False,
        transferable_by_sender=False,
        transferable_by_recipient=False,
        can_topup=False,
        stream_name=list(name_byte_array),
        withdraw_frequency=0,
        pausable=False,
        can_update_rate=False,
        increase_rate=int(increase_rate * RATE_PRECISION),
        penalty_rate=int(penalty_rate * RATE_PRECISION),
        is_penalized=is_penalized,
    )


def validate_decimal(ctx, param, value: str) -> Decimal:
    try:
        return Decimal(value)
    except InvalidOperation as e:
        raise click.BadParameter("Not a decimal value") from e


def validate_pubkey(ctx, param, value: str | None) -> Pubkey:
    try:
        return Pubkey.from_string(value)
    except Exception as e:
        raise click.BadParameter("Invalid pubkey") from e


def validate_pubkey_optional(ctx, param, value: str | None) -> Pubkey | None:
    if value is None:
        return value
    return validate_pubkey(ctx, param, value)


def validate_private_keys_file(ctx, param, value: str) -> Keypair:
    if not os.path.exists(value):
        try:
            return Keypair.from_base58_string(value)
        except Exception as e:
            raise click.BadParameter("Invalid key or keys file does not exist") from e
    with open(value) as r:
        try:
            return Keypair.from_json(r.read().strip())
        except Exception as e:
            raise click.BadParameter("Invalid keys file") from e


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--devnet", is_flag=True, show_default=True, default=False, help="Use devnet")
@click.option("--rpc", help="Use non default RPC Pool")
@click.option(
    "--program-id",
    default="strn1sS2qKxs7SgJ1xx4trPKSWdqxFim6HFG9ETXiCL",
    callback=validate_pubkey,
    help="Proxy program id",
)
@click.option(
    "--streamflow-program-id",
    callback=validate_pubkey_optional,
    help="Streamflow Vesting program id, takes precedence over `--devnet` flag",
)
@click.option(
    "--priority-fee",
    default=0,
    help="Priority fee used in transactions, set in micro-lamports as price per CU",
)
@click.pass_context
def cli(
    ctx: Context,
    devnet: bool,
    rpc: str | None,
    program_id: Pubkey,
    streamflow_program_id: Pubkey | None,
    priority_fee: int,
):
    ctx.ensure_object(dict)
    if rpc:
        ctx.obj["client"] = Client(rpc)
    else:
        ctx.obj["client"] = Client(NETWORKS[devnet])
    ctx.obj["program"] = program_id
    if streamflow_program_id:
        ctx.obj["streamflow_program"] = streamflow_program_id
    elif devnet:
        ctx.obj["streamflow_program"] = Pubkey.from_string("HqDGZjaVRXJ9MGRQEw7qDc2rAr6iH1n1kAQdCZaCMfMZ")
    else:
        ctx.obj["streamflow_program"] = Pubkey.from_string("strmRqUCoQUgGUan5YhzUZa6KqdzwX5L6FpUxfmKg5m")
    ctx.obj["compute_price"] = priority_fee


@cli.command()
@click.argument("recipient", callback=validate_pubkey)
@click.option(
    "-m",
    "--mint",
    show_default=True,
    default="Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
    callback=validate_pubkey,
    help="Mint of the token to vest",
)
@click.option("-n", "--net-amount", show_default=True, default=1000000, help="Total amount of tokens to vest")
@click.option("-p", "--period", show_default=True, default=30, help="Release period, release A amount every P seconds")
@click.option(
    "-a",
    "--amount-per-period",
    show_default=True,
    default=100000,
    help="Release amount, every P seconds release A amount",
)
@click.option(
    "-ir",
    "--increase-rate",
    show_default=True,
    default=Decimal("1.5"),
    callback=validate_decimal,
    help="Increase rate, A amount will be increased by it every P seconds",
)
@click.option(
    "-pr",
    "--penalty-rate",
    show_default=True,
    default=Decimal("1"),
    callback=validate_decimal,
    help="Penalty rate, enacted when recipient withdraws between periods",
)
@click.option("--penalized", is_flag=True, show_default=True, default=False, help="Penalize for claims")
@click.option("--name", show_default=True, default="", help="Name of a vesting stream")
@click.option(
    "--key",
    "sender",
    show_default=True,
    default="sender.json",
    callback=validate_private_keys_file,
    help="Path to the keys.json file for the stream sender or base58 encoded private key",
)
@click.pass_context
def create(
    ctx: Context,
    recipient: Pubkey,
    net_amount: int,
    mint: Pubkey,
    period: int,
    amount_per_period: int,
    increase_rate: Decimal,
    penalty_rate: Decimal,
    penalized: bool,
    name: str,
    sender: Keypair,
):
    stream_signer = Keypair()
    stream_metadata = stream_signer.pubkey()
    program = ctx.obj["program"]
    streamflow_program = ctx.obj["streamflow_program"]
    proxy_metadata, _ = Pubkey.find_program_address([bytes(stream_metadata)], program)
    escrow_tokens, _ = Pubkey.find_program_address([b"strm", bytes(stream_metadata)], streamflow_program)
    proxy_tokens, _ = Pubkey.find_program_address(
        [bytes(proxy_metadata), bytes(TOKEN_PROGRAM_ID), bytes(mint)], ASSOCIATED_TOKEN_PROGRAM_ID
    )
    sender_tokens, _ = Pubkey.find_program_address(
        [bytes(sender.pubkey()), bytes(TOKEN_PROGRAM_ID), bytes(mint)], ASSOCIATED_TOKEN_PROGRAM_ID
    )
    recipient_tokens, _ = Pubkey.find_program_address(
        [bytes(recipient), bytes(TOKEN_PROGRAM_ID), bytes(mint)], ASSOCIATED_TOKEN_PROGRAM_ID
    )
    args = CreateArgs(
        ix=build_create_params(net_amount, period, amount_per_period, name, increase_rate, penalty_rate, penalized)
    )
    accounts = CreateAccounts(
        sender=sender.pubkey(),
        sender_tokens=sender_tokens,
        recipient=recipient,
        recipient_tokens=recipient_tokens,
        proxy_metadata=proxy_metadata,
        proxy_tokens=proxy_tokens,
        stream_metadata=stream_metadata,
        escrow_tokens=escrow_tokens,
        withdrawor=WITHDRAWOR,
        partner=sender.pubkey(),
        partner_tokens=sender_tokens,
        mint=mint,
        fee_oracle=FEE_ORACLE,
        streamflow_program=streamflow_program,
    )
    tx = Transaction(
        fee_payer=sender.pubkey(),
        instructions=[
            set_compute_unit_limit(240_000),
            set_compute_unit_price(ctx.obj["compute_price"]),
            create_instruction(args, accounts, program),
        ],
    )
    client: Client = ctx.obj["client"]
    token_client = Token(client, mint, TOKEN_PROGRAM_ID, sender)
    if not token_client.get_accounts_by_owner(STREAMFLOW_TREASURY).value:
        click.echo("Initializing Treasury token account")
        token_client.create_associated_token_account(STREAMFLOW_TREASURY)
    if not token_client.get_accounts_by_owner(recipient).value:
        click.echo("Initializing Recipient token account")
        token_client.create_associated_token_account(recipient)
    resp = client.send_transaction(tx, stream_signer, sender)
    click.echo(f"Proxy Account id: {str(proxy_metadata)}")
    click.echo(f"Vesting Stream id: {str(stream_metadata)}")
    click.echo(f"Tx: {resp.value}")


def get_first_signature(client: Client, stream_id: Pubkey) -> Signature | None:
    last_tx_sig: Signature | None = None
    tx_signatures: list[RpcConfirmedTransactionStatusWithSignature] = []
    while not tx_signatures or len(tx_signatures) >= 1000:
        if tx_signatures:
            last_tx_sig = tx_signatures[-1].signature
        res = client.get_signatures_for_address(stream_id, before=last_tx_sig, limit=1000)
        tx_signatures = res.value
        if not tx_signatures:
            return last_tx_sig
    return tx_signatures[-1].signature


@cli.command()
@click.option(
    "-s",
    "--stream-id",
    callback=validate_pubkey,
    help="Vesting Stream id",
)
@click.option("-a", "--amount", show_default=True, default=18446744073709551615)
@click.option(
    "--key",
    "authority",
    show_default=True,
    default="recipient.json",
    callback=validate_private_keys_file,
    help="Path to the keys.json file for withdrawal authority or base58 encoded private key",
)
@click.pass_context
def withdraw(
    ctx: Context,
    stream_id: Pubkey,
    amount: int,
    authority: Keypair,
):
    client: Client = ctx.obj["client"]
    streamflow_program = ctx.obj["streamflow_program"]
    sig = get_first_signature(client, stream_id)
    if not sig:
        raise click.ClickException(f"Could not find initial tx for stream {str(stream_id)}")
    tx = client.get_transaction(sig).value.transaction.transaction
    accounts = list(tx.message.instructions[-1].accounts)
    account_keys = list(tx.message.account_keys)
    sender = account_keys[accounts[0]]
    recipient = account_keys[accounts[2]]
    mint = account_keys[accounts[11]]
    stream_id = account_keys[accounts[6]]
    escrow_tokens, _ = Pubkey.find_program_address([b"strm", bytes(stream_id)], streamflow_program)
    sender_tokens, _ = Pubkey.find_program_address(
        [bytes(sender), bytes(TOKEN_PROGRAM_ID), bytes(mint)], ASSOCIATED_TOKEN_PROGRAM_ID
    )
    recipient_tokens, _ = Pubkey.find_program_address(
        [bytes(recipient), bytes(TOKEN_PROGRAM_ID), bytes(mint)], ASSOCIATED_TOKEN_PROGRAM_ID
    )
    streamflow_treasury_tokens, _ = Pubkey.find_program_address(
        [bytes(STREAMFLOW_TREASURY), bytes(TOKEN_PROGRAM_ID), bytes(mint)], ASSOCIATED_TOKEN_PROGRAM_ID
    )
    args = withdraw_stream_struct.build({"amount": amount})
    ix_id = hashlib.sha256(b"global:withdraw").digest()[:8]
    ix = Instruction(
        program_id=streamflow_program,
        data=bytes(ix_id) + bytes(args) + bytes(10),
        accounts=[
            AccountMeta(authority.pubkey(), True, True),
            AccountMeta(recipient, False, True),
            AccountMeta(recipient_tokens, False, True),
            AccountMeta(stream_id, False, True),
            AccountMeta(escrow_tokens, False, True),
            AccountMeta(STREAMFLOW_TREASURY, False, True),
            AccountMeta(streamflow_treasury_tokens, False, True),
            AccountMeta(sender, False, True),
            AccountMeta(sender_tokens, False, True),
            AccountMeta(mint, False, False),
            AccountMeta(TOKEN_PROGRAM_ID, False, False),
        ],
    )
    tx = Transaction(
        fee_payer=authority.pubkey(),
        instructions=[
            set_compute_unit_price(ctx.obj["compute_price"]),
            ix,
        ],
    )
    resp = client.send_transaction(tx, authority)
    click.echo(f"Tx: {resp.value}")


@cli.command()
@click.option(
    "-s",
    "--stream-id",
    callback=validate_pubkey,
    help="Vesting Stream id",
)
@click.option(
    "--key",
    "authority",
    show_default=True,
    default="sender.json",
    callback=validate_private_keys_file,
    help="Path to the keys.json file for cancel authority or base58 encoded private key",
)
@click.pass_context
def cancel(
    ctx: Context,
    stream_id: Pubkey,
    authority: Keypair,
):
    client: Client = ctx.obj["client"]
    program = ctx.obj["program"]
    streamflow_program = ctx.obj["streamflow_program"]
    sig = get_first_signature(client, stream_id)
    if not sig:
        raise click.ClickException(f"Could not find initial tx for stream {str(stream_id)}")
    tx = client.get_transaction(sig).value.transaction.transaction
    accounts = list(tx.message.instructions[-1].accounts)
    account_keys = list(tx.message.account_keys)
    sender = account_keys[accounts[0]]
    recipient = account_keys[accounts[2]]
    partner = account_keys[accounts[9]]
    mint = account_keys[accounts[11]]
    stream_id = account_keys[accounts[6]]
    proxy_id = account_keys[accounts[4]]
    stream_program = account_keys[accounts[14]]
    escrow_tokens, _ = Pubkey.find_program_address([b"strm", bytes(stream_id)], streamflow_program)
    proxy_tokens, _ = Pubkey.find_program_address(
        [bytes(proxy_id), bytes(TOKEN_PROGRAM_ID), bytes(mint)], ASSOCIATED_TOKEN_PROGRAM_ID
    )
    sender_tokens, _ = Pubkey.find_program_address(
        [bytes(sender), bytes(TOKEN_PROGRAM_ID), bytes(mint)], ASSOCIATED_TOKEN_PROGRAM_ID
    )
    recipient_tokens, _ = Pubkey.find_program_address(
        [bytes(recipient), bytes(TOKEN_PROGRAM_ID), bytes(mint)], ASSOCIATED_TOKEN_PROGRAM_ID
    )
    partner_tokens, _ = Pubkey.find_program_address(
        [bytes(partner), bytes(TOKEN_PROGRAM_ID), bytes(mint)], ASSOCIATED_TOKEN_PROGRAM_ID
    )
    streamflow_treasury_tokens, _ = Pubkey.find_program_address(
        [bytes(STREAMFLOW_TREASURY), bytes(TOKEN_PROGRAM_ID), bytes(mint)], ASSOCIATED_TOKEN_PROGRAM_ID
    )
    accounts = CancelAccounts(
        sender=authority.pubkey(),
        sender_tokens=sender_tokens,
        recipient=recipient,
        recipient_tokens=recipient_tokens,
        proxy_metadata=proxy_id,
        proxy_tokens=proxy_tokens,
        stream_metadata=stream_id,
        escrow_tokens=escrow_tokens,
        streamflow_treasury=STREAMFLOW_TREASURY,
        streamflow_treasury_tokens=streamflow_treasury_tokens,
        partner=partner,
        partner_tokens=partner_tokens,
        mint=mint,
        streamflow_program=stream_program,
    )
    tx = Transaction(
        fee_payer=authority.pubkey(),
        instructions=[
            set_compute_unit_price(ctx.obj["compute_price"]),
            cancel_instruction(accounts, program),
        ],
    )
    resp = client.send_transaction(tx, authority)
    click.echo(f"Tx: {resp.value}")


def main():
    cli()


if __name__ == "__main__":
    main()
