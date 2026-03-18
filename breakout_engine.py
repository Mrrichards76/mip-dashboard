# breakout_engine.py

def calculate_breakout_alert(repo, source):
    if source == "GitHub":
        stars = repo.get("stargazers_count", 0)
        forks = repo.get("forks_count", 0)
        recent_activity = repo.get("recent_activity_days", 0)
        return 1 if stars > 1000 and recent_activity < 14 else 0
    elif source == "AngelList":
        followers = repo.get("followers", 0)
        funding_rounds = repo.get("funding_rounds", 0)
        return 1 if followers + 500*funding_rounds > 2000 else 0
    else:
        return 0
