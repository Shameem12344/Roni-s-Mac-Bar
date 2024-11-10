import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Set page config to wide mode
st.set_page_config(layout="wide")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('nona_data - nona_data.csv')

data = load_data()

# Process Data
data['Sent Date'] = pd.to_datetime(data['Sent Date'])

# UI Setup with smaller header to save space
st.markdown("<h2 style='text-align: center;'>Roni's Mac Bar - Business Insights Dashboard</h2>", unsafe_allow_html=True)

# Create filters in a horizontal line
col1, col2, col3, col4 = st.columns(4)
with col1:
    start_date = st.date_input("Start Date", data['Sent Date'].min().date())
with col2:    
    end_date = st.date_input("End Date", data['Sent Date'].max().date())
with col3:
    menu_items = st.multiselect("Menu Items", options=data['Parent Menu Selection'].unique(), 
                               default=data['Parent Menu Selection'].unique())
with col4:
    view_mode = st.selectbox("View Mode", ["Main Metrics", "Additional Insights"])

# Filter Data
filtered_data = data[
    (data['Sent Date'] >= pd.to_datetime(start_date)) &
    (data['Sent Date'] <= pd.to_datetime(end_date)) &
    (data['Parent Menu Selection'].isin(menu_items))
]

# Quick metrics row
metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)
with metric_col1:
    total_orders = filtered_data['Order ID'].nunique()
    st.metric("Total Orders", f"{total_orders:,}")
with metric_col2:
    avg_orders_per_day = total_orders / len(filtered_data['Sent Date'].dt.date.unique())
    st.metric("Avg Orders/Day", f"{avg_orders_per_day:.1f}")
with metric_col3:
    hourly_orders = filtered_data['Sent Date'].dt.hour.value_counts().sort_index()
    peak_hour = hourly_orders.idxmax()
    st.metric("Peak Hour", f"{peak_hour:02d}:00")
with metric_col4:
    day_of_week = filtered_data['Sent Date'].dt.day_name().value_counts()
    busiest_day = day_of_week.idxmax()
    st.metric("Busiest Day", busiest_day)
with metric_col5:
    avg_items_per_order = filtered_data.groupby('Order ID').size().mean()
    st.metric("Avg Items/Order", f"{avg_items_per_order:.1f}")

if view_mode == "Main Metrics":
    # Create layout with two rows and two columns
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)

    # Graph 1: Total Sales Over Time (Daily trend)
    with row1_col1:
        daily_orders = filtered_data.set_index('Sent Date')['Order ID'].resample('D').count()
        fig_daily_sales = px.line(
            daily_orders,
            title="Total Sales Over Time",
            height=400  # Increased height
        )
        fig_daily_sales.update_layout(
            xaxis_title="Sent Date",
            yaxis_title="Order ID",
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=40, r=20, t=40, b=40)
        )
        st.plotly_chart(fig_daily_sales, use_container_width=True)

    # Graph 2: Average Time of Day for Business
    with row1_col2:
        fig_hourly = px.line(
            hourly_orders,
            title="Average Time of Day for Business",
            height=400
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
            height=400,
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
        correct_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_of_week = day_of_week.reindex(correct_order)
        fig_dow = px.bar(
            day_of_week,
            title="Orders by Day of Week",
            height=400,
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

else:  # Additional Insights
    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)
    
    # Graph 1: Seasonal Patterns (Monthly Trend)
    with row1_col1:
        monthly_orders = filtered_data.set_index('Sent Date')['Order ID'].resample('M').count()
        fig_seasonal = px.line(
            monthly_orders,
            title="Seasonal Order Patterns",
            height=400
        )
        fig_seasonal.update_layout(
            xaxis_title="Month",
            yaxis_title="Order Count",
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_seasonal, use_container_width=True)

    # Graph 2: Rush Hour Analysis
    with row1_col2:
        filtered_data['is_rush_hour'] = filtered_data['Sent Date'].dt.hour.isin([11, 12, 13, 17, 18, 19])
        rush_hour_stats = filtered_data.groupby('is_rush_hour')['Order ID'].count()
        fig_rush = px.pie(
            values=rush_hour_stats.values,
            names=['Non-Rush Hour', 'Rush Hour'],
            title="Rush Hour vs Non-Rush Hour Orders",
            height=400
        )
        fig_rush.update_layout(template="plotly_dark")
        st.plotly_chart(fig_rush, use_container_width=True)

    # Graph 3: Popular Modifier Combinations
    with row2_col1:
        if 'Modifier' in filtered_data.columns:
            modifier_combos = filtered_data['Modifier'].value_counts().head(10)
            fig_mods = px.bar(
                modifier_combos,
                title="Top Modifier Combinations",
                height=400,
                color=modifier_combos.values,
                color_continuous_scale='Viridis'
            )
            fig_mods.update_layout(
                xaxis_title="Modifier Combination",
                yaxis_title="Count",
                template="plotly_dark",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig_mods, use_container_width=True)

    # Graph 4: Weekday vs Weekend Analysis
    with row2_col2:
        filtered_data['is_weekend'] = filtered_data['Sent Date'].dt.day_name().isin(['Saturday', 'Sunday'])
        weekend_analysis = filtered_data.groupby(['is_weekend', filtered_data['Sent Date'].dt.hour])['Order ID'].count().unstack()
        weekend_analysis.index = ['Weekday', 'Weekend']
        fig_weekend = px.line(
            weekend_analysis.T,
            title="Weekday vs Weekend Hourly Patterns",
            height=400
        )
        fig_weekend.update_layout(
            xaxis_title="Hour of Day",
            yaxis_title="Average Orders",
            template="plotly_dark",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_weekend, use_container_width=True)

# Add a section for detailed statistics
with st.expander("Detailed Statistics"):
    stat_col1, stat_col2 = st.columns(2)
    
    with stat_col1:
        st.write("### Order Timing Statistics")
        st.write(f"Busiest Hour: {peak_hour}:00")
        st.write(f"Average Daily Orders: {avg_orders_per_day:.1f}")
        st.write(f"Busiest Day: {busiest_day}")
        
    with stat_col2:
        st.write("### Menu Statistics")
        st.write(f"Most Popular Item: {filtered_data['Parent Menu Selection'].mode()[0]}")
        st.write(f"Average Items per Order: {avg_items_per_order:.1f}")
        if 'Modifier' in filtered_data.columns:
            st.write(f"Most Common Modifier: {filtered_data['Modifier'].mode()[0]}")
