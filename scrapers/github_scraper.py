import requests
import sqlite3
from datetime import datetime

# -------------------------
# DATABASE CONNECTION
# -------------------------

conn = sqlite3.connect("mip_live.db")
cursor = conn.cursor()

# -------------------------
# FETCH TRENDING REPOS
# -------------------------

url = "https://api.github.com/search/repositories?q=stars:%3E500&sort=stars&order=desc"

response = requests.get(url)
data = response.json()

repos = data.get("items", [])[:10]

# -------------------------
# INSERT SIGNALS
# -------------------------

for repo in repos:

    company = repo["name"]
    signal_type = "GitHub Spike"
    source = "GitHub"
    strength = repo["stargazers_count"] / 10000
    timestamp = datetime.utcnow().isoformat()
    details = repo["html_url"]

    cursor.execute("""
        INSERT INTO signals
        (company, signal_type, source, strength, timestamp, details)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (company, signal_type, source, strength, timestamp, details))

    print(f"Signal added for {company}")

conn.commit()
conn.close()
