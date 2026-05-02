import streamlit as st
import pandas as pd
import sqlalchemy

engine = sqlalchemy.create_engine("postgresql+psycopg2://itc6050:itc6050@localhost:5432/lab")

st.title("🐙 GitHub Issues — Repo Comparison")

df = pd.read_sql("SELECT * FROM analytics.stg_github_issues", engine)

# Sidebar filter
repos = df["repo"].unique().tolist()
selected = st.multiselect("Select repos to compare", repos, default=repos)
df = df[df["repo"].isin(selected)]

# Side-by-side metrics
cols = st.columns(len(selected))
for col, repo in zip(cols, selected):
    subset = df[df["repo"] == repo]
    col.metric(label=repo, value=f"{len(subset)} issues")

st.subheader("Issues by state")
summary = (
    df.groupby(["repo", "state"])
    .size()
    .reset_index(name="count")
)
st.bar_chart(summary, x="state", y="count", color="repo")

st.subheader("Top authors per repo")
for repo in selected:
    st.markdown(f"**{repo}**")
    top = (
        df[df["repo"] == repo]
        .groupby("author")
        .size()
        .reset_index(name="issues")
        .sort_values("issues", ascending=False)
        .head(5)
    )
    st.dataframe(top, hide_index=True)