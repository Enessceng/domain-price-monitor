from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
from datetime import datetime

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)

wait = WebDriverWait(driver, 20)

###################################
# DYNADOT
###################################

driver.get("https://www.dynadot.com/domain/prices")

rows = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
)

providers = []
tlds = []
prices = []

wanted = [".co", ".com", ".org", ".io", ".net"]

for row in rows:

    try:
        tld = row.find_element(By.CSS_SELECTOR, "td.data-row-name a").text
        price = row.find_element(By.CSS_SELECTOR, "td.data-row-reg_price span.value").text

        if tld in wanted:
            providers.append("Dynadot")
            tlds.append(tld)
            prices.append(price)

    except:
        continue

df_dynadot = pd.DataFrame({
    "Provider": providers,
    "TLD": tlds,
    "Price": prices
})

###################################
# NAMECHEAP
###################################

driver.get("https://www.namecheap.com/domains/full-tld-list/")

rows = wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
)

providers = []
tlds = []
prices = []

wanted = [".co", ".com", ".org", ".io", ".net"]

for row in rows:

    try:
        cols = row.find_elements(By.TAG_NAME, "td")

        if len(cols) < 5:
            continue

        tld = cols[0].text.replace("*","").strip()
        price = cols[4].text.split("\n")[0]

        if tld in wanted:
            providers.append("Namecheap")
            tlds.append(tld)
            prices.append(price)

    except:
        continue

df_namecheap = pd.DataFrame({
    "Provider": providers,
    "TLD": tlds,
    "Price": prices
})

###################################
# MERGE
###################################

final_df = pd.concat(
    [df_dynadot, df_namecheap],
    ignore_index=True
)

final_df["Date"] = datetime.today().date()

final_df.to_csv("domain_prices.csv", index=False)

driver.quit()

print("CSV created")
print(final_df)
