import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import datetime as dt
from datetime import datetime

# Initialize the Dash app
app = dash.Dash(__name__)

# Custom CSS styling
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

            body {
                font-family: 'Inter', sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }

            .dashboard-container {
                background: rgba(255, 255, 255, 0.95);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15);
                margin: 20px;
                padding: 30px;
                max-width: 1400px;
                margin-left: auto;
                margin-right: auto;
            }

            .header-section {
                text-align: center;
                margin-bottom: 40px;
                padding: 30px 20px;
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                border-radius: 15px;
                color: white;
                box-shadow: 0 10px 30px rgba(79, 172, 254, 0.3);
            }

            .header-section h1 {
                font-size: 3rem;
                font-weight: 700;
                margin: 0;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
            }

            .header-section h3 {
                font-size: 1.3rem;
                font-weight: 400;
                margin: 15px 0 0 0;
                opacity: 0.9;
            }

            .metrics-container {
                display: flex;
                gap: 20px;
                margin-bottom: 40px;
                justify-content: space-between;
                flex-wrap: wrap;
            }

            .metric-card {
                flex: 1;
                min-width: 250px;
                background: white;
                padding: 30px 20px;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
                border-left: 5px solid;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                position: relative;
                overflow: hidden;
            }

            .metric-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 3px;
                background: linear-gradient(90deg, transparent, currentColor, transparent);
                opacity: 0.3;
            }

            .metric-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
            }

            .metric-card h4 {
                font-size: 1.1rem;
                font-weight: 600;
                margin: 0 0 15px 0;
                text-transform: uppercase;
                letter-spacing: 1px;
            }

            .metric-card h2 {
                font-size: 2.5rem;
                font-weight: 700;
                margin: 0 0 10px 0;
                color: #2c3e50;
            }

            .metric-card p {
                font-size: 0.9rem;
                color: #7f8c8d;
                margin: 0;
                font-weight: 500;
            }

            .control-section {
                background: white;
                padding: 25px;
                border-radius: 15px;
                margin-bottom: 30px;
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
                border: 1px solid #e9ecef;
            }

            .control-section h4 {
                color: #2c3e50;
                font-size: 1.2rem;
                font-weight: 600;
                margin: 0 0 20px 0;
                display: flex;
                align-items: center;
                gap: 10px;
            }

            .control-section h4::before {
                content: '🌍';
                font-size: 1.5rem;
            }

            .radio-container {
                display: flex;
                gap: 15px;
                flex-wrap: wrap;
                justify-content: center;
            }

            .radio-item {
                background: #f8f9fa;
                padding: 12px 20px;
                border-radius: 25px;
                border: 2px solid #e9ecef;
                cursor: pointer;
                transition: all 0.3s ease;
                font-weight: 500;
                text-transform: capitalize;
                position: relative;
            }

            .radio-item:hover {
                background: #e3f2fd;
                border-color: #2196f3;
                transform: translateY(-2px);
            }

            .radio-item.selected {
                background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
                color: white;
                border-color: #4facfe;
                box-shadow: 0 5px 15px rgba(79, 172, 254, 0.4);
            }

            .chart-container {
                background: white;
                padding: 20px;
                border-radius: 15px;
                margin-bottom: 30px;
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
                border: 1px solid #e9ecef;
            }

            .conclusion-section {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px 30px;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
                margin-top: 30px;
            }

            .conclusion-section h3 {
                font-size: 2rem;
                font-weight: 700;
                margin: 0 0 25px 0;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
            }

            .conclusion-content {
                background: rgba(255, 255, 255, 0.15);
                backdrop-filter: blur(10px);
                padding: 30px;
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.2);
            }

            .conclusion-content p {
                font-size: 1.2rem;
                line-height: 1.6;
                margin: 0 0 15px 0;
            }

            .conclusion-content strong {
                font-weight: 700;
                text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
            }

            .pulse {
                animation: pulse 2s infinite;
            }

            @keyframes pulse {
                0% { opacity: 1; }
                50% { opacity: 0.8; }
                100% { opacity: 1; }
            }

            /* Responsive design */
            @media (max-width: 768px) {
                .metrics-container {
                    flex-direction: column;
                }

                .radio-container {
                    flex-direction: column;
                    align-items: center;
                }

                .header-section h1 {
                    font-size: 2rem;
                }

                .dashboard-container {
                    margin: 10px;
                    padding: 20px;
                }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''


def load_and_process_data(csv_file='pink_morsel_sales_consolidated.csv'):
    df = pd.read_csv(csv_file)

    # Ensure Date column is datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Sort by date
    df = df.sort_values('Date').reset_index(drop=True)

    return df


def create_processed_data():
    """
    Create processed data from raw CSV files if consolidated file doesn't exist.
    """
    input_files = [
        'data/daily_sales_data_0.csv',
        'data/daily_sales_data_1.csv',
        'data/daily_sales_data_2.csv'
    ]

    all_data = []
    for file_path in input_files:
        try:
            df = pd.read_csv(file_path)
            all_data.append(df)
        except FileNotFoundError:
            print(f"Warning: {file_path} not found")


    # Combine and process
    combined_df = pd.concat(all_data, ignore_index=True)
    pink_morsel_df = combined_df[
        combined_df['product'].str.lower() == 'pink morsel'
        ].copy()

    # Parse price and calculate sales
    pink_morsel_df['price_numeric'] = pink_morsel_df['price'].str.replace('$', '').astype(float)
    pink_morsel_df['Sales'] = pink_morsel_df['price_numeric'] * pink_morsel_df['quantity']

    # Create output format
    output_df = pink_morsel_df[['Sales', 'date', 'region']].copy()
    output_df.rename(columns={'date': 'Date', 'region': 'Region'}, inplace=True)

    return output_df



# Load the data
df = load_and_process_data()

# Define the price increase date
PRICE_INCREASE_DATE = datetime(2021, 1, 15)


def create_sales_chart(df, selected_region='all'):
    """Create the main sales line chart with optional region filtering."""

    # Filter data by region if not 'all'
    if selected_region != 'all':
        filtered_df = df[df['Region'].str.lower() == selected_region.lower()].copy()
        chart_title = f'Pink Morsel Daily Sales - {selected_region.title()} Region'
    else:
        filtered_df = df.copy()
        chart_title = 'Pink Morsel Daily Sales - All Regions'

    # Aggregate daily sales
    daily_sales = filtered_df.groupby('Date')['Sales'].sum().reset_index()

    # Create the line chart
    fig = go.Figure()

    # Add the main sales line with gradient effect
    fig.add_trace(go.Scatter(
        x=daily_sales['Date'],
        y=daily_sales['Sales'],
        mode='lines',
        name='Daily Sales',
        line=dict(color='#4facfe', width=3),
        fill='tonexty',
        fillcolor='rgba(79, 172, 254, 0.1)',
        hovertemplate='<b>Date:</b> %{x}<br><b>Sales:</b> $%{y:,.0f}<extra></extra>'
    ))

    # Convert price increase date to same format as data
    price_increase_str = PRICE_INCREASE_DATE.strftime('%Y-%m-%d')

    # Add vertical line for price increase
    fig.add_shape(
        type="line",
        x0=price_increase_str,
        y0=0,
        x1=price_increase_str,
        y1=1,
        yref="paper",
        line=dict(color="#e74c3c", width=3, dash="dash")
    )

    # Add annotation for the price increase line
    fig.add_annotation(
        x=price_increase_str,
        y=0.95,
        yref="paper",
        text="💰 Price Increase<br>Jan 15, 2021",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#e74c3c",
        bgcolor="rgba(255, 255, 255, 0.9)",
        bordercolor="#e74c3c",
        borderwidth=2,
        font=dict(size=12, color="#e74c3c")
    )

    # Add shaded regions
    fig.add_shape(
        type="rect",
        x0=daily_sales['Date'].min(),
        y0=0,
        x1=price_increase_str,
        y1=1,
        yref="paper",
        fillcolor="rgba(52, 152, 219, 0.1)",
        opacity=0.3,
        line_width=0,
        layer="below"
    )

    fig.add_shape(
        type="rect",
        x0=price_increase_str,
        y0=0,
        x1=daily_sales['Date'].max(),
        y1=1,
        yref="paper",
        fillcolor="rgba(46, 204, 113, 0.1)",
        opacity=0.3,
        line_width=0,
        layer="below"
    )

    # Update layout with modern styling
    fig.update_layout(
        title={
            'text': chart_title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 24, 'family': 'Inter', 'color': '#2c3e50'}
        },
        xaxis_title='Date',
        yaxis_title='Daily Sales ($)',
        yaxis=dict(tickformat='$,.0f', gridcolor='rgba(0,0,0,0.1)'),
        xaxis=dict(gridcolor='rgba(0,0,0,0.1)'),
        hovermode='x unified',
        height=500,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter', size=12, color='#2c3e50')
    )

    return fig


def calculate_period_stats(df, selected_region='all'):
    """Calculate statistics before and after the price increase."""

    # Filter by region if not 'all'
    if selected_region != 'all':
        df = df[df['Region'].str.lower() == selected_region.lower()].copy()

    df_copy = df.copy()
    df_copy['Date'] = pd.to_datetime(df_copy['Date'])

    before_increase = df_copy[df_copy['Date'] < PRICE_INCREASE_DATE]
    after_increase = df_copy[df_copy['Date'] >= PRICE_INCREASE_DATE]

    # Calculate daily averages
    before_daily = before_increase.groupby('Date')['Sales'].sum()
    after_daily = after_increase.groupby('Date')['Sales'].sum()

    if len(before_daily) == 0 or len(after_daily) == 0:
        return {
            'before_avg': 0,
            'after_avg': 0,
            'before_total': 0,
            'after_total': 0,
            'before_days': 0,
            'after_days': 0,
            'percent_change': 0
        }

    stats = {
        'before_avg': before_daily.mean(),
        'after_avg': after_daily.mean(),
        'before_total': before_increase['Sales'].sum(),
        'after_total': after_increase['Sales'].sum(),
        'before_days': len(before_daily),
        'after_days': len(after_daily),
        'percent_change': ((after_daily.mean() - before_daily.mean()) / before_daily.mean()) * 100
    }

    return stats


# Calculate initial statistics
stats = calculate_period_stats(df)

# Define the app layout
app.layout = html.Div([
    html.Div([
        # Header
        html.Div([
            html.H1("🍓 Pink Morsel Sales Analytics", className="pulse"),
            html.H3("Impact Analysis: Price Increase Strategy • January 15th, 2021")
        ], className="header-section"),

        # Key Metrics Cards
        html.Div([
            html.Div([
                html.H4("📊 Before Price Increase", style={'color': '#3498db'}),
                html.H2(id="before-metric", children=f"${stats['before_avg']:,.0f}"),
                html.P("Average Daily Sales")
            ], className="metric-card", style={'border-left-color': '#3498db'}),

            html.Div([
                html.H4("📈 After Price Increase", style={'color': '#27ae60'}),
                html.H2(id="after-metric", children=f"${stats['after_avg']:,.0f}"),
                html.P("Average Daily Sales")
            ], className="metric-card", style={'border-left-color': '#27ae60'}),

            html.Div([
                html.H4("📊 Performance Change",
                        style={'color': '#e74c3c' if stats['percent_change'] < 0 else '#27ae60'}),
                html.H2(id="change-metric", children=f"{stats['percent_change']:+.1f}%"),
                html.P("Percentage Impact")
            ], className="metric-card",
                style={'border-left-color': '#e74c3c' if stats['percent_change'] < 0 else '#27ae60'})
        ], className="metrics-container"),

        # Region Filter Control
        html.Div([
            html.H4("🌍 Regional Analysis Filter"),
            dcc.RadioItems(
                id='region-filter',
                options=[
                    {'label': 'All Regions', 'value': 'all'},
                    {'label': 'North', 'value': 'north'},
                    {'label': 'South', 'value': 'south'},
                    {'label': 'East', 'value': 'east'},
                    {'label': 'West', 'value': 'west'}
                ],
                value='all',
                className="radio-container",
                labelStyle={'display': 'inline-block', 'margin-right': '20px'},
                inputStyle={'margin-right': '8px'}
            )
        ], className="control-section"),

        # Main Chart
        html.Div([
            dcc.Graph(id='sales-chart')
        ], className="chart-container"),

        # Regional Breakdown Chart
        html.Div([
            html.H3("📍 Sales Distribution by Region",
                    style={'textAlign': 'center', 'color': '#2c3e50', 'margin-bottom': '20px'}),
            dcc.Graph(
                id='regional-chart',
                figure=px.box(
                    df,
                    x='Region',
                    y='Sales',
                    title='',
                    template='plotly_white',
                    color='Region',
                    color_discrete_sequence=['#4facfe', '#00f2fe', '#667eea', '#764ba2']
                ).update_layout(
                    height=400,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(family='Inter', size=12, color='#2c3e50'),
                    showlegend=False
                )
            )
        ], className="chart-container"),

        # Business Conclusion
        html.Div([
            html.H3("🎯 Strategic Business Insights"),
            html.Div(id="conclusion-content", children=[
                html.P([
                    "📈 The data reveals that Pink Morsel sales were ",
                    html.Strong(
                        "SIGNIFICANTLY HIGHER" if stats['percent_change'] > 0 else "LOWER",
                        className="pulse"
                    ),
                    " after the strategic price increase on January 15th, 2021."
                ]),
                html.P([
                    "💰 Revenue performance improved by ",
                    html.Strong(f"{stats['percent_change']:+.1f}%"),
                    f" with daily averages rising from ${stats['before_avg']:,.0f} to ${stats['after_avg']:,.0f}."
                ])
            ], className="conclusion-content")
        ], className="conclusion-section")

    ], className="dashboard-container")
], style={'min-height': '100vh'})


# Callback for updating chart and metrics based on region selection
@app.callback(
    [Output('sales-chart', 'figure'),
     Output('before-metric', 'children'),
     Output('after-metric', 'children'),
     Output('change-metric', 'children'),
     Output('conclusion-content', 'children')],
    [Input('region-filter', 'value')]
)
def update_dashboard(selected_region):
    # Calculate new statistics for selected region
    new_stats = calculate_period_stats(df, selected_region)

    # Update chart
    new_figure = create_sales_chart(df, selected_region)

    # Update metrics
    before_metric = f"${new_stats['before_avg']:,.0f}"
    after_metric = f"${new_stats['after_avg']:,.0f}"
    change_metric = f"{new_stats['percent_change']:+.1f}%"

    # Update conclusion
    region_text = f" in the {selected_region.title()} region" if selected_region != 'all' else ""
    conclusion = [
        html.P([
            f"📈 The data reveals that Pink Morsel sales{region_text} were ",
            html.Strong(
                "SIGNIFICANTLY HIGHER" if new_stats['percent_change'] > 0 else "LOWER",
                className="pulse"
            ),
            " after the strategic price increase on January 15th, 2021."
        ]),
        html.P([
            "💰 Revenue performance changed by ",
            html.Strong(f"{new_stats['percent_change']:+.1f}%"),
            f" with daily averages moving from ${new_stats['before_avg']:,.0f} to ${new_stats['after_avg']:,.0f}."
        ])
    ]

    return new_figure, before_metric, after_metric, change_metric, conclusion


# Run the app
if __name__ == '__main__':
    app.run(debug=True)