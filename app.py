import streamlit as st
from src.database import execute_query, read_sql_file
import plotly.express as px
import time
import pandas as pd


st.title("Instacart Executive Dashboard")

tab1, tab2, tab3 = st.tabs(["Overview", "Basic Analysis", "Business Discussion"])


with tab1:
    
    st.header("Introduction")
    st.image("Figures/instacart.png")
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
    with st.expander("⚠️ Warning"):
        st.warning("We will only be using the **order_products__prior** table as our **Orders** table. The **order_products__train** table is not used in this analysis as it is meant for training machine learning models and does not contain any additional information that is relevant to our analysis.")

    st.subheader("Products Table")
    st.text('Contains details about products, including aisle and department IDs.')
    df_preview = execute_query("SELECT * FROM products LIMIT 5")
    st.dataframe(df_preview)


with tab2:
    st.warning("The results were obtained from the SQL output but hardcoded due to the long runtime of the query.")
    st.subheader("1. What are the top 10 products that are most commonly added to the cart first?")
    top_products_sql = read_sql_file("top_products.sql")
    # if st.button("Run Top Products Analysis"):
    #     with st.spinner("Crunching the numbers and running SQL..."):
    #         # results = execute_query(sql)
    #         time.sleep(1)
        # Hard-Coded Execution since runtime takes too long, please remember to fix this

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
        st.code(top_products_sql, language="sql")

    st.subheader("2. What are the top 10 product pairs that are most frequently purchased together?")
    sql_pairs = read_sql_file("product_pairs.sql")
    # if st.button("Run Product Pair Analysis"):
    #     with st.spinner("Crunching the numbers and running SQL..."):
    #         # results = execute_query(sql_pairs)
    #         time.sleep(1)
    #     # Hard-Coded Execution since runtime takes too long, please remember to fix this
    top_product_pairs = pd.DataFrame({
        "product_1": [
                "Bag of Organic Bananas",
                "Bag of Organic Bananas",
                "Organic Strawberries",
                "Banana",
                "Organic Baby Spinach",
                "Bag of Organic Bananas",
                "Strawberries",
                "Banana",
                "Organic Strawberries",
                "Bag of Organic Bananas",
        ],
        "product_2": [
            "Organic Hass Avocado",
            "Organic Strawberries",
            "Banana",
            "Organic Avocado",
            "Banana",
            "Organic Baby Spinach",
            "Banana",
            "Large Lemon",
            "Organic Hass Avocado",
            "Organic Raspberries"
        ],
        "times_bought_together": [
            62341,
            61628,
            56156,
            53395,
            51395,
            50372,
            41232,
            40880,
            40794,
            40503
        ]
    })

    st.dataframe(
        top_product_pairs,
        use_container_width=True,
        hide_index=True
    )
    
    with st.expander("View SQL Logic"):
        st.code(sql_pairs, language="sql")
    
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

    # Answering Question 2
    st.write("---") 
    st.header("Q2 - Product Affinity")
    st.write("Identifying 'Staple' products that drive habitual app usage.")

    if st.button("Run Product Affinity Analysis"):
        
        with st.spinner("This may take some time..."):
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
        
        with st.expander("View the SQL Logic"):
            st.write("Production App Query")
            st.code(sql_affinity, language="sql")

        with st.expander("Explanation & Thought Process"):
            st.markdown("""
            To answer the second business question, I needed to identify which products act as "anchors" for the platform. 
            
            Methodology:
            * I calculated the 'Reorder Rate' by dividing total reorders by total purchases using the pre-aggregated data.
            * I applied a `WHERE total_purchases > 25000` filter to exclude niche items that were only bought a few times, ensuring statistical significance.
            
            Business Value: Products with extremely high reorder rates (like dairy, water, or fresh produce) are habit-forming. Instacart's marketing team can use these specific items as loss-leaders in promotional emails to guarantee high conversion rates and drive users back into the app.
            """)

    st.write("---") 
    st.header("Q3 - Operational Demand Forecasting")
    st.write("Mapping peak shopping hours to optimize delivery logistics and platform stability.")

    if st.button("Run Demand Analysis"):
        
        with st.spinner("Calculating hourly order volume..."):
            start_time = time.perf_counter()
            
            sql_demand = read_sql_file("hourly_demand.sql")
            df_demand = execute_query(sql_demand)
            
            end_time = time.perf_counter()
        
        fig_demand = px.line(
            df_demand, 
            x="order_hour_of_day", 
            y="total_orders", 
            title="Instacart Order Volume by Hour of Day",
            labels={"order_hour_of_day": "Hour of Day (0-23)", "total_orders": "Total Orders"},
            markers=True
        )
        
        fig_demand.update_layout(xaxis=dict(tickmode='linear', tick0=0, dtick=1))
        
        st.plotly_chart(fig_demand)

        st.write("---")
        st.subheader("Weekly Demand Trend")
        
        with st.spinner("Calculating daily order volume..."):
            sql_daily = read_sql_file("daily_demand.sql")
            df_daily = execute_query(sql_daily)
            
        fig_daily = px.bar(
            df_daily, 
            x="order_dow", 
            y="total_orders", 
            title="Instacart Order Volume by Day of Week",
            labels={"order_dow": "Day of Week (0-6)", "total_orders": "Total Orders"},
            color="total_orders",
            color_continuous_scale="Blues"
        )
        
        fig_daily.update_layout(xaxis=dict(tickmode='linear', tick0=0, dtick=1))
        
        st.plotly_chart(fig_daily)

        with st.expander("Explanation"):
            st.markdown(
                """
                    **Intraday Demand Curve (Hourly Trend)**
                    * Off-Peak Window (12 AM - 6 AM): Volume drops to its daily floor (~5k - 30k orders/hr), opening the optimal operational window for dark-store restocking, inventory audits, and batch maintenance.
                    * Morning Surge (7 AM - 9 AM): Demand ramps up sharply from 30k to over 250k orders/hr as same-day fulfillment requests surge.
                    * Peak Demand Plateau (10 AM - 4 PM): Volume sustains its maximum plateau between ~272k and ~288k orders/hr. Shopper allocations and driver dispatch must be capped at maximum density during this 6-hour core window to protect delivery SLAs.
                    * Evening Taper (5 PM - 11 PM): Activity steadily winds down from ~228k to 40k as daily fulfillment closes out.

                    **Day-of-Week Load Distribution (Weekly Trend)**
                    * Weekend Peak (Days 0 & 1): Days 0 and 1 (typically Sunday and Monday in the Instacart schema) drive the highest weekly volume, hitting ~600k and ~580k orders respectively.
                    * Mid-Week Baseline (Days 2 - 6): Demand stabilizes at a consistent baseline of 420k - 460k orders/day.
                    * Actionable Takeaway: Fulfillment centers and partner retail locations require 30-35% higher shopper capacity on Days 0 and 1 compared to mid-week baseline days to prevent order backlogs.

                """
            )


