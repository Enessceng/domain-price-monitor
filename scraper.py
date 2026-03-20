from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
from datetime import datetime

###################################
# CHROME SETTINGS
###################################

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)

###################################
# DYNADOT
###################################

driver.get("https://www.dynadot.com/domain/prices")

time.sleep(6)

rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

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

time.sleep(10)

rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

providers = []
tlds = []
prices = []

wanted = [".co", ".com", ".org", ".io", ".net"]

for row in rows:
    try:
        cols = row.find_elements(By.TAG_NAME, "td")

        if len(cols) < 5:
            continue

        tld = cols[0].text.replace("*", "").strip()
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
# HOSTINGER
###################################

driver.get("https://www.hostinger.com/pricing/domains")

time.sleep(6)

providers = []
tlds = []
prices = []

seen = set()
wanted = [".com", ".org", ".net", ".co", ".io"]

try:
    search = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Find a domain extension']")

    for tld_search in wanted:
        search.clear()
        time.sleep(1)
        search.send_keys(tld_search)
        time.sleep(2)

        try:
            row = driver.find_element(By.CSS_SELECTOR, "table tbody tr")

            tld = row.find_element(By.CSS_SELECTOR, "td.tlds-table__tld-cell a").text
            price = row.find_element(By.CSS_SELECTOR, ".tlds-table__first-year-price").text

            if tld not in seen:
                seen.add(tld)
                providers.append("Hostinger")
                tlds.append(tld)
                prices.append(price)
        except:
            continue
except:
    pass

df_hostinger = pd.DataFrame({
    "Provider": providers,
    "TLD": tlds,
    "Price": prices
})

###################################
# PORKBUN
###################################

driver.get("https://porkbun.com/products/domains")

time.sleep(10)

rows = driver.find_elements(By.CSS_SELECTOR, "[data-extension]")

providers = []
tlds = []
prices = []

wanted = ["com", "org", "net", "co", "io"]

for row in rows:
    try:
        extension = row.get_attribute("data-extension")
        price = row.get_attribute("data-price-registration")

        if extension in wanted and price:
            providers.append("Porkbun")
            tlds.append("." + extension)
            prices.append("$" + str(float(price) / 100))
    except:
        continue

df_porkbun = pd.DataFrame({
    "Provider": providers,
    "TLD": tlds,
    "Price": prices
})

###################################
# IONOS
###################################

driver.get("https://www.ionos.com/domains/domain-name-prices")

time.sleep(6)

providers = []
tlds = []
prices = []

wanted = {"com", "org", "net", "co", "io"}

try:
    dropdown = Select(driver.find_element(By.TAG_NAME, "select"))
    dropdown.select_by_visible_text("500")
    time.sleep(4)

    rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")

        if len(cols) < 2:
            continue

        tld = cols[0].text.strip().replace(".", "").lower()
        price = cols[1].text.strip()

        if tld in wanted:
            providers.append("IONOS")
            tlds.append("." + tld)
            prices.append(price)
except:
    pass

df_ionos = pd.DataFrame({
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
# SAVE
###################################

final_df.to_csv("domain_prices.csv", index=False)

driver.quit()

print("CSV created")
print(final_df)
