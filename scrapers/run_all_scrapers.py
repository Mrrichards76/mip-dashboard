import subprocess

# Since run_all_scrapers.py is inside scrapers/, just call the scripts directly
subprocess.run(["python", "github_scraper.py"])
subprocess.run(["python", "angel_scraper.py"])
