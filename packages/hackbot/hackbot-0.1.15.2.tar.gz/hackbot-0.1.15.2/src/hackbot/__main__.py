from hackbot.commands import get_args, hackbot_run
from hackbot.logging import setup_loguru


def _run():
    setup_loguru()
    args = get_args()
    if args.command == "run":
        exit(hackbot_run(args))
    else:
        log.error(f"❌ Error: Invalid command: {args.command}")
        exit(1)


if __name__ == "__main__":
    _run()
