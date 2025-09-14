import pandas as pd
import streamlit as st
import plotly.express as px


@st.cache_data
def load_data():
    fb = pd.read_csv("data/facebook.csv")
    google = pd.read_csv("data/Google.csv")
    tiktok = pd.read_csv("data/TikTok.csv")
    business = pd.read_csv("data/Business.csv")

    fb["channel"] = "Facebook"
    google["channel"] = "Google"
    tiktok["channel"] = "TikTok"

    ads = pd.concat([fb, google, tiktok], ignore_index=True)

    ads.columns = ads.columns.str.strip().str.lower().str.replace(" ", "_")
    business.columns = business.columns.str.strip().str.lower().str.replace(" ", "_")

    ads["date"] = pd.to_datetime(ads["date"])
    business["date"] = pd.to_datetime(business["date"])

    return ads, business

ads, business = load_data()


ads["ctr"] = ads["clicks"] / ads["impression"].replace(0, pd.NA)
ads["cpc"] = ads["spend"] / ads["clicks"].replace(0, pd.NA)
ads["roas"] = ads["attributed_revenue"] / ads["spend"].replace(0, pd.NA)

business["cac"] = business["total_revenue"] / business["new_customers"].replace(0, pd.NA)


st.set_page_config(page_title="Marketing Intelligence Dashboard", layout="wide")
st.title("📊 Marketing Intelligence Dashboard")

st.sidebar.header("Filters")
channels = ["All"] + list(ads["channel"].unique())
selected_channel = st.sidebar.selectbox("Select Channel", channels)

if selected_channel != "All":
    ads_filtered = ads[ads["channel"] == selected_channel]
else:
    ads_filtered = ads


st.subheader("Key Metrics")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Spend", f"${ads_filtered['spend'].sum():,.0f}")
col2.metric("Total Attributed Revenue", f"${ads_filtered['attributed_revenue'].sum():,.0f}")
col3.metric("Avg ROAS", f"{ads_filtered['roas'].mean():.2f}x")
col4.metric("Avg CPC", f"${ads_filtered['cpc'].mean():.2f}")


fig1 = px.line(ads_filtered, x="date", y="spend", color="channel",
               title="Daily Ad Spend")
st.plotly_chart(fig1, use_container_width=True)


fig2 = px.line(business, x="date", y="total_revenue",
               title="Business Revenue Over Time")
st.plotly_chart(fig2, use_container_width=True)


fig3 = px.bar(ads, x="channel", y="ctr", title="CTR by Channel", barmode="group")
st.plotly_chart(fig3, use_container_width=True)


fig4 = px.line(business, x="date", y="cac", title="Customer Acquisition Cost (CAC)")
st.plotly_chart(fig4, use_container_width=True)


with st.expander("📂 Show Raw Data"):
    st.write("### Ads Data", ads_filtered.head(10))
    st.write("### Business Data", business.head(10))
