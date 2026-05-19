import pandas as pd

# Load data
df = pd.read_csv("data/courses.csv")

print("\n=== NTU Academic Data Observatory ===\n")

# -------------------------
# Basic stats
# -------------------------
print("Total courses:", len(df))

df["prefix"] = df["course_code"].str.extract(r"([A-Z]+)")

print("\nCourses by department:")
print(df["prefix"].value_counts())

# -------------------------
# Specialization buckets
# -------------------------

AI_KEYWORDS = [
    "MACHINE LEARNING",
    "NEURAL",
    "ARTIFICIAL INTELLIGENCE",
    "NATURAL LANGUAGE",
    "COMPUTER VISION",
    "DATA ANALYTICS",
    "DATA VISUALISATION",
]

SYSTEMS_KEYWORDS = [
    "OPERATING SYSTEMS",
    "SOFTWARE",
    "DATABASE",
    "NETWORK",
    "ARCHITECTURE",
    "PARALLEL",
    "COMPILER",
]

SECURITY_KEYWORDS = [
    "SECURITY",
    "CRYPTO",
    "CYBER",
    "BLOCKCHAIN",
]

def find_courses(keywords):
    pattern = "|".join(keywords)
    return df[
        df["course_name"].str.upper().str.contains(pattern)
    ][["course_code", "course_name"]]

# -------------------------
# Print specialization paths
# -------------------------

print("\n=== AI / ML Track ===")
print(find_courses(AI_KEYWORDS).to_string(index=False))

print("\n=== Software Systems Track ===")
print(find_courses(SYSTEMS_KEYWORDS).to_string(index=False))

print("\n=== Cybersecurity Track ===")
print(find_courses(SECURITY_KEYWORDS).to_string(index=False))