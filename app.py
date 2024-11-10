import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('nona_data - nona_data.csv')

data = load_data()

# Process Data
data['Sent Date'] = pd.to_datetime(data['Sent Date'])

# UI Setup with smaller header to save space
st.markdown("<h2 style='text-align: center;'>Roni's Mac Bar - Business Insights Dashboard</h2>", unsafe_allow_html=True)

# Create two columns for filters
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", data['Sent Date'].min().date())
end_date = data['Sent Date'].max().date()
with col2:
    menu_items = st.multiselect("Menu Items", options=data['Parent Menu Selection'].unique(), 
                               default=data['Parent Menu Selection'].unique())

# Filter Data
filtered_data = data[
    (data['Sent Date'] >= pd.to_datetime(start_date)) &
    (data['Sent Date'] <= pd.to_datetime(end_date)) &
    (data['Parent Menu Selection'].isin(menu_items))
]

# Create layout with two rows and two columns
row1_col1, row1_col2 = st.columns(2)
row2_col1, row2_col2 = st.columns(2)

# Graph 1: Total Sales Over Time (Daily trend)
with row1_col1:
    daily_orders = filtered_data.set_index('Sent Date')['Order ID'].resample('D').count()
    fig_daily_sales = px.line(
        daily_orders,
        title="Total Sales Over Time",
        height=300  # Reduce height to fit in quad layout
    )
    fig_daily_sales.update_layout(
        xaxis_title="Sent Date",
        yaxis_title="Order ID",
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=20, t=40, b=40)  # Adjust margins
    )
    st.plotly_chart(fig_daily_sales, use_container_width=True)

# Graph 2: Average Time of Day for Business
with row1_col2:
    hourly_orders = filtered_data['Sent Date'].dt.hour.value_counts().sort_index()
    fig_hourly = px.line(
        hourly_orders,
        title="Average Time of Day for Business",
        height=300
    )
    fig_hourly.update_layout(
        xaxis_title="Hour",
        yaxis_title="Order Count",
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(tickmode='linear', tick0=0, dtick=1),
        margin=dict(l=40, r=20, t=40, b=40)
    )
    st.plotly_chart(fig_hourly, use_container_width=True)

# Graph 3: Menu Item Popularity
with row2_col1:
    item_popularity = filtered_data['Parent Menu Selection'].value_counts().head(10)
    fig_items = px.bar(
        item_popularity,
        title="Top Menu Items",
        height=300,
        color=item_popularity.values,
        color_continuous_scale='Viridis'
    )
    fig_items.update_layout(
        xaxis_title="Menu Item",
        yaxis_title="Order Count",
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=20, t=40, b=100),
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig_items, use_container_width=True)

# Graph 4: Day of Week Analysis
with row2_col2:
    day_of_week = filtered_data['Sent Date'].dt.day_name().value_counts()
    # Reorder days correctly
    correct_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_of_week = day_of_week.reindex(correct_order)
    
    fig_dow = px.bar(
        day_of_week,
        title="Orders by Day of Week",
        height=300,
        color=day_of_week.values,
        color_continuous_scale='Viridis'
    )
    fig_dow.update_layout(
        xaxis_title="Day of Week",
        yaxis_title="Order Count",
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=20, t=40, b=40)
    )
    st.plotly_chart(fig_dow, use_container_width=True)

# Add key metrics at the top in a row
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    total_orders = filtered_data['Order ID'].nunique()
    st.metric("Total Orders", f"{total_orders:,}")

with metric_col2:
    avg_orders_per_day = total_orders / len(filtered_data['Sent Date'].dt.date.unique())
    st.metric("Avg Orders/Day", f"{avg_orders_per_day:.1f}")

with metric_col3:
    peak_hour = hourly_orders.idxmax()
    st.metric("Peak Hour", f"{peak_hour:02d}:00")

with metric_col4:
    busiest_day = day_of_week.idxmax()
    st.metric("Busiest Day", busiest_day)

# Optional: Add additional insights
if st.checkbox("Show Additional Insights"):
    st.write("---")
    col1, col2 = st.columns(2)
    
    with col1:
        # Average orders by weekday vs weekend
        filtered_data['is_weekend'] = filtered_data['Sent Date'].dt.day_name().isin(['Saturday', 'Sunday'])
        weekend_avg = filtered_data[filtered_data['is_weekend']]['Order ID'].nunique() / \
                     filtered_data[filtered_data['is_weekend']]['Sent Date'].dt.date.nunique()
        weekday_avg = filtered_data[~filtered_data['is_weekend']]['Order ID'].nunique() / \
                     filtered_data[~filtered_data['is_weekend']]['Sent Date'].dt.date.nunique()
        
        st.write("Average Orders:")
        st.write(f"Weekdays: {weekday_avg:.1f}")
        st.write(f"Weekends: {weekend_avg:.1f}")
    
    with col2:
        # Most popular modifier combinations
        if 'Modifier' in filtered_data.columns:
            modifier_combos = filtered_data['Modifier'].value_counts().head(5)
            st.write("Top Modifier Combinations:")
            st.write(modifier_combos)
