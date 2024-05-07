# Non-Linear vesting Proxy account

Wrapper program that allows to create a Vesting stream with non-linear vesting support (recipient gets rewarded for not claiming a stream);

## Penalized Vesting

The way it works is:

1. Sender calls `create` method of the program, passes all parameters needed for vesting stream creation along with `increase_rate` and `penalty_rate`.
2. Program creates a proxy account and creates a vesting stream with the proxy account as sender. It's needed because only stream sender can update release amount for the stream.
3. A separate worker every release period calls `update_release` method of the program.
4. Program checks how many funds are released (minus withdrawn) to the recipient.
5. Program calculates at what step of non-linear vesting recipient should be with this amount of released funds.
6. Program sets release amount according to the step that recipient is at +1.

With this logic if recipient claims, released amount gets decreased (we can also increase their punishment by applying `penalty_rate` to the released amount), so we will decrease release amount. If user does not withdraw, release amount is increased.

Limitations:
- transfer, topup, pause, cliff is not available (basically only cancellation of the stream is possible);
- auto-claim is not possible as sender is a proxy account;

Example Contract is https://explorer.solana.com/address/DCiRMRzCvd8wqJF3SdJNNe2QRWR77ndQ4ByJCMjx1o4g?cluster=devnet:
- initial release amount of `100000` with increase rate of `1.5`;
- second transaction updates release to `150000`; 
- third transaction updates release to `225000`; 
- fourth transaction updates release to `337500`; 
- there no fifth transaction, because it happens before the last unlock period, there is no need to update release amount anymore given user has not withdrawn;

## Non-Penalized Vesting

It's also possible to create a Proxy Account with `penalized` flag off, this way recipient won't be penalized for claiming.
Each unlock period their `amount_per_period` will be increased. 
As `increase_rate` supports value of less than `1`, it can be used to set up a vesting with a decreased rate.

Example proxy account https://explorer.solana.com/address/BRFdc4RzAebs5U1UNqe3MvcxLXQpV294TCsjQTVRNwns?cluster=devnet:
- initial release amount of `100000` with increase rate of `0.9`;
- second transaction updates release to `90000`;
- third transaction updates release to `81000`;
- fourth transaction updates release to `72900`;

# CLI

There is a cli script that requires to have [poetry](https://python-poetry.org/docs/#installation) and python 3.11 to be installed on your machine. Then you can install it with command
```poetry install```

And run the script with

```poetry run non_linear_cli -h```

```poetry run non_linear_cli --devnet create```

Or you cna use a pre-built binary (with pyinstaller) from `dist` directory like so 

```./dist/non_linear_cli -h```

Works the same as with poetry bit without a need to install dependencies

## Parameters on create

```
  -m, --mint TEXT                 Mint of the token to vest  [default: Es9vMFr
                                  zaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB]
  -n, --net-amount INTEGER        Total amount of tokens to vest  [default:
                                  1000000]
  -p, --period INTEGER            Release period, release A amount every P
                                  seconds  [default: 30]
  -a, --amount-per-period INTEGER
                                  Release amount, every P seconds release A
                                  amount  [default: 100000]
  -ir, --increase-rate TEXT       Increase rate, A amount will be increased by
                                  it every P seconds  [default: 1.5]
  -pr, --penalty-rate TEXT        Penalty rate, enacted when recipient
                                  withdraws between periods  [default: 1]
  --penalized                     Penalize for claims
  --name TEXT                     Name of a vesting stream
  --key TEXT                      Path to the keys.json file for the stream
                                  sender or base58 encoded private key
                                  [default: sender.json]
```

### Notes

- `-n, --net-amount` and `-a, --amount-per-period` are set in Raw tokens amount, should include token decimals, i.e. if your token has 9 decimals and you want to vest 10 tokens, you need to pass `10000000000` as net amount;
- `-ir, --increase-rate` is the rate by which `amount_per_period` will be multiplied every `period`, to decrease the amount each period it should be less than 1;

## Example commands

Penalized with increasing rate:
```bash
poetry run non_linear_cli --devnet create \
-m 4r64XjgR6P6KaSwhkvmp1Ye1dZ7YPdFX1Z84e5jZY4nk \
-n 500000 \
-p 60 \
-a 100000 \
-ir 1.5 \
--name "Test Penalized" \
--key authority.key \
--penalized \
4vnGXnpbYBM5EzgKDvNHiGooojyxPFYn9xA4SaFYMpbb
```

Non-Penalized with decreasing rate:
```bash
poetry run non_linear_cli --devnet create \
-m 4r64XjgR6P6KaSwhkvmp1Ye1dZ7YPdFX1Z84e5jZY4nk \
-n 500000 \
-p 60 \
-a 100000 \
-ir 0.9 \
--name "Test Non-Penalized" \
--key authority.key \
4vnGXnpbYBM5EzgKDvNHiGooojyxPFYn9xA4SaFYMpbb
```
