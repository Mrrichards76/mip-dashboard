import sqlite3
from datetime import datetime, timezone

# 1️⃣ Database setup — connect to existing DB
conn = sqlite3.connect("mip_live.db")
cursor = conn.cursor()

# 2️⃣ Placeholder for startup data
# In real usage, replace with API calls or scraping logic
startups = [
    {"name": "StartupA", "followers": 1500, "funding_rounds": 2, "url": "https://angel.co/startupA"},
    {"name": "StartupB", "followers": 800, "funding_rounds": 1, "url": "https://angel.co/startupB"},
    {"name": "StartupC", "followers": 3000, "funding_rounds": 3, "url": "https://angel.co/startupC"},
]

# 3️⃣ Momentum score function
def calculate_momentum_score(startup):
    # Example: followers + 500 * funding_rounds
    followers = startup.get("followers", 0)
    funding_rounds = startup.get("funding_rounds", 0)
    return followers + (500 * funding_rounds)

# 4️⃣ Breakout alert placeholder
def calculate_breakout_alert(startup):
    # Example: mark breakout if momentum_score > 2000
    return 1 if calculate_momentum_score(startup) > 2000 else 0

# 5️⃣ Insert startups into DB
for s in startups:
    company = s.get("name")
    signal_type = "AngelList Signal"
    source = "AngelList"
    strength = s.get("followers", 0) / 1000  # simple scaling
    timestamp = datetime.now(timezone.utc).isoformat()
    details = s.get("url")
    
    momentum_score = calculate_momentum_score(s)
    breakout_alert = calculate_breakout_alert(s)
    
    cursor.execute("""
        INSERT INTO signals (company, signal_type, source, strength, timestamp, details, momentum_score, breakout_alert)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (company, signal_type, source, strength, timestamp, details, momentum_score, breakout_alert))

conn.commit()
conn.close()
print("GCM — AngelList scraper completed successfully!")
