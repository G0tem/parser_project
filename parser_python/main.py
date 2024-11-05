from logic_parser.ParserRepository import parser_run
import schedule
import asyncio
import time


def main():
    """
    Logical entry point running at 10 minute intervals
    """
    asyncio.run(parser_run())

main()  # run 1 time during startup
schedule.every(10).minutes.do(main)  # run every 10 minutes

while True:
    schedule.run_pending()
    time.sleep(1)
