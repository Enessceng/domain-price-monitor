from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from datetime import datetime

driver = webdriver.Chrome()
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
# HOSTINGER
###################################

driver.get("https://www.hostinger.com/domain-prices")

time.sleep(5)

providers = []
tlds = []
prices = []

rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")

for row in rows:

    try:
        tld = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
        price = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text

        if tld in wanted:
            providers.append("Hostinger")
            tlds.append(tld)
            prices.append(price)

    except:
        continue

df_hostinger = pd.DataFrame({
    "Provider": providers,
    "TLD": tlds,
    "Price": prices
})

###################################
# IONOS
###################################

driver.get("https://www.ionos.com/domains/domain-names")

time.sleep(5)

providers = []
tlds = []
prices = []

rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

for row in rows:

    try:
        tld = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
        price = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text

        if tld in wanted:
            providers.append("IONOS")
            tlds.append(tld)
            prices.append(price)

    except:
        continue

df_ionos = pd.DataFrame({
    "Provider": providers,
    "TLD": tlds,
    "Price": prices
})

###################################
# NAMECHEAP
###################################

driver.get("https://www.namecheap.com/domains/registration/")

time.sleep(5)

providers = []
tlds = []
prices = []

rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")

for row in rows:

    try:
        tld = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
        price = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text

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
# PORKBUN
###################################

driver.get("https://porkbun.com/tld/pricing")

time.sleep(5)

providers = []
tlds = []
prices = []

rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

for row in rows:

    try:
        tld = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text
        price = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text

        if tld in wanted:
            providers.append("Porkbun")
            tlds.append(tld)
            prices.append(price)

    except:
        continue

df_porkbun = pd.DataFrame({
    "Provider": providers,
    "TLD": tlds,
    "Price": prices
})

###################################
# MERGE
###################################

final_df = pd.concat(
    [df_dynadot, df_namecheap, df_hostinger, df_porkbun, df_ionos],
    ignore_index=True
)


final_df["Date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

###################################
# SAVE CSV
###################################

final_df.to_csv("domain_prices.csv", index=False)

driver.quit()

print("CSV created successfully")
print(final_df)
