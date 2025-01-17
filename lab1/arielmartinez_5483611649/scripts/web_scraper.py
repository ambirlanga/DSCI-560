from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions 
from bs4 import BeautifulSoup
import os

# URL
url = "https://www.cnbc.com/world/?region=world"

# Selenium to capture JavaScript content that requests avoid
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--start-fullscreen")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:
    
    # Obtain HTML
    print("Obtaining html...")
    driver.get(url)
    # Wait to MarketCard-row because if not it will cut most of the content 
    WebDriverWait(driver, 5).until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, "MarketCard-row")))

    print("Parsing...")
    soup = BeautifulSoup(driver.page_source, "html.parser")


    # Obtain Sections
    print("Extracting Market Banner data...")
    market = soup.find("div", class_="MarketsBanner-main").prettify() 

    print("Extracting Latests News data...")
    news = soup.find("ul", class_="LatestNews-list").prettify() 


    # Save HTML sections
    print("Creating file...\n")
    current_dir = os.path.dirname(os.path.abspath(__file__))  
    base_dir = os.path.join(current_dir, "..", "data/raw_data")
    out = os.path.join(base_dir, "web_data.html")
    with open(out, "w", encoding="utf-8") as file:
        file.write(str(market))
        file.write("\n\n\n\n\n")
        file.write(news)

    print("Data successfully saved to 'web_data.html'.")

except Exception as e:
    print(f"Error: {e}")
finally:
    driver.quit()
