import streamlit as st
import pandas as pd
import json

# ====================================================
# PAGE CONFIG
# ====================================================

st.set_page_config(
    page_title="NTU Degree Navigator",
    page_icon="🎓",
    layout="wide"
)

# ====================================================
# CUSTOM CSS
# ====================================================

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

.block-container {
    padding-top: 2rem;
}

h1, h2, h3 {
    color: white;
}

div[data-testid="metric-container"] {
    background-color: #161b22;
    border: 1px solid #30363d;
    padding: 15px;
    border-radius: 15px;
}

div[data-testid="stProgressBar"] > div > div > div {
    background-color: #00c2ff;
}

.st-emotion-cache-1v0mbdj {
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

# ====================================================
# LOAD DATA
# ====================================================

try:
    df = pd.read_csv("data/courses.csv")
except:
    st.error("Could not load data/courses.csv")
    st.stop()

try:
    with open("data/degree_requirements.json") as f:
        degree_data = json.load(f)
except:
    st.error("Could not load degree_requirements.json")
    st.stop()

try:
    with open("data/prerequisites.json") as f:
        prerequisites = json.load(f)
except:
    st.error("Could not load prerequisites.json")
    st.stop()

try:
    with open("data/roadmaps.json") as f:
        roadmaps = json.load(f)
except:
    st.error("Could not load roadmaps.json")
    st.stop()

try:
    with open("data/specializations.json") as f:
        specializations = json.load(f)
except:
    st.error("Could not load specializations.json")
    st.stop()

# ====================================================
# PREP DATA
# ====================================================

all_df = df.copy()

if "AU" not in all_df.columns:
    all_df["AU"] = 3

all_df["display"] = (
    all_df["course_code"]
    + " — "
    + all_df["course_name"]
)

# ====================================================
# SIDEBAR
# ====================================================

with st.sidebar:

    st.title("🎓 NTU Navigator")

    st.markdown("---")

    st.header("👤 Student Profile")

    degree = st.selectbox(
        "Degree Programme",
        list(degree_data.keys())
    )

    year = st.selectbox(
        "Current Year",
        ["Y1", "Y2", "Y3", "Y4", "Y5"]
    )

    semester = st.selectbox(
        "Current Semester",
        ["Semester 1", "Semester 2"]
    )

    career_path = st.selectbox(
        "Career Interest",
        [
            "Artificial Intelligence / ML",
            "Software Engineering",
            "Cybersecurity",
            "Data Science",
            "Quant / Finance Tech",
            "Research / Academia"
        ]
    )

requirements = degree_data[degree]

# ====================================================
# TITLE
# ====================================================

st.title("🎓 NTU Degree Navigator")

st.caption(
    "Smart academic planning for NTU students"
)

# ====================================================
# TABS
# ====================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dashboard",
    "🧠 Career Explorer",
    "📚 Degree Planner",
    "🔍 Course Browser"
])

# ====================================================
# TAB 1 — DASHBOARD
# ====================================================

with tab1:

    st.header("📊 Academic Dashboard")

    st.subheader("✅ Completed Courses")

    completed_display = st.multiselect(
        "Select completed modules",
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

    total_required = requirements["total_au"]

    progress = min(
        completed_au / total_required,
        1.0
    )

    remaining_au = (
        total_required - completed_au
    )

    # ====================================================
    # METRICS
    # ====================================================

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Completed AU",
            completed_au
        )

    with col2:
        st.metric(
            "Remaining AU",
            remaining_au
        )

    with col3:
        st.metric(
            "Graduation Progress",
            f"{round(progress * 100)}%"
        )

    st.progress(progress)

    # ====================================================
    # CURRICULUM TRACKER
    # ====================================================

    st.markdown("---")

    st.subheader("📚 Curriculum Progress")

    for category, value in requirements.items():

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

        with st.container(border=True):

            st.markdown(
                f"### {category.replace('_', ' ').title()}"
            )

            category_progress = (
                len(completed) / len(value)
                if len(value) > 0
                else 0
            )

            st.progress(category_progress)

            st.write(
                f"Completed: "
                f"{len(completed)}/{len(value)}"
            )

            if remaining:

                st.warning(
                    "Remaining: "
                    + ", ".join(remaining)
                )

            else:

                st.success(
                    "All requirements completed!"
                )

    # ====================================================
    # OFFICIAL NTU ROADMAP
    # ====================================================

    st.markdown("---")

    st.header("📚 Official NTU Semester Roadmap")

    semester_key = (
        year
        + semester.replace("Semester ", "S")
    )

    degree_roadmap = roadmaps.get(
        degree,
        {}
    )

    recommended_sem = degree_roadmap.get(
        semester_key,
        []
    )

    if recommended_sem:

        st.success(
            f"Recommended modules for {semester_key}"
        )

        for course in recommended_sem:

            row = all_df[
                all_df["course_code"] == course
            ]

            if not row.empty:

                name = row.iloc[0]["course_name"]

                with st.container(border=True):

                    st.markdown(f"### {course}")

                    st.write(name)

                    if course in completed_codes:

                        st.success(
                            "✅ Already completed"
                        )

    else:

        st.warning(
            "No roadmap available yet."
        )

    # ====================================================
    # SMART RECOMMENDATIONS
    # ====================================================

    st.markdown("---")

    st.header("🧠 Recommended Next Courses")

    recommended = []

    # ====================================================
    # CAREER TRACK COURSE TARGETS
    # ====================================================

    if career_path == "Artificial Intelligence / ML":

        target_courses = [
            "SC3000",
            "SC4000",
            "SC4001",
            "SC4002",
            "SC4061",
            "SC4020"
        ]

    elif career_path == "Software Engineering":

        target_courses = [
            "SC2005",
            "SC2006",
            "SC2207",
            "SC3020",
            "SC3040"
        ]

    elif career_path == "Cybersecurity":

        target_courses = [
            "SC3010",
            "SC4010",
            "SC4016",
            "SC4053"
        ]

    elif career_path == "Data Science":

        target_courses = [
            "SC4020",
            "SC4024",
            "SC4000"
        ]

    elif career_path == "Quant / Finance Tech":

        target_courses = [
            "SC2000",
            "SC4020",
            "SC4000"
        ]

    else:

        target_courses = [
            "SC4001",
            "SC4002",
            "SC4061"
        ]

    # ====================================================
    # CHECK ELIGIBILITY
    # ====================================================

    for course in target_courses:

        if course in completed_codes:
            continue

        prereqs = prerequisites.get(course, [])

        eligible = all(
            prereq in completed_codes
            for prereq in prereqs
        )

        if eligible:
            recommended.append(course)

    # ====================================================
    # DISPLAY RECOMMENDATIONS
    # ====================================================

    if recommended:

        st.success(
            "Recommended based on your profile"
        )

        for course in recommended:

            row = all_df[
                all_df["course_code"] == course
            ]

            if not row.empty:

                name = row.iloc[0]["course_name"]

                with st.container(border=True):

                    st.markdown(f"### {course}")

                    st.write(name)

                    prereqs = prerequisites.get(
                        course,
                        []
                    )

                    if prereqs:

                        st.caption(
                            "Prerequisites: "
                            + ", ".join(prereqs)
                        )

    else:

        st.warning(
            "No eligible recommendations yet."
        )

# ====================================================
# TAB 2 — CAREER EXPLORER
# ====================================================

with tab2:

    st.header("🚀 Career Explorer")

    if career_path == "Artificial Intelligence / ML":

        st.subheader("🧠 AI / ML")

        with st.expander("💼 Career Roles"):

            st.write("""
            - ML Engineer
            - AI Engineer
            - Data Scientist
            - NLP Engineer
            - Computer Vision Engineer
            """)

        with st.expander("📚 Recommended NTU Courses"):

            st.write("""
            - SC3000 Artificial Intelligence
            - SC4000 Machine Learning
            - SC4001 Deep Learning
            - SC4002 NLP
            - SC4061 Computer Vision
            """)

        with st.expander("🛠️ Skills To Learn"):

            st.write("""
            - Python
            - PyTorch
            - TensorFlow
            - SQL
            - Statistics
            - Model Deployment
            """)

    elif career_path == "Software Engineering":

        st.subheader("💻 Software Engineering")

        with st.expander("💼 Career Roles"):

            st.write("""
            - Software Engineer
            - Backend Engineer
            - Full Stack Developer
            - Platform Engineer
            """)

        with st.expander("📚 Recommended NTU Courses"):

            st.write("""
            - SC2005 Operating Systems
            - SC2006 Software Engineering
            - SC2207 Databases
            - SC3020 Database Systems
            """)

        with st.expander("🛠️ Skills To Learn"):

            st.write("""
            - React
            - Node.js
            - APIs
            - Git/GitHub
            - Cloud Computing
            """)

    elif career_path == "Cybersecurity":

        st.subheader("🔐 Cybersecurity")

        with st.expander("💼 Career Roles"):

            st.write("""
            - Security Engineer
            - SOC Analyst
            - Threat Analyst
            - Penetration Tester
            """)

        with st.expander("📚 Recommended NTU Courses"):

            st.write("""
            - SC3010 Computer Security
            - SC4010 Cryptography
            - SC4016 Threat Intelligence
            """)

    elif career_path == "Data Science":

        st.subheader("📊 Data Science")

        with st.expander("💼 Career Roles"):

            st.write("""
            - Data Scientist
            - Data Analyst
            - BI Analyst
            """)

        with st.expander("📚 Recommended Courses"):

            st.write("""
            - SC4020 Data Analytics
            - SC4024 Data Visualisation
            - SC4000 Machine Learning
            """)

# ====================================================
# TAB 3 — DEGREE PLANNER
# ====================================================

with tab3:

    st.header("📚 Semester Planning")

    planned_display = st.multiselect(
        "Select planned courses",
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

    st.metric(
        "Planned AU",
        planned_au
    )

    # ====================================================
    # OVERLOAD WARNINGS
    # ====================================================

    if planned_au > 24:

        st.error(
            "⚠️ Extremely heavy semester."
        )

    elif planned_au > 18:

        st.warning(
            "⚠️ Moderately heavy semester."
        )

    else:

        st.success(
            "✅ Reasonable workload."
        )

    # ====================================================
    # PREREQUISITE CHECKER
    # ====================================================

    st.markdown("---")

    st.subheader("🚨 Invalid Plan Detection")

    invalid = False

    for course in planned_codes:

        prereqs = prerequisites.get(
            course,
            []
        )

        missing = [
            prereq for prereq in prereqs
            if prereq not in completed_codes
        ]

        if missing:

            invalid = True

            st.error(
                f"{course} missing prerequisites: "
                + ", ".join(missing)
            )

    if not invalid:

        st.success(
            "All planned courses satisfy prerequisites!"
        )

# ====================================================
# TAB 4 — COURSE BROWSER
# ====================================================

with tab4:

    st.header("🔍 Browse NTU Courses")

    search = st.text_input(
        "Search course code or course name"
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

    st.dataframe(
        filtered,
        use_container_width=True
    )