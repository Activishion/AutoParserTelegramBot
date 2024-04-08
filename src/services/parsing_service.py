import time

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from seleniumwire import webdriver

from repository import auto_repository
from settings.dict_marks import dict_marks_car
from settings.dict_models import dict_models
from services.logging_service import error_log, static_log


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--no-gpu')
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--dns-prefetch-disable')

driver = webdriver.Chrome(options=chrome_options)


async def get_content_wallapop(data: dict[str, str]) -> list[str]:
    url = (f"https://es.wallapop.com/app/search?brand={data.get('brand')}&min_year={data.get('years').split('-')[0]}"
           f"&max_year={data.get('years').split('-')[1]}&min_km={data.get('mileage').split('-')[0]}"
           f"&max_km={data.get('mileage').split('-')[1]}&min_sale_price={data.get('price').split('-')[0]}"
           f"&max_sale_price={data.get('price').split('-')[1]}&filters_source=default_filters&"
           f"category_ids=100&keywords={data.get('model')}&longitude=-3.69196&latitude=40.41956")
    try:
        driver.get(url)
        static_log.info(f'Request es.wallapop.com {datetime.now()}')
        time.sleep(5)

        all_cars = driver.find_elements(By.CLASS_NAME, "ItemCardList__item")
        list_link_cars = [car.get_attribute('href') for car in all_cars]

        driver.close()
        return list_link_cars
    except:
        error_log.error('Error parsing es.wallapop.com')
        return []


async def get_content_coches(data: dict[str, str]) -> list[str]:
    try:
        brand_id: int = dict_marks_car.get(data.get('brand'))
        model_id: int = dict_models.get(data.get('model'))

        #model_id: int = await auto_repository.get_model_id_auto(data.get('model'))  если нужно будет из бд тащить
    
        url = (f"https://www.coches.net/segunda-mano/?MinPrice={data.get('price').split('-')[0]}&MaxPrice="
               f"{data.get('price').split('-')[1]}&MinYear={data.get('years').split('-')[0]}&MaxYear="
               f"{data.get('years').split('-')[1]}&MinKms={data.get('mileage').split('-')[0]}&MaxKms="
               f"{data.get('mileage').split('-')[1]}&MakeIds[0]={brand_id}&"
               f"ModelIds[0]={model_id}&Versions[0]=")
        driver.get(url)
        time.sleep(5)

        all_cars = driver.find_elements(By.CLASS_NAME, "mt-CardBasic-titleLink")
        list_link_cars: list[str] = [f"https://www.coches.net/{car.get_attribute('href')}" for car in list(all_cars)]
        driver.close()

        return list_link_cars
    except:
        error_log.error('Error parsing www.coches.net')
        return []
