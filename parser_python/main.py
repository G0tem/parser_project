from logic_parser.ParserRepository import parser_start


url = 'https://habr.com/ru/articles/'

def main():
    """Старт логики"""
    print("Запуск логики")
    parser_start(url)

if __name__ == "__main__":
    main()

