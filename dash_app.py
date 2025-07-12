import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import datetime as dt
from datetime import datetime

# Initialize the Dash app
app = dash.Dash(__name__)


def load_and_process_data(csv_file='pink_morsel_sales_consolidated.csv'):
    df = pd.read_csv(csv_file)

    df['Date'] = pd.to_datetime(df['Date'])

    df = df.sort_values('Date').reset_index(drop=True)

    return df


def create_processed_data():

    input_files = [
        'data/daily_sales_data_0.csv',
        'data/daily_sales_data_1.csv',
        'data/daily_sales_data_2.csv'
    ]

    all_data = []

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


def create_sales_chart(df):

    # Aggregate daily sales across all regions
    daily_sales = df.groupby('Date')['Sales'].sum().reset_index()

    # Create the line chart
    fig = go.Figure()

    # Add the main sales line
    fig.add_trace(go.Scatter(
        x=daily_sales['Date'],
        y=daily_sales['Sales'],
        mode='lines',
        name='Daily Sales',
        line=dict(color='#2E86C1', width=2),
        hovertemplate='<b>Date:</b> %{x}<br><b>Sales:</b> $%{y:,.0f}<extra></extra>'
    ))

    # Convert price increase date to same format as data
    price_increase_str = PRICE_INCREASE_DATE.strftime('%Y-%m-%d')

    # Add vertical line for price increase using shapes instead of add_vline
    fig.add_shape(
        type="line",
        x0=price_increase_str,
        y0=0,
        x1=price_increase_str,
        y1=1,
        yref="paper",
        line=dict(color="red", width=2, dash="dash")
    )

    # Add annotation for the price increase line
    fig.add_annotation(
        x=price_increase_str,
        y=1,
        yref="paper",
        text="Price Increase<br>Jan 15, 2021",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="red",
        bgcolor="white",
        bordercolor="red",
        borderwidth=1
    )

    # Add shaded regions using shapes
    fig.add_shape(
        type="rect",
        x0=daily_sales['Date'].min(),
        y0=0,
        x1=price_increase_str,
        y1=1,
        yref="paper",
        fillcolor="lightblue",
        opacity=0.1,
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
        fillcolor="lightgreen",
        opacity=0.1,
        line_width=0,
        layer="below"
    )

    # Update layout
    fig.update_layout(
        title={
            'text': 'Pink Morsel Daily Sales Over Time',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        xaxis_title='Date',
        yaxis_title='Daily Sales ($)',
        yaxis=dict(tickformat='$,.0f'),
        hovermode='x unified',
        height=500,
        showlegend=True,
        template='plotly_white'
    )

    return fig


def calculate_period_stats(df):

    df_copy = df.copy()
    df_copy['Date'] = pd.to_datetime(df_copy['Date'])

    before_increase = df_copy[df_copy['Date'] < PRICE_INCREASE_DATE]
    after_increase = df_copy[df_copy['Date'] >= PRICE_INCREASE_DATE]

    # Calculate daily averages
    before_daily = before_increase.groupby('Date')['Sales'].sum()
    after_daily = after_increase.groupby('Date')['Sales'].sum()

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


# Calculate statistics
stats = calculate_period_stats(df)

# Define the app layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1(
            "Pink Morsel Sales Analysis Dashboard",
            style={
                'textAlign': 'center',
                'color': '#2C3E50',
                'marginBottom': '10px',
                'fontFamily': 'Arial, sans-serif'
            }
        ),
        html.H3(
            "Impact Analysis: Price Increase on January 15th, 2021",
            style={
                'textAlign': 'center',
                'color': '#7F8C8D',
                'marginBottom': '30px',
                'fontFamily': 'Arial, sans-serif',
                'fontWeight': 'normal'
            }
        )
    ], style={'marginBottom': '20px'}),

    # Key Metrics Cards
    html.Div([
        html.Div([
            html.H4("Before Price Increase", style={'color': '#3498DB', 'textAlign': 'center'}),
            html.H2(f"${stats['before_avg']:,.0f}", style={'textAlign': 'center', 'color': '#2C3E50'}),
            html.P("Average Daily Sales", style={'textAlign': 'center', 'color': '#7F8C8D'})
        ], className='metric-card', style={
            'backgroundColor': '#F8F9FA',
            'padding': '20px',
            'borderRadius': '10px',
            'margin': '10px',
            'border': '2px solid #3498DB',
            'flex': '1'
        }),

        html.Div([
            html.H4("After Price Increase", style={'color': '#27AE60', 'textAlign': 'center'}),
            html.H2(f"${stats['after_avg']:,.0f}", style={'textAlign': 'center', 'color': '#2C3E50'}),
            html.P("Average Daily Sales", style={'textAlign': 'center', 'color': '#7F8C8D'})
        ], className='metric-card', style={
            'backgroundColor': '#F8F9FA',
            'padding': '20px',
            'borderRadius': '10px',
            'margin': '10px',
            'border': '2px solid #27AE60',
            'flex': '1'
        }),

        html.Div([
            html.H4("Change",
                    style={'color': '#E74C3C' if stats['percent_change'] < 0 else '#27AE60', 'textAlign': 'center'}),
            html.H2(f"{stats['percent_change']:+.1f}%", style={
                'textAlign': 'center',
                'color': '#E74C3C' if stats['percent_change'] < 0 else '#27AE60'
            }),
            html.P("Percentage Change", style={'textAlign': 'center', 'color': '#7F8C8D'})
        ], className='metric-card', style={
            'backgroundColor': '#F8F9FA',
            'padding': '20px',
            'borderRadius': '10px',
            'margin': '10px',
            'border': f"2px solid {'#E74C3C' if stats['percent_change'] < 0 else '#27AE60'}",
            'flex': '1'
        })
    ], style={'display': 'flex', 'justifyContent': 'space-around', 'marginBottom': '30px'}),

    # Main Chart
    html.Div([
        dcc.Graph(
            id='sales-chart',
            figure=create_sales_chart(df)
        )
    ], style={'marginBottom': '30px'}),

    # Regional Breakdown
    html.Div([
        html.H3("Regional Sales Breakdown", style={'textAlign': 'center', 'color': '#2C3E50'}),
        dcc.Graph(
            id='regional-chart',
            figure=px.box(
                df,
                x='Region',
                y='Sales',
                title='Sales Distribution by Region',
                template='plotly_white'
            ).update_layout(height=400)
        )
    ]),

    # Business Conclusion
    html.Div([
        html.H3("Business Conclusion", style={'color': '#2C3E50', 'textAlign': 'center'}),
        html.Div([
            html.P([
                "The data clearly shows that Pink Morsel sales were ",
                html.Strong(
                    "HIGHER" if stats['percent_change'] > 0 else "LOWER",
                    style={'color': '#27AE60' if stats['percent_change'] > 0 else '#E74C3C'}
                ),
                " after the price increase on January 15th, 2021."
            ], style={'fontSize': '18px', 'textAlign': 'center'}),
            html.P([
                "Average daily sales changed by ",
                html.Strong(f"{stats['percent_change']:+.1f}%",
                            style={'color': '#27AE60' if stats['percent_change'] > 0 else '#E74C3C'}),
                f" from ${stats['before_avg']:,.0f} to ${stats['after_avg']:,.0f} per day."
            ], style={'fontSize': '16px', 'textAlign': 'center', 'color': '#7F8C8D'})
        ], style={
            'backgroundColor': '#F8F9FA',
            'padding': '30px',
            'borderRadius': '10px',
            'border': f"2px solid {'#27AE60' if stats['percent_change'] > 0 else '#E74C3C'}"
        })
    ], style={'margin': '30px 0'})

], style={'maxWidth': '1200px', 'margin': '0 auto', 'padding': '20px'})

# Run the app
if __name__ == '__main__':

    app.run(debug=True)