import pandas as pd

# Load data
df = pd.read_csv("data/courses.csv")

print("\n=== NTU Specialization Recommender ===\n")
print("Answer with yes/no.\n")

likes_math = input("Do you enjoy math-heavy subjects? ").lower()
likes_coding = input("Do you enjoy building software systems? ").lower()
likes_security = input("Are you interested in security / hacking? ").lower()
likes_ai = input("Are you interested in AI / machine learning? ").lower()

# Keyword sets
AI_KEYWORDS = [
    "MACHINE LEARNING",
    "NEURAL",
    "ARTIFICIAL INTELLIGENCE",
    "NATURAL LANGUAGE",
    "COMPUTER VISION",
    "DATA ANALYTICS",
]

SYSTEMS_KEYWORDS = [
    "OPERATING SYSTEMS",
    "SOFTWARE",
    "DATABASE",
    "NETWORK",
    "ARCHITECTURE",
]

SECURITY_KEYWORDS = [
    "SECURITY",
    "CRYPTO",
    "CYBER",
    "BLOCKCHAIN",
]

def get_courses(keywords):
    pattern = "|".join(keywords)
    return df[
    (df["course_name"].str.upper().str.contains(pattern)) &
    (df["course_code"].str.startswith("SC"))
    ][["course_code", "course_name"]]

print("\n--- Recommendation ---\n")

if likes_ai == "yes" and likes_math == "yes":
    print("Recommended Track: AI / Machine Learning\n")
    print(get_courses(AI_KEYWORDS).to_string(index=False))

elif likes_security == "yes":
    print("Recommended Track: Cybersecurity\n")
    print(get_courses(SECURITY_KEYWORDS).to_string(index=False))

elif likes_coding == "yes":
    print("Recommended Track: Software Systems\n")
    print(get_courses(SYSTEMS_KEYWORDS).to_string(index=False))

else:
    print("You seem exploratory—try a mix of courses first!")