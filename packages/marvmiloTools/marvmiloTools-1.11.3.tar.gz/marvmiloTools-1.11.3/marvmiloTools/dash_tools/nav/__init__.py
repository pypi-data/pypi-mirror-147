import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State

#import other scripts
from . import item

#function for creating Navbar
def bar(
    logo = None, 
    logo_style = {
        "width": "3rem", 
        "height": "3rem",
        "backgroundSize": "cover",
    }, 
    title = "", 
    title_style = {
        "width": "15rem",
        "fontSize": "1.5rem"
    },
    href = "/", 
    items = [], 
    color = "primary", 
    dark = True,
    expand = "lg"
):
    return dbc.Navbar(
        children = [
            html.A(
                html.Div(
                    children = [
                        html.Div(
                            style = {
                                "backgroundImage": logo,
                                **logo_style
                            }
                        ),
                        html.Div(style = {"width": "1rem"}),
                        html.Div(
                            html.Strong(title), 
                            style = title_style
                        ),
                    ],
                    style = {
                        "display": "flex",
                        "flexWrap": "nowrap",
                        "alignItems": "center",
                        "flexDirection": "row",
                    }
                ),
                href = href,
                className = "a-nav"
            ),
            dbc.NavbarToggler(
                id="navbar-toggler", 
                n_clicks=0,
                style = {
                    "marginTop": "0.5rem",
                    "marginBottom": "0.5rem",
                    "marginLeft": "0.5rem"
                }
            ),
            dbc.Collapse(
                items, id="navbar-collapse", navbar=True, is_open=False
            ),
        ],
        color = color,
        dark = dark,
        expand = expand,
        style =  {
            "padding": "1rem 10%",
            "position": "sticky",
            "top": 0,
            "zIndex": 100
        }
    )

#calback:
callback_args = [
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
]
def callback_function(n, is_open):
    if n:
        return not is_open
    return is_open