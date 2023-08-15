import time
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
df = pd.DataFrame()

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument('--allow-running-insecure-content')
chrome_options.add_argument('--ignore-certificate-errors')

driver = uc.Chrome(executable_path="chromedriver",chrome_options=chrome_options)

firstpage = 0
lastpage = 101

for i in range(firstpage,lastpage):
    try:
        driver.get(f'https://clutch.co/developers/artificial-intelligence?page={i}')
        company_names = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "company_info"))  # This is a dummy element
        )
        company_websites = driver.find_elements(By.CLASS_NAME, "website-link__item")
        for i in range(50):
            company = company_names[i].text
            company_website = company_websites[i].get_attribute("href")
            new_row = {'Company Name ': company, 'Company Website': company_website}
            df = df.append(new_row, ignore_index=True)
        df.to_csv('clutch_data.csv', index=False)
    except Exception as e:
        print(e)
    time.sleep(50)


