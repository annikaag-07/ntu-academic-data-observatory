import streamlit as st
import pandas as pd

# -------------------------
# Page setup
# -------------------------
st.set_page_config(page_title="NTU Degree Navigator")
st.title("🎓 NTU Degree Navigator")
st.write("Plan your next courses smarter.")

# -------------------------
# Load course data
# -------------------------
try:
    df = pd.read_csv("data/courses.csv")
except:
    st.error("Could not load data/courses.csv")
    st.stop()

# Use ALL courses
all_df = df.copy()

# Add default AU column if not present
if "AU" not in all_df.columns:
    all_df["AU"] = 3

# -------------------------
# Sidebar
# -------------------------
st.sidebar.header("Choose Mode")

mode = st.sidebar.radio(
    "What do you want?",
    [
        "Track Recommendation",
        "Browse All Courses",
        "Degree Planner",
    ]
)

# ====================================================
# MODE 1: Track Recommendation
# ====================================================
if mode == "Track Recommendation":

    st.header("Find your best specialization")

    user_input = st.text_area(
        "Tell me your interests:",
        placeholder="I like math and coding, dislike hardware, want good internships..."
    )

    if st.button("Get Recommendation"):

        text = user_input.lower()

        # AI / ML
        if any(word in text for word in [
            "ai",
            "machine learning",
            "ml",
            "math",
            "data",
            "coding",
            "internship"
        ]):

            st.success("Recommended: AI / Machine Learning")

            st.subheader("Why this fits you")
            st.write("✅ Strong math foundation")
            st.write("✅ Great internship opportunities")
            st.write("✅ Less hardware-focused")

            st.subheader("Suggested Courses")
            st.write("- SC3000 Artificial Intelligence")
            st.write("- SC4000 Machine Learning")
            st.write("- SC4001 Neural Network & Deep Learning")
            st.write("- SC4002 Natural Language Processing")
            st.write("- SC4061 Computer Vision")

        # Cybersecurity
        elif any(word in text for word in [
            "security",
            "cyber",
            "hacking",
            "cryptography"
        ]):

            st.success("Recommended: Cybersecurity")

            st.subheader("Why this fits you")
            st.write("✅ Strong industry demand")
            st.write("✅ Great for problem-solvers")
            st.write("✅ Hands-on practical learning")

            st.subheader("Suggested Courses")
            st.write("- SC3010 Computer Security")
            st.write("- SC4010 Applied Cryptography")
            st.write("- SC4016 Cyber Threat Intelligence")
            st.write("- SC4053 Blockchain Technology")

        # Software systems
        else:

            st.success("Recommended: Software Systems")

            st.subheader("Why this fits you")
            st.write("✅ Best for software engineering roles")
            st.write("✅ Strong internship opportunities")
            st.write("✅ Broadest technical foundation")

            st.subheader("Suggested Courses")
            st.write("- SC2005 Operating Systems")
            st.write("- SC2006 Software Engineering")
            st.write("- SC2008 Computer Network")
            st.write("- SC3020 Database Systems")
            st.write("- SC3040 Advanced Software Engineering")


# ====================================================
# MODE 2: Browse All Courses
# ====================================================
elif mode == "Browse All Courses":

    st.header("Browse NTU Courses")

    search = st.text_input(
        "Search by course code or name"
    )

    filtered = all_df.copy()

    if search:
        filtered = filtered[
            filtered["course_code"].str.contains(search, case=False)
            |
            filtered["course_name"].str.contains(search, case=False)
        ]

    # reset numbering to start at 1
    filtered = filtered.reset_index(drop=True)
    filtered.index = filtered.index + 1

    st.dataframe(filtered)


# ====================================================
# MODE 3: Degree Planner
# ====================================================
elif mode == "Degree Planner":

    st.header("Plan Your Degree")

    # Create nicer searchable labels
    all_df["display"] = (
        all_df["course_code"] + " — " + all_df["course_name"]
    )

    # -------------------------
    # Completed courses
    # -------------------------
    st.subheader("1. Mark completed courses")

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

    # -------------------------
    # Planned courses
    # -------------------------
    st.subheader("2. Select future courses")

    planned_display = st.multiselect(
        "Planned courses",
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

    # -------------------------
    # Progress
    # -------------------------
    total_au = completed_au + planned_au

    st.subheader("3. Progress Summary")

    degree_requirement = 137

    st.write(
        f"**Total AU accounted for:** "
        f"{total_au}/{degree_requirement}"
    )

    progress = min(
        total_au / degree_requirement,
        1.0
    )

    st.progress(progress)

    # -------------------------
    # Show selected courses
    # -------------------------
    st.subheader("Selected Course Details")

    display_df = pd.concat(
        [completed_df, planned_df]
    ).drop_duplicates()

    display_df = display_df.reset_index(
        drop=True
    )

    display_df.index += 1

    st.dataframe(display_df)