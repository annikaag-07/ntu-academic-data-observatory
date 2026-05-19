import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


# NTU schedule page
URL = "https://wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1"


def fetch_course_schedule():
    # Search for ALL SC courses (full-time)
    payload = {
        "acadsem": "2025;1",
        "r_subj_code": "SC",
        "r_search_type": "F",
        "boption": "Search",
        "staff_access": "false"
    }

    response = requests.post(URL, data=payload)
    response.raise_for_status()
    return response.text


def parse_courses(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text("\n")

    # Split text into clean lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    courses = []

    i = 0
    while i < len(lines) - 1:
        # Match course codes like SC1005, SC2001, CZ3006
        if re.match(r"^[A-Z]{2,3}\d{4}$", lines[i]):
            code = lines[i]
            name = lines[i + 1]

            # Skip bad captures like "INDEX"
            if name == "INDEX":
                i += 1
                continue

            courses.append({
                "course_code": code,
                "course_name": name
            })

            i += 2
        else:
            i += 1

    return pd.DataFrame(courses)


def main():
    print("Fetching NTU courses...")
    
    html = fetch_course_schedule()

    print("Parsing courses...")
    
    df = parse_courses(html)

    output_path = "data/courses.csv"
    df.to_csv(output_path, index=False)

    print(f"Saved to {output_path}")
    print(df.head())


if __name__ == "__main__":
    main()