from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
from datetime import datetime
import logging
import os

# LOG ADJUST


logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Script started")


# DRIVER

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

wanted = [".co", ".com", ".org", ".io", ".net"]


# DYNADOT

providers = []
tlds = []
prices = []

try:

    driver.get("https://www.dynadot.com/domain/prices")

    rows = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table tbody tr"))
    )

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

    logging.info("Dynadot scraped successfully")

except Exception as e:
    logging.error(f"Dynadot scraping failed: {e}")

df_dynadot = pd.DataFrame({
    "Provider": providers,
    "TLD": tlds,
    "Price": prices
})

# NAMECHEAP

providers = []
tlds = []
prices = []

try:

    driver.get("https://www.namecheap.com/domains/full-tld-list/")

    time.sleep(5)

    rows = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

    for row in rows:

        try:
            cols = row.find_elements(By.TAG_NAME, "td")

            tld = cols[0].text.replace("*","")
            price = cols[4].text.split("\n")[0]

            if tld in wanted:
                providers.append("Namecheap")
                tlds.append(tld)
                prices.append(price)

        except:
            continue

    logging.info("Namecheap scraped successfully")

except Exception as e:
    logging.error(f"Namecheap scraping failed: {e}")

df_namecheap = pd.DataFrame({
    "Provider": providers,
    "TLD": tlds,
    "Price": prices
})


# HOSTINGER


providers = []
tlds = []
prices = []

try:

    driver.get("https://www.hostinger.com/pricing/domains")

    search = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Find a domain extension']"))
    )

    for tld_search in wanted:

        search.clear()
        time.sleep(1)
        search.send_keys(tld_search)
        time.sleep(2)

        try:
            row = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table tbody tr"))
            )

            tld = row.find_element(By.CSS_SELECTOR, "td.tlds-table__tld-cell a").text
            price = row.find_element(By.CSS_SELECTOR, ".tlds-table__first-year-price").text

            providers.append("Hostinger")
            tlds.append(tld)
            prices.append(price)

        except:
            continue

    logging.info("Hostinger scraped successfully")

except Exception as e:
    logging.error(f"Hostinger scraping failed: {e}")

df_hostinger = pd.DataFrame({
    "Provider": providers,
    "TLD": tlds,
    "Price": prices
})


# PORKBUN

providers = []
tlds = []
prices = []

try:

    driver.get("https://porkbun.com/products/domains")

    time.sleep(5)

    rows = driver.find_elements(By.CSS_SELECTOR, "div.domainsPricingAllExtensionsItem")

    for row in rows:

        extension = row.get_attribute("data-extension")
        price = row.get_attribute("data-price-registration")

        if extension in ["com","org","net","co","io"]:

            providers.append("Porkbun")
            tlds.append("." + extension)
            prices.append("$" + str(float(price)/100))

    logging.info("Porkbun scraped successfully")

except Exception as e:
    logging.error(f"Porkbun scraping failed: {e}")

df_porkbun = pd.DataFrame({
    "Provider": providers,
    "TLD": tlds,
    "Price": prices
})

# IONOS

providers = []
tlds = []
prices = []

try:

    driver.get("https://www.ionos.com/domains/domain-name-prices")

    time.sleep(5)

    dropdown = Select(driver.find_element(By.TAG_NAME, "select"))
    dropdown.select_by_visible_text("500")

    time.sleep(4)

    rows = driver.find_elements(By.CSS_SELECTOR, "tbody tr")

    wanted_set = {"com","org","net","co","io"}

    for row in rows:

        cols = row.find_elements(By.TAG_NAME,"td")

        if len(cols) < 2:
            continue

        tld = cols[0].text.strip().replace(".","").lower()
        price = cols[1].text.strip()

        if tld in wanted_set:

            providers.append("IONOS")
            tlds.append("." + tld)
            prices.append(price)

    logging.info("IONOS scraped successfully")

except Exception as e:
    logging.error(f"IONOS scraping failed: {e}")

df_ionos = pd.DataFrame({
    "Provider":providers,
    "TLD":tlds,
    "Price":prices
})


# DATAFRAME MERGE

final_df = pd.concat(
    [df_dynadot, df_namecheap, df_hostinger, df_porkbun, df_ionos],
    ignore_index=True
)

final_df["Date"] = datetime.today().date()

# CSV(APPEND)


file_name = "domain_prices.csv"

try:

    if os.path.exists(file_name):

        final_df.to_csv(
            file_name,
            mode="a",
            header=False,
            index=False
        )

    else:

        final_df.to_csv(
            file_name,
            mode="w",
            header=True,
            index=False
        )

    logging.info("Data saved successfully")

except Exception as e:

    logging.error(f"Saving CSV failed: {e}")

# DRIVER CLOSE


driver.quit()

logging.info("Script finished successfully")

print(final_df)