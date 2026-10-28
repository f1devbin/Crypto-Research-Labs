"""Command line: `crl <command>`. Every scheduled workflow is one command."""
import argparse
import logging
import sys

from crl import registry


def _registry_check(_args) -> int:
    hyps = registry.load_all()
    bad = 0
    ids = [h.id for h in hyps]
    for dup in {i for i in ids if ids.count(i) > 1}:
        print(f"✗ duplicate id {dup}")
        bad += 1
    for h in hyps:
        errs = registry.validate(h) + [f"same test as {d}" for d in registry.duplicates(h, hyps)]
        print(f"{'✗' if errs else '✓'} {h.get('id', h.path.name)} [{h.get('status')}] {h.get('title', '')}")
        for e in errs:
            print(f"    - {e}")
        bad += bool(errs)
    print(f"\n{len(hyps)} hypotheses, {bad} with problems")
    return 1 if bad else 0


def _registry_register(args) -> int:
    for h in registry.load_all():
        if h.id in args.ids:
            registry.register(h)
            print(f"registered {h.id}: sha256 {h['prereg_sha256'][:16]}…")
    return 0


def _registry_list(_args) -> int:
    for h in registry.load_all():
        print(f"{h.id:7} {h['status']:10} {h['family']:8} {h['title']}")
    return 0


def _data(args) -> int:
    if args.action == "everscale":
        from crl.data import everscale
        return everscale.main()
    from crl.agents import data_steward
    return data_steward.main()


def _run(args) -> int:
    from crl.agents import runner
    return runner.main(args.ids or None, args.force)


def _watch(_args) -> int:
    from crl.agents import regime_watch
    return regime_watch.main()


def _propose(args) -> int:
    from crl.llm import proposer
    return proposer.main(args.n)


def _digest(_args) -> int:
    from crl.llm import digest
    return digest.main()


def _notify_test(_args) -> int:
    from crl import notify
    ok = notify.telegram(f"🔬 Crypto Research Labs: {notify.a('t_test')} ({notify.lang()}).\n"
                         f"{notify.a('test_body')}\n{notify.site_url()}")
    print("sent" if ok else "NOT sent: check TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID and press /start in the bot")
    return 0 if ok else 1


def _scan(_args) -> int:
    from crl import scan
    return scan.main()


def _forecast(_args) -> int:
    from crl.engine import forecast
    res = forecast.publish()
    print(res)
    return 0 if res["status"] in ("published", "already published") else 1


def _site(_args) -> int:
    from crl import site
    return site.main()


def main(argv=None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    ap = argparse.ArgumentParser(prog="crl", description="Crypto Research Labs")
    sub = ap.add_subparsers(dest="cmd", required=True)

    reg = sub.add_parser("registry", help="hypothesis registry")
    rsub = reg.add_subparsers(dest="action", required=True)
    rsub.add_parser("check", help="validate every hypothesis file").set_defaults(fn=_registry_check)
    rsub.add_parser("list", help="list hypotheses").set_defaults(fn=_registry_list)
    r = rsub.add_parser("register", help="lock draft specs (sha256) so they can be tested")
    r.add_argument("ids", nargs="+")
    r.set_defaults(fn=_registry_register)

    d = sub.add_parser("data", help="data steward: refresh cache + integrity checks")
    d.add_argument("action", choices=["refresh", "everscale"],
                   help="refresh: prices and features; everscale: Gate.io EVER deposits for H-032 (slow)")
    d.set_defaults(fn=_data)

    r = sub.add_parser("run", help="run due hypotheses (or the given ids)")
    r.add_argument("ids", nargs="*")
    r.add_argument("--force", action="store_true", help="run even if not due")
    r.set_defaults(fn=_run)

    sub.add_parser("watch", help="regime watch").set_defaults(fn=_watch)

    p = sub.add_parser("propose", help="LLM drafts new hypotheses (needs ANTHROPIC_API_KEY)")
    p.add_argument("-n", type=int, default=3)
    p.set_defaults(fn=_propose)

    sub.add_parser("digest", help="weekly digest").set_defaults(fn=_digest)
    sub.add_parser("notify-test", help="send a test Telegram message").set_defaults(fn=_notify_test)
    sub.add_parser("scan", help="coverage scan: every tested rule on every coin (exploratory)").set_defaults(fn=_scan)
    sub.add_parser("site", help="build the static dashboard into _site/").set_defaults(fn=_site)
    sub.add_parser("forecast", help="publish today's model forecasts (H-029/H-030 log)").set_defaults(fn=_forecast)

    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
