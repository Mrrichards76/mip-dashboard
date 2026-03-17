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

        # ---- Momentum Score Calculation ----
    stars = repo.get("stargazers_count", 0)
    forks = repo.get("forks_count", 0)
    recent_activity_days = (datetime.utcnow() - parser.parse(repo["pushed_at"])).days
    contributors = repo.get("contributors_count", 1)
    has_docs = bool(repo.get("has_docs", False))
    is_org = repo.get("owner_type", "") == "Organization"

    momentum_score = calculate_momentum_score(
        stars, forks, recent_activity_days, contributors, has_docs, is_org
    )

    cursor.execute("""
        SELECT momentum_score FROM signals
        WHERE company = ?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (company_name,))
    result = cursor.fetchone()
    previous_score = result[0] if result else 0

    breakout_alert = 1 if (momentum_score - previous_score) >= 15 else 0

    cursor.execute("""
        INSERT INTO signals
        (company, signal_type, source, strength, timestamp, details)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (company, signal_type, source, strength, timestamp, details))

    print(f"Signal added for {company}")

conn.commit()
conn.close()
