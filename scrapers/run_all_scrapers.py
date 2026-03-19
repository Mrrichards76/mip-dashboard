import subprocess
import os

# Change working directory to the script's folder
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Run the scrapers
subprocess.run(["python", "github_scraper.py"])
subprocess.run(["python", "angel_scraper.py"])
