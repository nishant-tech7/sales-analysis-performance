import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Retail Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

DATA_PATH = r"D:\sales-analysis-performance\data\cleaned\cleaned_retail_sales.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["OrderDate"] = pd.to_datetime(df["OrderDate"])
    return df


df = load_data()

# ---------- Sidebar filters ----------
st.sidebar.title("🔎 Dashboard Filters")

date_range = st.sidebar.date_input(
    "Order date",
    value=(df["OrderDate"].min().date(), df["OrderDate"].max().date()),
    min_value=df["OrderDate"].min().date(),
    max_value=df["OrderDate"].max().date()
)

regions = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

categories = st.sidebar.multiselect(
    "Category",
    sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

segments = st.sidebar.multiselect(
    "Customer segment",
    sorted(df["Segment"].unique()),
    default=sorted(df["Segment"].unique())
)

filtered_df = df[
    (df["OrderDate"].dt.date >= date_range[0])
    & (df["OrderDate"].dt.date <= date_range[1])
    & (df["Region"].isin(regions))
    & (df["Category"].isin(categories))
    & (df["Segment"].isin(segments))
]

# ---------- Title ----------
st.title("📊 Retail Sales Performance Dashboard")
st.caption("Sales, profitability, products, regions, and customer-segment performance")

# ---------- KPI cards ----------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["OrderID"].nunique()
total_quantity = filtered_df["Quantity"].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales else 0

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

kpi1.metric("Total Sales", f"${total_sales:,.0f}")
kpi2.metric("Total Profit", f"${total_profit:,.0f}")
kpi3.metric("Profit Margin", f"{profit_margin:.1f}%")
kpi4.metric("Orders", f"{total_orders:,}")
kpi5.metric("Units Sold", f"{total_quantity:,}")

st.divider()

# ---------- Charts ----------
left, right = st.columns(2)

monthly_sales = (
    filtered_df
    .set_index("OrderDate")
    .resample("MS")
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    .reset_index()
)

fig_trend = px.line(
    monthly_sales,
    x="OrderDate",
    y=["Sales", "Profit"],
    markers=True,
    title="Monthly Sales and Profit Trend",
    labels={"value": "Amount ($)", "variable": "Metric", "OrderDate": "Month"}
)
left.plotly_chart(fig_trend, use_container_width=True)

category_sales = (
    filtered_df.groupby("Category", as_index=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    .sort_values("Sales", ascending=False)
)

fig_category = px.bar(
    category_sales,
    x="Category",
    y=["Sales", "Profit"],
    barmode="group",
    title="Sales and Profit by Category",
    labels={"value": "Amount ($)", "variable": "Metric"}
)
right.plotly_chart(fig_category, use_container_width=True)

left, right = st.columns(2)

region_sales = (
    filtered_df.groupby("Region", as_index=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    .sort_values("Sales", ascending=False)
)

fig_region = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    color="Profit",
    title="Sales by Region",
    color_continuous_scale="Blues"
)
left.plotly_chart(fig_region, use_container_width=True)

top_products = (
    filtered_df.groupby("Product", as_index=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    .sort_values("Sales", ascending=False)
    .head(10)
)

fig_products = px.bar(
    top_products,
    x="Sales",
    y="Product",
    orientation="h",
    color="Profit",
    title="Top 10 Products by Sales",
    color_continuous_scale="Greens"
)
fig_products.update_layout(yaxis={"categoryorder": "total ascending"})
right.plotly_chart(fig_products, use_container_width=True)

# ---------- Detailed data ----------
st.subheader("Filtered Order Details")

st.dataframe(
    filtered_df.sort_values("OrderDate", ascending=False),
    use_container_width=True,
    hide_index=True
)

st.download_button(
    "⬇️ Download Filtered Data",
    data=filtered_df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_retail_sales.csv",
    mime="text/csv"
)