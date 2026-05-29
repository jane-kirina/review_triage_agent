# Streamlit entry point
import streamlit as st

from src.db.queries import (
    get_apps,
    get_dataset_overview,
    get_reviews_by_app,
    get_review_score_distribution,
    get_top_apps_by_review_count
)


st.set_page_config(
    page_title="Review Triage Agent",
    layout="wide"
)

st.title("Review Triage Agent")
st.subheader("LLM-powered app review triage tool")

# -----------------------
# Dataset overview
# Shows general statistics from PostgreSQL:
# - number of applications
# - reviews considered
# - average score by reviews

st.header(" - Dataset overview - ")

overview_df = get_dataset_overview()

if overview_df.empty:
    st.warning("No data found in database")
    st.stop()

overview = overview_df.iloc[0]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Apps", int(overview["apps_count"]))

with col2:
    st.metric("Reviews", int(overview["reviews_count"]))

with col3:
    avg_score = overview["avg_review_score"]
    st.metric("Average review score", avg_score if avg_score is not None else "N/A")

st.subheader("Top apps by review count")
top_apps_df = get_top_apps_by_review_count(limit=10)

top_apps_df = top_apps_df.rename(
    columns={
        "app_name": "App name",
        "reviews_count": "Reviews count",
        "avg_review_score": "Average review score"
    }
)
st.dataframe(top_apps_df, use_container_width=True, hide_index=True)

# -----------------------
# Select app

st.header(" - Select app - ")

apps_df = get_apps(limit=300)

if apps_df.empty:
    st.warning("No apps found in database")
    st.stop()

st.dataframe(
    apps_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "app_id": "App ID",
        "app_name": "App name",
        "score": "Score",
        "downloads": "Downloads",
        "categories": "Categories"
    },
)

app_options = dict(zip(apps_df["app_name"], apps_df["app_id"]))

selected_app_name = st.selectbox(
    "Choose app",
    options=list(app_options.keys()),
)

selected_app_id = app_options[selected_app_name]

selected_app_row = apps_df[apps_df["app_id"] == selected_app_id].iloc[0]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("App score", selected_app_row["score"])

with col2:
    st.metric("Downloads", selected_app_row["downloads"])

with col3:
    st.metric("Score", selected_app_row["score"])

# -----------------------
# Reviews preview
# Shows reviews only for the selected app
# TODO placeholder

st.header(" - Reviews preview - ")

reviews_limit = st.slider(
    "Number of reviews to preview",
    min_value=10,
    max_value=100,
    value=50,
    step=10
)

reviews_df = get_reviews_by_app(
    app_id=selected_app_id,
    limit=reviews_limit
)

score_distribution_df = get_review_score_distribution(selected_app_id)

left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader(f"Reviews for {selected_app_name}")

    if reviews_df.empty:
        st.warning("No reviews found for this app")
    else:
        st.dataframe(reviews_df, use_container_width=True)

with right_col:
    st.subheader("Score distribution")

    if score_distribution_df.empty:
        st.info("No score data available")
    else:
        chart_df = score_distribution_df.set_index("review_score")
        st.bar_chart(chart_df)


# -----------------------------
# Run triage
# TODO placeholder

st.header(" - Run triage - ")

st.info(
    "This section will later run the LangGraph review analysis workflow"
)

triage_sample_size = st.slider(
    "Number of reviews to analyze later",
    min_value=10,
    max_value=200,
    value=50,
    step=10
)

if st.button("Analyze reviews"):
    st.session_state["triage_requested"] = True
    st.session_state["selected_app_id"] = selected_app_id
    st.session_state["selected_app_name"] = selected_app_name
    st.session_state["triage_sample_size"] = triage_sample_size

    st.success(
        f"Triage placeholder triggered for {triage_sample_size} reviews "
        f"from {selected_app_name}"
    )


# -----------------------------
# Results dashboard
# - category
# - sentiment
# - severity
# - topic
# - summary
# - suggested_action
# - confidence

st.header(" - Results dashboard -")

if "triage_requested" not in st.session_state:
    st.warning("No triage results yet. Run analysis first")
else:
    st.write("Selected app:", st.session_state["selected_app_name"])
    st.write("Sample size:", st.session_state["triage_sample_size"])

    st.info(
        "Triage results will appear here after the LLM/LangGraph pipeline is implemented"
    )

    empty_results = {
        "review_id": [],
        "category": [],
        "sentiment": [],
        "severity": [],
        "topic": [],
        "summary": [],
        "suggested_action": [],
        "confidence": []
    }

    st.dataframe(empty_results, use_container_width=True)

