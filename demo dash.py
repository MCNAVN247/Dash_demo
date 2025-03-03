import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# Khởi tạo ứng dụng Dash
app = Dash(__name__)

# Tạo dữ liệu giả lập
np.random.seed(42)
months = pd.date_range(start="2024-01-01", periods=12, freq="M")
products = ['A', 'B', 'C', 'D']
df = pd.DataFrame({
    "Month": np.tile(months, len(products)),
    "Product": np.repeat(products, len(months)),
    "Revenue": np.random.randint(100, 300, len(months) * len(products)) * 10,
    "Expenses": np.random.randint(50, 200, len(months) * len(products)) * 10
})
df["Profit"] = df["Revenue"] - df["Expenses"]
df["Profit Margin"] = (df["Profit"] / df["Revenue"]) * 100

# Layout giao diện
app.layout = html.Div([
    html.H1("📊 Financial Dashboard: KPI & Nhóm Sản Phẩm", style={"text-align": "center"}),

    html.Div([
        html.Label("📅 Chọn khoảng thời gian:"),
        dcc.RangeSlider(
            id="time-slider",
            min=0, max=len(months) - 1,
            value=[0, len(months) - 1],
            marks={i: str(months[i].strftime("%b")) for i in range(len(months))},
            step=1
        ),
    ]),

    html.Div([
        html.Label("🛍 Chọn sản phẩm:"),
        dcc.Dropdown(
            id="product-dropdown",
            options=[{"label": p, "value": p} for p in products],
            value=products,
            multi=True
        )
    ]),

    html.Div([
        html.Div(id="kpi-container", style={"display": "flex", "justify-content": "space-around"})
    ]),

    dcc.Graph(id="revenue-expenses-chart"),
    dcc.Graph(id="profit-margin-chart"),
    dcc.Graph(id="product-comparison-chart"),
])

# Callback cập nhật KPI
@app.callback(
    Output("kpi-container", "children"),
    [Input("time-slider", "value"), Input("product-dropdown", "value")]
)
def update_kpis(selected_time, selected_products):
    df_filtered = df[(df["Month"] >= months[selected_time[0]]) & (df["Month"] <= months[selected_time[1]]) & (df["Product"].isin(selected_products))]
    total_revenue = df_filtered["Revenue"].sum()
    total_expenses = df_filtered["Expenses"].sum()
    total_profit = df_filtered["Profit"].sum()
    profit_margin = round((total_profit / total_revenue) * 100, 2) if total_revenue else 0
    return [
        html.H3(f"💰 Tổng Doanh Thu: {total_revenue:,} VND"),
        html.H3(f"📉 Tổng Chi Phí: {total_expenses:,} VND"),
        html.H3(f"📈 Lợi Nhuận: {total_profit:,} VND"),
        html.H3(f"📊 Tỷ suất lợi nhuận: {profit_margin}%")
    ]

# Callback cập nhật biểu đồ doanh thu - chi phí
@app.callback(
    Output("revenue-expenses-chart", "figure"),
    [Input("time-slider", "value"), Input("product-dropdown", "value")]
)
def update_revenue_expenses(selected_time, selected_products):
    df_filtered = df[(df["Month"] >= months[selected_time[0]]) & (df["Month"] <= months[selected_time[1]]) & (df["Product"].isin(selected_products))]
    fig = px.line(df_filtered, x="Month", y=["Revenue", "Expenses"], color_discrete_map={"Revenue": "green", "Expenses": "red"}, title="📊 Doanh Thu & Chi Phí")
    return fig

# Callback cập nhật biểu đồ tỷ suất lợi nhuận
@app.callback(
    Output("profit-margin-chart", "figure"),
    [Input("time-slider", "value"), Input("product-dropdown", "value")]
)
def update_profit_margin(selected_time, selected_products):
    df_filtered = df[(df["Month"] >= months[selected_time[0]]) & (df["Month"] <= months[selected_time[1]]) & (df["Product"].isin(selected_products))]
    fig = px.bar(df_filtered, x="Month", y="Profit Margin", color="Product", title="📊 Tỷ Suất Lợi Nhuận (%)")
    return fig

# Callback cập nhật biểu đồ so sánh nhóm sản phẩm
@app.callback(
    Output("product-comparison-chart", "figure"),
    [Input("time-slider", "value"), Input("product-dropdown", "value")]
)
def update_product_comparison(selected_time, selected_products):
    df_filtered = df[(df["Month"] >= months[selected_time[0]]) & (df["Month"] <= months[selected_time[1]]) & (df["Product"].isin(selected_products))]
    fig = px.bar(df_filtered, x="Product", y="Revenue", color="Product", title="📊 So sánh Doanh Thu theo Nhóm Sản Phẩm")
    return fig

# Chạy server
if __name__ == "__main__":
    app.run_server(debug=True)
