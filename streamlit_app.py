import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Hope Foundation Dashboard", layout="wide")
st.title("🏥 Hope Foundation Dashboard")

# Use cleaned data
df = pd.read_excel("cleaning_data.xlsx")

# Sidebar navigation
page = st.sidebar.selectbox("Dashboard Pages",
                                [
                                    "Ready for Review",
                                    "Support by Demographics",
                                    "Annual Impact Summary"
                                ]
                            )


# PAGE NAME = Ready for Review
if page == "Ready for Review":
    st.title("Applications: Ready for Review")
    df['year'] = pd.to_datetime(df['grant_req_date']).dt.year

    summary = df.groupby('year').agg(
        total_granted=('amount', 'sum'),
        unique_patients=('patient_id', 'nunique')
    ).reset_index()

    fig = px.bar(summary, x='year', y='total_granted', title="Total Support by Year")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(summary)

# PAGE NAME = Support by Demographics
elif page == "Support by Demographics":
    st.title("Support Distribution by Demographics")
    group_field = st.selectbox("Group by demographic:", [
        "gender", "insurance_type", "assistance_type", "marital_status", "race"
    ])

    if group_field in df.columns:
        grouped = df.groupby(group_field)['amount'].sum().reset_index()
        fig = px.bar(grouped, x=group_field, y='amount', title=f"Support by {group_field.title()}")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("That column is not available.")

# PAGE NAME = Annual Impact Summary
elif page == "Annual Impact Summary":
    st.title("Annual Impact Summary")

    df['year'] = pd.to_datetime(df['grant_req_date']).dt.year

    summary = df.groupby('year').agg(
        total_granted=('amount', 'sum'),
        unique_patients=('patient_id', 'nunique')
    ).reset_index()

    fig = px.bar(summary, x='year', y='total_granted', title="Total Support by Year")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(summary)

st.subheader("Cleaned Data Preview")
st.dataframe(df.head())
