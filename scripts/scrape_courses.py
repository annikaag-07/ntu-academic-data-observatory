import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

URL = "https://wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1"

# ALL relevant prefixes NTU CS students may take
PREFIXES = [
    "SC", "CC", "ML", "MH", "MA",
    "CV", "IE", "BS", "BU",
    "HW", "HY", "CM", "ES",
    "HH", "HL", "HP", "HS",
    "HZ", "HA", "HC", "HE",
    "BG", "SP", "RE", "DD"
]

all_courses = []

for prefix in PREFIXES:
    print(f"Scraping {prefix}...")

    payload = {
        "acadsem": "2025;1",
        "r_subj_code": prefix,
        "r_search_type": "F",
        "boption": "Search",
        "staff_access": "false"
    }

    response = requests.post(URL, data=payload)
    soup = BeautifulSoup(response.text, "html.parser")

    text = soup.get_text("\n")

    # Match things like:
    # SC1003 DATA STRUCTURES & ALGORITHMS 3.0
    pattern = r"([A-Z]{2}\d{4})\s+(.+?)\s+(\d+\.\d)"

    matches = re.findall(pattern, text)

    for code, name, au in matches:
        all_courses.append({
            "course_code": code.strip(),
            "course_name": name.strip(),
            "AU": float(au)
        })

# Remove duplicates
df = pd.DataFrame(all_courses)
df = df.drop_duplicates(subset=["course_code"])

# Sort nicely
df = df.sort_values("course_code")

# Save
df.to_csv("data/courses.csv", index=False)

print("\nDone.")
print(f"Saved {len(df)} courses to data/courses.csv")