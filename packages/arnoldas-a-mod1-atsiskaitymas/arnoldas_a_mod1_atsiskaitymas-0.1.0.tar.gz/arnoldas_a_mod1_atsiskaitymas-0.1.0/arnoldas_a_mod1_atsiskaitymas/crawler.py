import time
# importuotas time, kad būtų galima naudoti timeout funkciją
import pandas as pd
from arnoldas_a_mod1_atsiskaitymas.football_results import footbal_results
from arnoldas_a_mod1_atsiskaitymas.book_info import book_info

class TimeoutException(Exception):
    pass

class Crawl:
    def __init__(self, source: str, timeout: int = 60, return_format: str = "csv"):
        self.source = source
        self.timeout = timeout
        self.return_format = return_format
        self.start_time = time.time()

    def web_results(self):
        try:
            if self.source == "football_results":
                footbal_results()
                data = pd.read_csv("../samples/football_results.csv")

            elif self.source == "book_info":
                book_info("book_info.csv")
                data = pd.read_csv("../samples/book_info.csv")

            else:
                raise ValueError("Pasirinkite 'football_results' arba 'book_info'.")

            if time.time() - self.start_time > self.timeout:
                raise TimeoutException("Funkcijos vykdymo laikas baigėsi.")

            if self.return_format == "csv":
                print("Rezultatai išsaugoti CSV faile.")
                return None
            elif self.return_format == "dict":
                return data.to_dict(orient="records")
            else:
                raise ValueError("Netinkamas formatas. Pasirinkite 'csv' arba 'dict'.")

        except TimeoutException:
            print("Funkcijos vykdymo laikas baigėsi.")
            return None
        except Exception as e:
            print(f"Klaida: {e}")
            return None