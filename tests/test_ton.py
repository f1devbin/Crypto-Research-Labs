from crl.data import ton as T
from crl.data.everscale import addr_id

GATE = T.GATE_TON.upper()
ALICE = "0:0AF0DCD699E4F194F5E2ABC0CFC2AE974ED6652A25B7BD4E75358357BADDA510"
ALICE_FRIENDLY = "UQAK8NzWmeTxlPXiq8DPwq6XTtZlKiW3vU51NYNXut2lEChk"
BOB = "0:" + "B" * 64


def msg(src, value, ts=1700000000, bounced=False, h=None):
    return {"source": src, "destination": GATE, "value": str(int(value * 1e9)), "bounced": bounced,
            "created_at": str(ts), "created_lt": "1", "hash": h or f"{src}{ts}{value}"}


def test_user_friendly_and_raw_addresses_match():
    assert T.raw(ALICE_FRIENDLY) == T.raw(ALICE) == ALICE.lower()


def test_parse_keeps_plain_deposits_by_sender_and_drops_the_rest():
    msgs = [msg(BOB, 50), msg(BOB, 0.5), msg(BOB, 80, bounced=True), msg(ALICE, 30),
            msg(T.GATE_TON, 1000), msg(None, 20)]
    df = T.parse(msgs, T.GATE_TON, min_value=1.0, exclude={ALICE_FRIENDLY})
    assert list(df["wallet"]) == [addr_id(T.raw(BOB))] and list(df["value"]) == [50.0]
    assert set(df.columns) == {"ts", "wallet", "deposit", "value", "first_sweep_ts"} and (df["first_sweep_ts"] == 0).all()
    assert df["deposit"].iloc[0] == addr_id(T.GATE_TON) and BOB.lower() not in df.to_csv()
