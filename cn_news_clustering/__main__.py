from scrape_articles import WebsiteDatabase
from globals import Globals as glob


def main():
    try:
        webdb = WebsiteDatabase(glob.sites)
        for site in webdb.sites:
            print(site.name)
        output = webdb.compute()
        print(output)
    except KeyboardInterrupt:
        print("\nUser interrupted session.\n")

if __name__ == "__main__":
    main()
