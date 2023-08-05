import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import string
import random

#import other scripts
from . import browsertime as bt_import
from . import nav as nav_import

#to get browsertime of current user
browsertime = bt_import
"""
# browsertime
Creating a Object in dash html form, wich provides the current clock time of the browser. That means the callbacks can calulate timezone of input.

### Add this to your callbacks:
```
app.clientside_callback(*mmt.dash.browsertime.clientside_callback_args)
```

### Add this in your html layout of the page: 
```
mmt.dash.browsertime.htmlObj()
```
### Example Callback with browser time:
```
from dash.dependencies import Input, Output, State

@app.callback(
    [Output(...)],
    [Input(...)],
    [State("browser-time", "data")]
)
def callback(... , browsertime):
    datetime_object = mmt.dash.browsertime.datetime(browsertime)
    time_shift = mmt.dash.browsertime.time_shift(browsertime)
```
### Also datetime objects from browsertime string can be created. Time shift can also be calculated.
"""

#navbar for dash plotly
nav = nav_import
"""
# nav
Simply creating a dash navbar with custom items.
```
import marvmiloTools as mmt

mmt.dash.nav.bar(
    logo = "url(/assets/logo.png)",
    logo_style = {
        "width": "3rem", 
        "height": "3rem",
        "background-size": "cover",
    },
    title = "Navbar Title",
    title_style = {
        "width": "15rem",
        "font-size": "1.5rem"
    }, 
    expand = "lg",
    items = [
        mmt.dash.nav.item.href(
            "Link",
            href = "https://github.com/marvmilo",
            target = "_blank",
            size = "lg"
        ),
        mmt.dash.nav.item.normal(
            "Button",
            id = "button-id",
            size = "lg"
        )
    ]
)

@app.callback(*mmt.dash.nav.callback_args)
def cn(n, is_open):
    return mmt.dash.nav.callback_function(n, is_open)
```
"""
 
#meta tags for mobile optimization
mobile_optimization = {"name": "viewport", "content": "width=device-width, initial-scale=1"}
"""
# mobile_optimization
Meta tags for setting app to a mobile optiomized app.
## Example:
```
import marvmiloTools as mmt
import dash

app = dash.Dash(__name__, meta_tags = [mmt.dash.mobile_optimization])
```
"""
 
#function for flex style
def flex_style(additional_dict = dict()):
    """
# flex_style
Dictionary for centering content in dash plotlys html.Div
## Example:
```
import marvmiloTools as mmt
from dash import html

html.Div(
    children = [
        "hello world"
    ],
    style = mmt.dash.flex_style({
        "background-color": "black"
    })
)
```
    """
    flex_style_dict = {
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center"
    }
    return {**flex_style_dict, **additional_dict}
 
#function for creating content div with specified width
def content_div(width, padding, children):
    """
# content_div
For creating a dynamic scalealbe content Div.
## Example:
```
import marvmiloTools as mmt
from dash import html
import dash_bootstrap_components as dbc

app.layout = html.Div(
    children = [
        dbc.Navbar(...),
        mmt.dash.content_div(
            width = "1000px",
            padding = "5%",
            content = [
                "children"
            ]
        )
    ]
)
```
    """
    return html.Div(
        html.Div(
            children = [
                *children,
                html.Div(style = {"width": width, "width": "100%"})
            ],
            style = {"maxWidth": width, "width": width}
        ),
        style = flex_style({"padding": padding})
    )
 
#function for creating modal header with close button
def modal_header_close(title, close_id , color = "#222"):
    """
# modal_header_close
Creating an modal header with close button and specific color.
## Example:
```
import marvmiloTools as mmt
import dash_bootstrap_components as dbc

dbc.Modal(
    children = [
        mmt.dash.modal_header_close(
            title = "This is the header",
            close_id = "modal-close", #id of the close button,
            color = "#4287f5" #background color of header
        ),
        dbc.Modal_Body("This is modal body")
    ]
)
```
    """
    return html.Div(
        children = [
            html.H5(
                title,
                className = "modal-title"
            ),
            dbc.Button(
                className = "btn-close",
                id = close_id
            )  
        ],
        className = "modal-header",
        style = {
            "background": color,
            "borderColor": color
        }
    )

#function for creating random dash id
def random_ID(length):
    """
# random_ID
Creating random IDs compatible with dash.
## Example:
```
import marvmiloTools as mmt
from dash import html

html.Div(
    children = "Hello World",
    id = mmt.dash.random_ID()
)
```
Output ID: 'MNPhNBfXcpVeHVVxuJeF' 
    """
    return "".join(random.choice(string.ascii_letters) for i in range(length))