import streamlit as st
import pandas as pd
import plotly.express as px

# Load data (replace 'path_to_your_combined_data.csv' with actual file path in your GitHub repo)
@st.cache_data
def load_data():
    return pd.read_csv('nona_data - nona_data.csv')

data = load_data()

# Process Data
data['Sent Date'] = pd.to_datetime(data['Sent Date'])

# UI Setup
st.title("Roni's Mac Bar - Business Insights Dashboard")
st.markdown("Analyze customer preferences, order trends, and more for Roni's Mac Bar.")

# Date Selection
start_date = st.date_input("Start Date", data['Sent Date'].min().date())
end_date = st.date_input("End Date", data['Sent Date'].max().date())

# Menu Item Filter
menu_items = st.multiselect("Menu Items", options=data['Parent Menu Selection'].unique(), default=data['Parent Menu Selection'].unique())

# Filter Data
filtered_data = data[
    (data['Sent Date'] >= pd.to_datetime(start_date)) &
    (data['Sent Date'] <= pd.to_datetime(end_date)) &
    (data['Parent Menu Selection'].isin(menu_items))
]

# Display Insights
st.write(f"Total Orders: {filtered_data['Order ID'].nunique()}")
popular_item = filtered_data['Parent Menu Selection'].mode()[0] if not filtered_data.empty else "N/A"
st.write(f"Most Popular Item: {popular_item}")

# Monthly Orders Trend
if not filtered_data.empty:
    monthly_orders = filtered_data.set_index('Sent Date').resample('M')['Order ID'].nunique()
    fig_monthly_orders = px.line(monthly_orders, y='Order ID', title="Monthly Order Trend")
    st.plotly_chart(fig_monthly_orders)

    # Top Modifiers
modifier_counts = filtered_data['Modifier'].str.split(', ').explode().value_counts().head(10)
fig_modifiers = px.bar(
    modifier_counts, 
    x=modifier_counts.index, 
    y=modifier_counts.values, 
    title="Top 10 Modifiers",
    labels={'y': 'Frequency', 'x': 'Modifiers'}  # Use 'y' instead of 'value'
)

# You can also set it using figure update layout
fig_modifiers.update_layout(
    yaxis_title="Frequency"
)

st.plotly_chart(fig_modifiers)

# Total Sales Over Time (daily trend)
daily_orders = filtered_data.set_index('Sent Date')['Order ID'].resample('D').count()
fig_daily_sales = px.line(
    daily_orders,
    title="Total Sales Over Time",
    labels={'value': 'Order ID', 'Sent Date': 'Sent Date'}
)

fig_daily_sales.update_layout(
    xaxis_title="Sent Date",
    yaxis_title="Order ID",
    template="plotly_dark",  # This gives the dark theme
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    paper_bgcolor='rgba(0,0,0,0)'  # Transparent paper
)

st.plotly_chart(fig_daily_sales)

# Average Time of Day for Business
# Extract hour from datetime and count orders by hour
hourly_orders = filtered_data['Sent Date'].dt.hour.value_counts().sort_index()
fig_hourly = px.line(
    hourly_orders,
    title="Average Time of Day for Business",
    labels={'index': 'Hour', 'value': 'Order Count'}
)

fig_hourly.update_layout(
    xaxis_title="Hour",
    yaxis_title="Order Count",
    template="plotly_dark",  # This gives the dark theme
    plot_bgcolor='rgba(0,0,0,0)',  # Transparent background
    paper_bgcolor='rgba(0,0,0,0)',  # Transparent paper
    xaxis=dict(tickmode='linear', tick0=0, dtick=1)  # Show all hours on x-axis
)

st.plotly_chart(fig_hourly)

