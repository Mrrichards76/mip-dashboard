# 1️⃣ Imports
import requests
from datetime import datetime, timezone
import sqlite3
from dateutil import parser

# 2️⃣ Database setup — creates table if it doesn't exist
conn = sqlite3.connect("mip_live.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company TEXT,
    signal_type TEXT,
    source TEXT,
    strength REAL,
    timestamp TEXT,
    details TEXT,
    momentum_score INTEGER DEFAULT 0,
    breakout_alert INTEGER DEFAULT 0
)
""")
conn.commit()

# 3️⃣ Momentum Score function
def calculate_momentum_score(repo):
    """
    Returns a simple momentum score based on stars and forks.
    Can be refined later with additional signals.
    """
    stars = repo.get("stargazers_count", 0)
    forks = repo.get("forks_count", 0)
    return stars + forks

# 4️⃣ Placeholder Breakout Alert function
def calculate_breakout_alert(repo):
    # For now, always return 0; refine logic later
    return 0

# 5️⃣ GitHub scraping logic
# Example: fetch trending repos from GitHub API (can be replaced with real query)
url = "https://api.github.com/search/repositories?q=language:python&sort=stars&order=desc&per_page=10"
response = requests.get(url)
data = response.json()
repos = data.get("items", [])

# 6️⃣ Loop through repos and insert into DB
for repo in repos:
    company = repo.get("name")
    signal_type = "GitHub Spike"
    source = "GitHub"
    strength = repo.get("stargazers_count", 0) / 1000  # example
    timestamp = datetime.now(timezone.utc).isoformat()
    details = repo.get("html_url")
    
    # Compute scores
    momentum_score = calculate_momentum_score(repo)
    breakout_alert = calculate_breakout_alert(repo)
    
    # Insert into DB (correct 1-tuple)
    cursor.execute("""
        INSERT INTO signals (company, signal_type, source, strength, timestamp, details, momentum_score, breakout_alert)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (company, signal_type, source, strength, timestamp, details, momentum_score, breakout_alert))

conn.commit()
conn.close()
print("GCM — Scraper completed successfully!")
