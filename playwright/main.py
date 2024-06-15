from websites.amazonca import crawl_amazonca
from websites.sourceofficefurniture import crawl_sourceofficefurniture
from websites.toysrusca import crawl_toysrusca
import sys

def main():
    args = sys.argv[1:]
    match args:
        case "1":
            # amazonca
            crawl_amazonca()
        case "2":
            # sourceofficefurniture
            crawl_sourceofficefurniture()
        case "3":
            # toysrusca
            crawl_toysrusca()
        case _:
            print("Invalid option")


if __name__ == "__main__":
    main()
