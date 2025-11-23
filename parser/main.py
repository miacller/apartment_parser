#parser/main.py
from parser.scraper import get_tree, get_apartments, apartment_parameters
from parser.utils import PAGE_DELAY, APARTMENT_DELAY, ERROR_DELAY, BASE_URL, rooms_counter
from requests.exceptions import RequestException
from tqdm.auto import tqdm
import time
import random

def main():
    minprice = 1
    maxprice = 5000000
    price_step = 5000000
    max_total_price = 60000000


    with tqdm(total=(max_total_price//price_step), desc="Общий прогресс по ценам", unit="диапазон") as price_bar:
        while maxprice <= max_total_price:
            base_url = f"{BASE_URL}&maxprice={maxprice}&minprice={minprice}"
        
            time.sleep(random.uniform(*PAGE_DELAY))
        
            try:
                tree = get_tree(base_url)
                h5_text = tree.find('h5', class_="_93444fe79c--color_text-primary-default--vSRPB").get_text(strip=True)
                total_ads = int(h5_text.split('Найдено')[1].split('объ')[0].replace(" ", ""))
                maxpage = min((total_ads // 30) + 1, 50)
            
                for page in tqdm(range(1, maxpage + 1), desc=f"Цена {minprice}-{maxprice}", leave=False, unit="стр"):
                    page_url = f"{base_url}&p={page}"
                
                    try:
                        time.sleep(random.uniform(*PAGE_DELAY))
                        links = get_apartments(page_url)

                        for link in tqdm(links, desc=f"Страница {page}", leave=False, unit="кв"):
                            try:
                                time.sleep(random.uniform(*APARTMENT_DELAY))
                                apartment_parameters(link)
                            except Exception as e:
                                print(f"\nОшибка квартиры {link}: {e}")
                                time.sleep(ERROR_DELAY)
                            
                    except RequestException as e:
                        print(f"\nСетевая ошибка страницы {page}: {e}")
                        time.sleep(ERROR_DELAY)
                    except Exception as e:
                        print(f"\nОшибка страницы {page}: {e}")
                        time.sleep(ERROR_DELAY)
                    
            except RequestException as e:
                print(f"\nСетевая ошибка диапазона {minprice}-{maxprice}: {e}")
                time.sleep(ERROR_DELAY * 2)
            except Exception as e:
                print(f"\nОшибка диапазона {minprice}-{maxprice}: {e}")
                time.sleep(ERROR_DELAY * 2)
            finally:
                minprice += price_step
                maxprice += price_step
                price_bar.update(1)

if __name__ == "__main__":
    main()