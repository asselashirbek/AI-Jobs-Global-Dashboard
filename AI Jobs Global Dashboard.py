import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("🌍 AI Jobs Global Dashboard")

uploaded_file = st.file_uploader("Upload your AI Jobs CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # Sidebar filters
    st.sidebar.header("Filter the dataset")
    job_titles = st.sidebar.multiselect("Job Title", sorted(df['job_title'].dropna().unique()))
    experience = st.sidebar.multiselect("Experience Level", sorted(df['experience_level'].dropna().unique()))
    employment = st.sidebar.multiselect("Employment Type", sorted(df['employment_type'].dropna().unique()))
    locations = st.sidebar.multiselect("Company Location", sorted(df['company_location'].dropna().unique()))
    remote = st.sidebar.slider("Remote Ratio (%)", 0, 100, (0, 100), step=10)
    company_size = st.sidebar.multiselect("Company Size", sorted(df['company_size'].dropna().unique()))
    currency = st.sidebar.multiselect("Salary Currency", sorted(df['salary_currency'].dropna().unique()))

    # Apply filters
    filtered_df = df.copy()
    if job_titles:
        filtered_df = filtered_df[filtered_df['job_title'].isin(job_titles)]
    if experience:
        filtered_df = filtered_df[filtered_df['experience_level'].isin(experience)]
    if employment:
        filtered_df = filtered_df[filtered_df['employment_type'].isin(employment)]
    if locations:
        filtered_df = filtered_df[filtered_df['company_location'].isin(locations)]
    if company_size:
        filtered_df = filtered_df[filtered_df['company_size'].isin(company_size)]
    if currency:
        filtered_df = filtered_df[filtered_df['salary_currency'].isin(currency)]
    filtered_df = filtered_df[(filtered_df['remote_ratio'] >= remote[0]) & (filtered_df['remote_ratio'] <= remote[1])]

    # Dashboard visualizations
    st.subheader("📊 Salary Distribution")
    fig1, ax1 = plt.subplots()
    sns.histplot(filtered_df['salary_usd'], kde=True, bins=30, ax=ax1)
    ax1.set_xlabel("Salary (USD)")
    st.pyplot(fig1)

    st.subheader("📈 Salary by Experience Level")
    fig2, ax2 = plt.subplots()
    sns.boxplot(x='experience_level', y='salary_usd', data=filtered_df, ax=ax2)
    st.pyplot(fig2)

    st.subheader("💼 Top 10 Job Titles")
    top_jobs = filtered_df['job_title'].value_counts().head(10)
    st.bar_chart(top_jobs)

    st.subheader("🌍 Average Salary by Company Location")
    salary_by_country = filtered_df.groupby('company_location')['salary_usd'].mean().sort_values(ascending=False)
    st.bar_chart(salary_by_country)

    st.subheader("📌 Correlation Heatmap (Numerical Variables)")
    numeric_data = filtered_df.select_dtypes(include=['int64', 'float64'])
    fig3, ax3 = plt.subplots()
    sns.heatmap(numeric_data.corr(), annot=True, cmap="coolwarm", ax=ax3)
    st.pyplot(fig3)

    st.subheader("📋 Filtered Data Preview")
    st.dataframe(filtered_df.head(50))

else:
    st.info("Please upload your dataset to start visualizing.")