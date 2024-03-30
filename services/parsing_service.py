import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from seleniumwire import webdriver

from repository import auto_repository


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
        time.sleep(5)

        all_cars = driver.find_elements(By.CLASS_NAME, "ItemCardList__item")
        list_link_cars = [car.get_attribute('href') for car in all_cars]

        driver.close()
        return list_link_cars
    except:
        return []


async def get_content_milanuncios(data: dict[str, str]):
    url = (f"https://www.milanuncios.com/coches-de-segunda-mano/?s={data.get('brand')} - {data.get('model')}"
           f"&desde={data.get('price').split('-')[0]}&hasta={data.get('price').split('-')[1]}&demanda=n&"
           f"kilometersFrom={data.get('mileage').split('-')[0]}&kilometersTo={data.get('mileage').split('-')[1]}"
           f"&anod={data.get('years').split('-')[0]}&anoh={data.get('years').split('-')[1]}&orden=relevance&"
           "fromSearch=1&hitOrigin=listing")
    try:
        driver.get(url)
        time.sleep(5)
        
        all_cars = driver.find_elements(By.CLASS_NAME, "ma-AdCardListingV2-TitleLink")
        list_link_cars = [f"https://www.milanuncios.com{car.get_attribute('href')}" for car in all_cars]

        driver.close()
        return list_link_cars
    except:
        return []

async def get_content_coches(data: dict[str, str]):
    brand_id, model_id = await auto_repository.get_brand_and_model_auto(brand_name=data.get('brand'),
                                                                            model_name=data.get('model'))

    url = (f"https://www.coches.net/segunda-mano/?MinPrice={data.get('price').split('-')[0]}&MaxPrice="
        f"{data.get('price').split('-')[1]}&MinYear={data.get('years').split('-')[0]}&MaxYear="
        f"{data.get('years').split('-')[1]}&MinKms={data.get('mileage').split('-')[0]}&MaxKms="
        f"{data.get('mileage').split('-')[1]}&MakeIds[0]={brand_id}&"
        f"ModelIds[0]={model_id}&Versions[0]=")

    try:
        driver.get(url)
        time.sleep(5)
        
        all_cars = driver.find_elements(By.CLASS_NAME, "mt-CardBasic-titleLink")
        list_link_cars = [car.get_attribute('href') for car in all_cars]
        driver.close()
        return list_link_cars
    except:
        return []