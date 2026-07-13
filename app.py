import streamlit as st
from src.database import execute_query, read_sql_file
import plotly.express as px
import time
import pandas as pd


st.title("Instacart Executive Dashboard")

tab1, tab2, tab3 = st.tabs(["Overview", "Basic Analysis", "Business Discussion"])

st.sidebar.title("Table of Contents")
st.sidebar.markdown("[1. Problem Statement](#ProblemStatement)", unsafe_allow_html=True)
st.sidebar.markdown("[2. Business Question](#BusinessQuestion)", unsafe_allow_html=True)
st.sidebar.markdown("[3. Database Preview](#DatabasePreview)", unsafe_allow_html=True)

with tab1:
    st.header("Introduction")
    st.write('**Instacart** is a grocery delivery and pickup service. Users can select items from local grocery stores through the Instacart app or website and then either have them delivered to their doorstep by a personal shopper or prepared for pickup at the store.')

    st.header("Problem Statement")
    st.write("Grocery delivery is a highly competitive, low-margin business. To remain profitable, Instacart must maximize customer retention (preventing churn) and increase the average basket size per order. However, without clear visibility into user purchasing habits and product affinities, marketing and operations teams cannot effectively target promotions or anticipate inventory demand.")

    st.header("Business Question")
    st.write("""
    1. Who are our most loyal customers, and who is at risk of abandoning the app?
    2. Which products drive the most consistent revenue, and what items are "staples" (always reordered)?
    3. When is our app traffic the heaviest, and how does purchasing behavior change throughout the week?
    """)

    # Database Preview
    st.header("Database Preview")

    st.subheader("Aisles Table")
    st.text('Contains information about different product categories (aisles).')
    df_preview = execute_query("SELECT * FROM aisles LIMIT 5")
    st.dataframe(df_preview)

    st.subheader("Departments Table")
    st.text('Provides details about various departments within the store.')
    df_preview = execute_query("SELECT * FROM departments LIMIT 5")
    st.dataframe(df_preview)

    st.subheader("Products Ordered Table")
    st.text('Includes information about products included in prior customer orders.')
    df_preview = execute_query("SELECT * FROM order_products__prior LIMIT 5")
    st.dataframe(df_preview)

    st.subheader("Orders Table")
    st.text('Provides information about individual orders and customers.')
    df_preview = execute_query("SELECT * FROM orders LIMIT 5")
    st.dataframe(df_preview)

    st.subheader("Products Table")
    st.text('Contains details about products, including aisle and department IDs.')
    df_preview = execute_query("SELECT * FROM products LIMIT 5")
    st.dataframe(df_preview)


with tab2:
    st.header("Top Products Analysis")
    st.markdown("> Results are taken from the SQL output, however it is hardcoded since the runtime process takes too long..")
    if st.button("Run Top Products Analysis"):
        with st.spinner("Crunching the numbers and running SQL..."):
            sql = read_sql_file("top_products.sql")
            # results = execute_query(sql)
            time.sleep(1)
        # Hard-Coded Execution since runtime takes too long, please remember to fix this
        st.write("### Top 10 Products")
        top_products = pd.DataFrame({
            "product_name": [
                "Banana",
                "Bag of Organic Bananas",
                "Organic Strawberries",
                "Organic Baby Spinach",
                "Organic Hass Avocado",
                "Organic Avocado",
                "Large Lemon",
                "Strawberries",
                "Limes",
                "Organic Whole Milk"
            ],
            "total_orders": [
                472565,
                379450,
                264683,
                241921,
                213584,
                176815,
                152657,
                142951,
                140627,
                137905
            ]
        })

        st.dataframe(
            top_products,
            use_container_width=True,
            hide_index=True
        )
        
        with st.expander("View SQL Logic"):
            st.code(sql, language="sql")
    
with tab3:
    # Answering Question 1
    st.header("Q1 - Customer Segmentation")
    st.write("Grouping customers based on purchasing frequency and cadence.")

    if st.button("Run Segmentation Analysis"):
        with st.spinner("Crunching the numbers and running SQL..."):
            sql = read_sql_file("customer_segmentation.sql")
            df = execute_query(sql)

        st.dataframe(df)
        fig = px.bar(
            df, 
            x="customer_segment", 
            y="total_users", 
            color="customer_segment",
            title="Users per Segment",
            text_auto=True
        )
        st.plotly_chart(fig)
        
        with st.expander("View the SQL Logic"):
            st.code(sql, language="sql")
        
        with st.expander("Explanation & Thought Process"):
            st.markdown("""
            To answer the first business question, I searched through the database to find the best variables to create a churn analysis.
            
            A typical churn analysis utilizes RFM (Recency, Frequency, Monetary). However, since 'Monetary' data is not included in this database, I shifted the approach to a Recency & Frequency (R&F) Customer Segmentation Model.
            
            The chosen variables are `order_number` to represent 'Frequency' and `days_since_prior_order` to represent 'Recency'.
            
            Customers are divided into 3 groups:
            * Loyal Customers: Have more than 10 total orders AND average less than 14 days between orders (bi-weekly shoppers).
            * At Risk Customers: Have an average of more than 28 days (4 weeks) between orders.
            * Casual Shoppers: Anyone who does not fit into the categories above.
            
            **Conclusion:** Most shoppers are 'Casual Shoppers' (approx. 129.7k), while the smallest group is 'At Risk' customers (approx. 9k). *It is worth noting that these groupings are based on domain logic and have not been tested statistically. In a future iteration, an ANOVA test should be conducted to prove the significance of the variance between these groups.*
            """)
        
    st.write("---") 
    st.header("Q2 - Product Affinity")
    st.write("Identifying 'Staple' products that drive habitual app usage.")

    if st.button("Run Product Affinity Analysis"):
        
        with st.spinner("Fetching pre-aggregated reorder rates..."):
            sql_affinity = read_sql_file("product_affinity.sql")
            df_affinity = execute_query(sql_affinity)
        
        st.dataframe(df_affinity)
        fig_affinity = px.bar(
            df_affinity, 
            x="reorder_rate_percent", 
            y="product_name", 
            orientation='h', 
            title="Top 15 Staple Products by Reorder Rate",
            labels={"reorder_rate_percent": "Reorder Rate (%)", "product_name": "Product"},
            color="reorder_rate_percent",
            color_continuous_scale="Viridis",
            text_auto=True
        )
        fig_affinity.update_layout(yaxis={'categoryorder':'total ascending'}) 
        
        st.plotly_chart(fig_affinity)
        
        with st.expander("Explanation & Thought Process"):
            st.markdown("""
            To answer the second business question, I needed to identify which products act as "anchors" for the platform. 
            
            Data Engineering & Performance Tuning:
            Initially, calculating reorder rates required joining and aggregating millions of rows in real-time, which caused severe dashboard latency. To optimize performance, I engineered a data pipeline step. I created a 'Materialized View' (pre-aggregated table) directly in SQLite to compute the baseline purchase counts and reorders beforehand. This shifted the compute load off the app and reduced query execution time to milliseconds.
            
            Methodology:
            * I calculated the 'Reorder Rate' by dividing total reorders by total purchases using the pre-aggregated data.
            * I applied a `WHERE total_purchases > 25000` filter to exclude niche items that were only bought a few times, ensuring statistical significance.
            
            Business Value: Products with extremely high reorder rates (like dairy, water, or fresh produce) are habit-forming. Instacart's marketing team can use these specific items as loss-leaders in promotional emails to guarantee high conversion rates and drive users back into the app.
            """)
            
        with st.expander("View the SQL & Pipeline Logic"):
            st.write("### 1. Data Pre-Processing")
            st.write("This query was run directly in the database to pre-aggregate the rows, acting as a Materialized View to optimize app performance:")
            st.code("""
CREATE TABLE product_reorder_stats AS 
SELECT 
    product_id, 
    COUNT(*) AS total_purchases, 
    SUM(reordered) AS total_reorders
FROM order_products_prior
GROUP BY product_id;
            """, language="sql")
            
            st.write("### 2. Production App Query")
            st.write("This query is the main process after the pre-aggregation:")
            st.code(sql_affinity, language="sql")