Create a Python Streamlit dashboard for a business analytics project called "Urban Vogue".
The application must meet three main requirements:
1. Monitor sales by collection/category.
2. Evaluate marketing effectiveness.
3. Uncover customer loyalty trends.

Dataset structure:
Columns: ['Date', 'Time of Day', 'Channel', 'Category', 'Service', 'Ad Spend', 'Conversions', 'Revenue', 'Cost', 'Profit', 'Customer Type']

Requirements:
1. Sidebar Filters: Date range picker, Channel multiselect, Category multiselect, Customer Type multiselect.
2. High-level KPIs: Total Revenue, Total Profit, Total Ad Spend, ROAS (Revenue / Ad Spend), Total Conversions, CPA (Ad Spend / Conversions).
3. Tab 1 - Sales & Collections:
   - Bar chart: Revenue & Profit by Category & Service.
   - Line chart: Daily / Monthly Revenue trends.
   - Pie chart / Donut chart: Revenue distribution by Time of Day.
4. Tab 2 - Marketing Effectiveness:
   - Bar chart comparing Ad Spend vs Revenue by Channel.
   - ROAS and Conversion Rate per Channel.
   - Scatter plot or bubble chart comparing Ad Spend vs Conversions.
5. Tab 3 - Customer Loyalty Trends:
   - Donut chart: New vs Returning Customers breakdown.
   - Metric comparison (Average Revenue & Profit per Customer Type).
   - Channel breakdown by Customer Type.
6. Design: Clean UI using Plotly express/graph_objects and Streamlit columns, styled with custom CSS. Include support for uploading an Excel/CSV file or reading from a default Data.xlsx file.
