import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title("Advanced ESG Scoring App")

@st.cache
def load_data():
    data = pd.DataFrame({
        'Company': ['Company A', 'Company B', 'Company C'],
        'Environmental': [75, 65, 80],
        'Social': [70, 60, 85],
        'Governance': [80, 70, 90],
        'Date': pd.date_range(start='2021-01-01', periods=3, freq='Y')
    })
    return data

esg_data = load_data()

st.sidebar.header("Select Options")

companies = esg_data['Company'].unique()
selected_company = st.sidebar.selectbox('Select a Company', companies)

if st.sidebar.checkbox("Show Raw Data"):
    st.subheader("Raw ESG Data")
    st.write(esg_data)

st.header(f"ESG Scores for {selected_company}")

company_data = esg_data[esg_data['Company'] == selected_company]
st.subheader("Score Breakdown")
st.write(company_data[['Environmental', 'Social', 'Governance']])

company_data['Total ESG Score'] = company_data[['Environmental', 'Social', 'Governance']].mean(axis=1)
st.subheader("Total ESG Score")
st.write(company_data['Total ESG Score'].iloc[0])

categories = ['Environmental', 'Social', 'Governance']
fig = px.line_polar(company_data.melt(id_vars=['Company'], value_vars=categories),
                    r='value', theta='variable', line_close=True)
fig.update_traces(fill='toself')
st.plotly_chart(fig)

st.header("Compare Companies")
selected_companies = st.multiselect('Select Companies to Compare', companies, default=companies[0:2])

comparison_data = esg_data[esg_data['Company'].isin(selected_companies)]

st.subheader("ESG Component Comparison")
fig2 = px.bar(comparison_data.melt(id_vars=['Company'], value_vars=categories),
              x='variable', y='value', color='Company', barmode='group')
st.plotly_chart(fig2)
