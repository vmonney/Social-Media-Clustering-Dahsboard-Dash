"""Create a dashboard using the results of the clustering analysis."""
# Import dependencies
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# Create an instance of the app
app = Dash(
    "Cluster Dashboard",
    external_stylesheets=["https://codepen.io/chriddyp/pen/bWLwgP.css"],
)

# Load data using pandas
cluster_results = pd.read_csv("cluster_results.csv")


# Define a function to create scatter plots for categorical data
def create_scatter_plot(
    df: pd.DataFrame,
    x: str,
    y: str,
    color: str,
    title: str,
) -> px.scatter:
    """Create a scatter plot using plotly express."""
    fig = px.scatter(
        df,
        x=x,
        y=y,
        color=color,
        title=title,
        category_orders={"cluster": [str(i) for i in range(4)]},
        labels={color: "Cluster"},  # Rename legend title
    )
    fig.update_traces(
        marker={
            "size": 10,
            "opacity": 0.8,
            "line": {"width": 0.5, "color": "DarkSlateGrey"},
        },
    )
    fig.update_layout(legend_title_text="Cluster")
    fig.update_coloraxes(showscale=False)  # Hide the continuous color scale
    return fig


# Create plots with plotly express using the defined function
fig1 = create_scatter_plot(
    cluster_results,
    "num_comments",
    "num_reactions",
    "cluster",
    "Comments vs Reactions",
)
fig2 = create_scatter_plot(
    cluster_results,
    "num_shares",
    "num_likes",
    "cluster",
    "Shares vs Likes",
)
fig3 = create_scatter_plot(
    cluster_results,
    "num_angrys",
    "num_sads",
    "cluster",
    "Angrys vs Sads",
)
fig4 = create_scatter_plot(
    cluster_results,
    "num_loves",
    "num_wows",
    "cluster",
    "Loves vs Wows",
)


# Adjust the layout of each figure
for fig in [fig1, fig2, fig3, fig4]:
    fig.update_layout(margin={"l": 40, "r": 40, "t": 40, "b": 30})

# Create app layout
app.layout = html.Div(
    children=[
        html.H1(children="Cluster Dashboard", style={"textAlign": "center"}),
        html.Div(
            children="Showcasing your results using Dash",
            style={"textAlign": "center"},
        ),
        dcc.Graph(id="comments", figure=fig1),
        dcc.Graph(id="shares", figure=fig2),
        dcc.Graph(id="angrys", figure=fig3),
        dcc.Graph(id="loves", figure=fig4),
    ],
    style={
        "font-family": "Roboto",
        "margin": "0 auto",
        "width": "70%",
        "padding": "10px",
    },
)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
