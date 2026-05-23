import streamlit as st
import pandas as pd
import json

# ====================================================
# PAGE SETUP
# ====================================================

st.set_page_config(
    page_title="NTU Degree Navigator",
    layout="wide"
)

st.title("🎓 NTU Degree Navigator")
st.write("Plan your NTU degree smarter.")

# ====================================================
# LOAD COURSE DATA
# ====================================================

try:
    df = pd.read_csv("data/courses.csv")
except:
    st.error("Could not load data/courses.csv")
    st.stop()

# Use ALL courses
all_df = df.copy()

# Add default AU column if missing
if "AU" not in all_df.columns:
    all_df["AU"] = 3

# Better display label
all_df["display"] = (
    all_df["course_code"]
    + " — "
    + all_df["course_name"]
)

# ====================================================
# LOAD DEGREE REQUIREMENTS
# ====================================================

try:
    with open("data/degree_requirements.json") as f:
        degree_data = json.load(f)
except:
    st.error(
        "Could not load data/degree_requirements.json"
    )
    st.stop()

# ====================================================
# LOAD SPECIALIZATION DATA
# ====================================================

try:
    with open("data/specializations.json") as f:
        specializations = json.load(f)
except:
    st.error(
        "Could not load data/specializations.json"
    )
    st.stop()

# ====================================================
# STUDENT PROFILE
# ====================================================

st.header("👤 Your NTU Profile")

degree = st.selectbox(
    "Select your degree programme",
    list(degree_data.keys())
)

year = st.selectbox(
    "Current study year",
    ["Y1", "Y2", "Y3", "Y4", "Y5"]
)

# Load selected degree requirements
requirements = degree_data[degree]

# ====================================================
# COMPLETED COURSES
# ====================================================

st.header("✅ Mark Completed Courses")

completed_display = st.multiselect(
    "Completed courses",
    options=all_df["display"].tolist()
)

completed_codes = [
    item.split(" — ")[0]
    for item in completed_display
]

completed_df = all_df[
    all_df["course_code"].isin(completed_codes)
]

completed_au = completed_df["AU"].sum()

st.write(f"### Completed AU: {completed_au}")

# ====================================================
# DEGREE PROGRESS
# ====================================================

st.header("📊 Degree Progress")

degree_requirement = requirements["total_au"]

progress = min(
    completed_au / degree_requirement,
    1.0
)

st.write(
    f"### Total AU Progress: "
    f"{completed_au}/{degree_requirement}"
)

st.progress(progress)

# ====================================================
# CURRICULUM TRACKER
# ====================================================

st.header("📚 Curriculum Checklist")

for category, value in requirements.items():

    # Skip non-list items
    if not isinstance(value, list):
        continue

    completed = [
        code for code in value
        if code in completed_codes
    ]

    remaining = [
        code for code in value
        if code not in completed_codes
    ]

    st.subheader(
        category.replace("_", " ").title()
    )

    st.write(
        f"Completed: "
        f"{len(completed)}/{len(value)}"
    )

    category_progress = (
        len(completed) / len(value)
        if len(value) > 0
        else 0
    )

    st.progress(category_progress)

    # Completed list
    if completed:
        st.success(
            "Completed: "
            + ", ".join(completed)
        )

    # Remaining list
    if remaining:
        st.warning(
            "Remaining: "
            + ", ".join(remaining)
        )
    else:
        st.success("All completed!")

# ====================================================
# CAREER & SPECIALIZATION EXPLORER
# ====================================================

st.header("🚀 Career & Specialization Explorer")

career_path = st.selectbox(
    "Which path are you interested in?",
    [
        "Artificial Intelligence / ML",
        "Software Engineering",
        "Cybersecurity",
        "Data Science",
        "Quant / Finance Tech",
        "Research / Academia"
    ]
)

# ====================================================
# AI / ML
# ====================================================

if career_path == "Artificial Intelligence / ML":

    st.subheader("🧠 AI / ML Path")

    st.write(
        """
        Best for students who enjoy:
        - Math
        - Coding
        - Data
        - Building intelligent systems
        """
    )

    st.subheader("💼 Typical Careers")

    st.write("""
    - ML Engineer
    - AI Engineer
    - Data Scientist
    - NLP Engineer
    - Computer Vision Engineer
    - AI Researcher
    """)

    st.subheader("📚 Recommended NTU Courses")

    st.write("""
    - SC3000 Artificial Intelligence
    - SC4000 Machine Learning
    - SC4001 Neural Network & Deep Learning
    - SC4002 Natural Language Processing
    - SC4061 Computer Vision
    - SC4020 Data Analytics & Mining
    """)

    st.subheader("🛠️ Skills To Build")

    st.write("""
    - Python
    - PyTorch / TensorFlow
    - Data Structures & Algorithms
    - Math & Statistics
    - SQL
    - Model Deployment
    """)

    st.subheader("📈 Internship Roles")

    st.write("""
    - AI Intern
    - Data Science Intern
    - ML Engineer Intern
    - Analytics Intern
    """)

# ====================================================
# SOFTWARE ENGINEERING
# ====================================================

elif career_path == "Software Engineering":

    st.subheader("💻 Software Engineering Path")

    st.write("""
    Best for students who enjoy:
    - Building applications
    - System design
    - Backend/frontend engineering
    - Product development
    """)

    st.subheader("💼 Typical Careers")

    st.write("""
    - Software Engineer
    - Backend Engineer
    - Full Stack Developer
    - Platform Engineer
    - Mobile Developer
    """)

    st.subheader("📚 Recommended NTU Courses")

    st.write("""
    - SC2005 Operating Systems
    - SC2006 Software Engineering
    - SC2207 Introduction to Databases
    - SC3020 Database Systems
    - SC3040 Advanced Software Engineering
    - SC3030 Advanced Computer Networks
    """)

    st.subheader("🛠️ Skills To Build")

    st.write("""
    - Full-stack development
    - System design
    - APIs
    - Cloud computing
    - Git/GitHub
    - React / Node.js
    """)

    st.subheader("📈 Internship Roles")

    st.write("""
    - SWE Intern
    - Backend Intern
    - Full Stack Intern
    - Platform Engineering Intern
    """)

# ====================================================
# CYBERSECURITY
# ====================================================

elif career_path == "Cybersecurity":

    st.subheader("🔐 Cybersecurity Path")

    st.write("""
    Best for students interested in:
    - Security
    - Hacking
    - Networks
    - Cryptography
    """)

    st.subheader("💼 Typical Careers")

    st.write("""
    - Security Engineer
    - Penetration Tester
    - SOC Analyst
    - Threat Intelligence Analyst
    """)

    st.subheader("📚 Recommended NTU Courses")

    st.write("""
    - SC3010 Computer Security
    - SC4010 Applied Cryptography
    - SC4016 Cyber Threat Intelligence
    - SC4053 Blockchain Technology
    """)

    st.subheader("🛠️ Skills To Build")

    st.write("""
    - Linux
    - Networking
    - Cryptography
    - Web security
    - CTFs
    """)

# ====================================================
# DATA SCIENCE
# ====================================================

elif career_path == "Data Science":

    st.subheader("📊 Data Science Path")

    st.write("""
    Strong fit for students who enjoy:
    - Statistics
    - Analytics
    - Business insights
    - Data storytelling
    """)

    st.subheader("📚 Recommended NTU Courses")

    st.write("""
    - SC4020 Data Analytics & Mining
    - SC4024 Data Visualisation
    - SC4000 Machine Learning
    - MH1812 Discrete Mathematics
    """)

    st.subheader("💼 Typical Careers")

    st.write("""
    - Data Scientist
    - Data Analyst
    - BI Analyst
    - Analytics Consultant
    """)

# ====================================================
# QUANT
# ====================================================

elif career_path == "Quant / Finance Tech":

    st.subheader("📈 Quant / Finance Tech")

    st.write("""
    Great for students who enjoy:
    - Math
    - Statistics
    - Finance
    - Algorithms
    """)

    st.subheader("📚 Recommended NTU Courses")

    st.write("""
    - SC2000 Probability & Statistics
    - MH1812 Discrete Mathematics
    - SC4020 Data Analytics
    - HE courses
    """)

    st.subheader("💼 Careers")

    st.write("""
    - Quant Analyst
    - Quant Developer
    - FinTech Engineer
    - Trading Systems Engineer
    """)

# ====================================================
# RESEARCH
# ====================================================

elif career_path == "Research / Academia":

    st.subheader("🔬 Research & Academia")

    st.write("""
    Best for students interested in:
    - Deep technical work
    - Publishing papers
    - Masters / PhD
    - Advanced AI systems
    """)

    st.subheader("📚 Recommended NTU Courses")

    st.write("""
    - SC4001 Neural Networks
    - SC4002 NLP
    - SC4061 Computer Vision
    - Advanced math/statistics modules
    """)

    st.subheader("💼 Pathways")

    st.write("""
    - Undergraduate research
    - PhD track
    - Research labs
    - AI research internships
    """)

# ====================================================
# FUTURE COURSE PLANNING
# ====================================================

st.header("🗓️ Plan Future Courses")

planned_display = st.multiselect(
    "Select planned future courses",
    options=all_df["display"].tolist()
)

planned_codes = [
    item.split(" — ")[0]
    for item in planned_display
]

planned_df = all_df[
    all_df["course_code"].isin(planned_codes)
]

planned_au = planned_df["AU"].sum()

st.write(f"### Planned AU: {planned_au}")

# Semester load warning
if planned_au > 24:
    st.error(
        "⚠️ Heavy overload semester detected!"
    )

elif planned_au > 18:
    st.warning(
        "⚠️ Moderately heavy semester load."
    )

else:
    st.success(
        "✅ Reasonable semester workload."
    )

# ====================================================
# SHOW SELECTED COURSE DETAILS
# ====================================================

st.header("📖 Selected Course Details")

display_df = pd.concat(
    [completed_df, planned_df]
).drop_duplicates()

display_df = display_df.reset_index(drop=True)
display_df.index += 1

st.dataframe(display_df)

# ====================================================
# BROWSE ALL COURSES
# ====================================================

st.header("🔍 Browse All NTU Courses")

search = st.text_input(
    "Search by course code or course name"
)

filtered = all_df.copy()

if search:

    filtered = filtered[
        filtered["course_code"].str.contains(
            search,
            case=False
        )
        |
        filtered["course_name"].str.contains(
            search,
            case=False
        )
    ]

filtered = filtered.reset_index(drop=True)
filtered.index += 1

st.dataframe(filtered)