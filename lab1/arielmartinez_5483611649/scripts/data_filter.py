from bs4 import BeautifulSoup
import os
import pandas as pd

# Read the HTML 
print("Accessing HTML...")
current_dir = os.path.dirname(os.path.abspath(__file__))  
base_dir = os.path.join(current_dir, "..", "data")
inp = os.path.join(base_dir, "raw_data/web_data.html")
with open(inp, "r", encoding="utf-8") as file:
    html = file.read()

# Parse 
print("Parsing...")
soup = BeautifulSoup(html, "html.parser")

# Extract Market Data
print("Extracting Market Data...")
market_data = []
market = soup.select(".MarketCard-container")
for m in market:
    symbol = m.select_one(".MarketCard-symbol").text.strip()
    pos = m.select_one(".MarketCard-stockPosition").text.strip()
    pct = m.select_one(".MarketCard-changesPct").text.strip() 
    market_data.append({
        "Market Symbol": symbol,
        "Market Stock Position": float(pos.replace(',','')),
        "Market Change Pct": pct
    })

# Extract News Data
print("Extracting Latests News Data...")
news_data = []
news = soup.select(".LatestNews-item")
for n in news:
    stamp = n.select_one(".LatestNews-timestamp").text.strip()
    title = n.select_one(".LatestNews-headline").text.strip()
    link = n.select_one(".LatestNews-headline")["href"]
    news_data.append({
        "LatestNews Timestamp": stamp,
        "Title": title,
        "Link": link
    })

# Save results in csv
print("Saving Results...")
out = os.path.join(base_dir, "processed_data")
market_data_path = os.path.join(out, "market_data.csv")
news_data_path = os.path.join(out, "news_data.csv")
pd.DataFrame(market_data).to_csv(market_data_path, index=False)
pd.DataFrame(news_data).to_csv(news_data_path, index=False)
print("Market data saved to:", market_data_path)
print("News data saved to:", news_data_path)
