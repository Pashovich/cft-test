from aiohttp import web
from app.config.app import app_config
import argparse
import asyncio
from app.config.enviroment import load_environment

def main():
    parser = argparse.ArgumentParser(description='Run application.')

    parser.add_argument(
        '--port',
        type=int,
        default=8080,
        help='application port.'
    )

    parser.add_argument(
        '--debug',
        action='store_true',
    )
    parser.add_argument(
        '--load_env',
        action='store_true',
    )

    args = parser.parse_args()

    if args.load_env:
        load_environment()
        return

    app = web.Application(
        debug=args.debug
    )
    load_environment()
    app_config(app)

    web.run_app(
        app,
        port=args.port,
        access_log=None
    )


if __name__ == '__main__':
    main()