from webdriver_manager.firefox import GeckoDriverManager
import time
import undetected_chromedriver as uc
import pandas as pd
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from tqdm import tqdm

try:
    with tqdm(total=100) as pbar:
        read_from = 'PostCode (1).xlsx'
        save_to = 'Sold_Zoobla.xlsx'
        url = 'https://www.zoopla.co.uk/house-prices/'

        options = uc.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument('--disable-gpu')
        capa = DesiredCapabilities.FIREFOX
        capa["pageLoadStrategy"] = "none"

        # Set GeckoDriver (Firefox) version
        driver_version = 'v0.33.0'  # Change this to the desired version
        driver_path = GeckoDriverManager(
            version=driver_version).install()

        driver = uc.Chrome(service=Service(driver_path), options=options)
        time.sleep(4)

        names = []
        descs = []
        post_codes = []
        sold_price = []
        estimate_price = []
        last_sold_date = []

        def auto_save(post_code, names, descs, sold_price, estimate_price, last_sold_date):
            print(f'Auto saved:{len(post_code)} ')
            names = list(filter(
                lambda x: x != 'Only 1 result, try broadening your criteria...', names))
            max_length = max(len(descs), len(last_sold_date), len(
                names), len(estimate_price), len(post_code), len(sold_price))
            descs += [None] * (max_length - len(descs))
            last_sold_date += [None] * \
                (max_length - len(last_sold_date))
            names += [None] * (max_length - len(names))
            estimate_price += [None] * (max_length - len(estimate_price))
            post_code += [None] * (max_length - len(post_code))
            sold_price += [None] * (max_length - len(sold_price))

            json = {'PostCode': post_code,
                    'Name': names,
                    'Type': descs,
                    'Last Sold Date': last_sold_date,
                    'Sold Price': sold_price,
                    'Estimate Price': estimate_price
                    }

            df_ = pd.DataFrame(json)

            df_ = df_.drop_duplicates(
                ['PostCode', 'Name', 'Type', 'Last Sold Date', 'Sold Price', 'Estimate Price'], keep='last')

            df = pd.DataFrame(df_)
            df.to_excel(save_to, index=False)

        def get_sold_page(base_url, post_code_s):
            prop_names = driver.find_elements(
                By.XPATH, "//div[@data-testid='result-item']//h2")
            prop_descs = driver.find_elements(
                By.XPATH, "//div[contains(@class,'_1qo832z2')]")
            prop_last_sold_prices = driver.find_elements(
                By.XPATH, "//div[label[contains(text(),'Last sold')]]/label[@class='_136k16p6 _1dgm2fc6']")
            prop_last_estimated_prices = driver.find_elements(
                By.XPATH, "//div[label[contains(text(),'Estimated price')]]/label[@class='_136k16p6 _1dgm2fc6']")
            prop_last_sold_dates = driver.find_elements(
                By.XPATH, "//div[label[contains(text(),'Last sold -')]]")

            for prop_name in prop_names:
                post_codes.append(post_code_s)
                names.append(prop_name.get_attribute('textContent'))
            for prop_desc in prop_descs:
                descs.append(prop_desc.get_attribute('textContent'))
            for prop_last_sold_price in prop_last_sold_prices:
                sold_price.append(
                    prop_last_sold_price.get_attribute('textContent'))
            for prop_last_estimated_price in prop_last_estimated_prices:
                estimate_price.append(
                    prop_last_estimated_price.get_attribute('textContent'))
            for k in range(len(prop_last_sold_dates)):
                last_sold_date.append(prop_last_sold_dates[k].get_attribute('textContent').replace(
                    'Last sold - ', '').replace(prop_last_sold_prices[k].get_attribute('textContent'), ''))
            auto_save(post_codes, names, descs, sold_price,
                      estimate_price, last_sold_date)
            global i
            i = i+1
            page = f'&pn={i}'
            driver.get(f'{base_url}{page}')

            scope = driver.find_elements(
                By.XPATH, "//div[@data-testid='result-item']//h2")
            if len(scope) != 0:
                get_sold_page(base_url, post_code_s)
            else:
                return

        driver.get(url)
        time.sleep(4)

        df = pd.read_excel(read_from, sheet_name='Zoopla Sold')
        print('Total len of post codes :')
        print(len(df))
        u = 0
        for i in range(len(df)):

            post = df['PostCode'][i].replace(' ', '-').lower()
            print(f'\nCurrently at :{i+1} of {len(df)} post code : {post}')

            while driver.current_url == url:

                driver.get(url)
                if u == 0:
                    time.sleep(8)
                u = 1
                try:
                    driver.find_element(
                        By.XPATH, "//button[@text()='Accept all cookies']").click()
                    driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(
                        EC.element_to_be_clickable((By.XPATH, "//label[text()='Search area']/following-sibling::div//input"))))
                except Exception:
                    pass
                # Get 1st item in row
                search = driver.find_element(
                    By.XPATH, "//label[text()='Search area']/following-sibling::div//input")
                search.click()
                search.send_keys(post)
                driver.find_element(
                    By.XPATH, "//button[.//div[text()='Search']]").click()
                time.sleep(5)

            base_url = driver.current_url
            i = 1
            get_sold_page(base_url, post)
            pbar.update(100/len(df))
            driver.get(url)

    pbar.update(100 - pbar.n)
except Exception as e:
    print(e)
