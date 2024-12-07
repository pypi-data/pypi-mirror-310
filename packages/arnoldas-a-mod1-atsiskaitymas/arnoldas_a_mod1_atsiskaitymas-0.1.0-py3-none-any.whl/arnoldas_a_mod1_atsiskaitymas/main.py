from arnoldas_a_mod1_atsiskaitymas.crawler import Crawl

def main():
    # source "book_info" or "football_results"
    source = "book_info"
    # timeout in seconds
    timeout = 60
    # return_format "dict" or "csv"
    return_format = "dict"

    results = Crawl(source=source, timeout=timeout, return_format=return_format).web_results()
    if results:
        print("Gauti duomenys:")
        print(results)

if __name__ == "__main__":
    main()