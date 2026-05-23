import os
import pandas as pd
from google import genai


# -------------------------------
# STEP 1: Load API key
# -------------------------------
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("Error: GEMINI_API_KEY not found.")
    print("Run this first:")
    print('export GEMINI_API_KEY="YOUR_API_KEY_HERE"')
    exit()

client = genai.Client(api_key=API_KEY)


# -------------------------------
# STEP 2: Load course data
# -------------------------------
try:
    df = pd.read_csv("data/courses.csv")
    print("✅ Loaded course file successfully!")
except Exception as e:
    print("Error loading course file:")
    print(e)
    exit()

# Keep only SC courses
sc_df = df[df["course_code"].str.startswith("SC")]


# -------------------------------
# STEP 3: Ask user
# -------------------------------
print("\n=== NTU Gemini Course Advisor ===\n")

user_input = input(
    "Tell me your interests / confusion about specialization:\n"
)


# -------------------------------
# STEP 4: Build Gemini prompt
# -------------------------------
prompt = f"""
You are an NTU Computer Science academic advisor.

Available computing courses:

{sc_df.to_string(index=False)}

Student says:
{user_input}

Your task:
1. Recommend ONE specialization track
2. Explain WHY it fits
3. Suggest 4-5 useful courses

Keep it concise and friendly.
"""


# -------------------------------
# STEP 5: Try Gemini first
# -------------------------------
try:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )

    print("\n=== Gemini Recommendation ===\n")
    print(response.text)


# -------------------------------
# STEP 6: Fallback local advisor
# -------------------------------
except Exception:
    print("\nGemini is currently unavailable (API quota exceeded).")
    print("Using local NTU advisor instead...\n")

    text = user_input.lower()

    # AI / ML track
    if any(word in text for word in [
        "ai",
        "machine learning",
        "ml",
        "math",
        "data",
        "coding",
        "internship",
    ]):
        print("Recommended Track: AI / Machine Learning\n")

        print("Why this fits you:")
        print("- Strong math foundation helps in ML")
        print("- High internship demand in AI/Data roles")
        print("- Less hardware-focused, more software + problem solving\n")

        print("Suggested Courses:")
        print("- SC3000 Artificial Intelligence")
        print("- SC4000 Machine Learning")
        print("- SC4001 Neural Network & Deep Learning")
        print("- SC4002 Natural Language Processing")
        print("- SC4061 Computer Vision")

    # Cybersecurity track
    elif any(word in text for word in [
        "security",
        "cyber",
        "hacking",
        "cryptography",
    ]):
        print("Recommended Track: Cybersecurity\n")

        print("Why this fits you:")
        print("- Great for security and hacking enthusiasts")
        print("- Strong demand in industry")
        print("- Mix of systems knowledge and analytical thinking\n")

        print("Suggested Courses:")
        print("- SC3010 Computer Security")
        print("- SC4010 Applied Cryptography")
        print("- SC4016 Cyber Threat Intelligence")
        print("- SC4053 Blockchain Technology")

    # Default: Software Systems
    else:
        print("Recommended Track: Software Systems\n")

        print("Why this fits you:")
        print("- Great for software engineering internships")
        print("- Focuses on building scalable systems")
        print("- Less theoretical math, more practical coding\n")

        print("Suggested Courses:")
        print("- SC2005 Operating Systems")
        print("- SC2006 Software Engineering")
        print("- SC2008 Computer Network")
        print("- SC3020 Database Systems")
        print("- SC3040 Advanced Software Engineering")