from logic_parser.ParserRepository import parser_run
import schedule
import asyncio
import time


def main():
    """
    Входная точка логики которая запускается с интервалом в 10 минут
    """
    asyncio.run(parser_run())

main()
schedule.every(10).minutes.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)
