import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import folium
from folium.plugins import HeatMap


# initialize the app
app = dash.Dash(__name__)

# add external styling
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

# set a title
app.title = "Beijing Housing Price"


# read the data
read = pd.read_csv("BJ_houseprice_17.csv", engine='python')
# filter dates in 2011-2017
# filtered = read.loc[(read['year']>2010) & (read['year']<2018)]

# filter the dataset
def filter_data(data, month):
    subset = data.loc[data['month']==month]
    return subset



def get_folium_map(data):
    # initialize the Folium map
    m = folium.Map(location=[39.919775,116.365913], tiles='cartodbpositron', zoom_start=11)
    locationlist = list(zip(data['Lat_transed'], data['Lng_transed']))
    HeatMap(locationlist).add_to(m)
    # define popup content
    # def popup(price, month):
    #     content = "Price: " + str(price) + "\nMonth: " + str(month)
    #     return content
    # # define color by price
    # def color(price):
    #     if (price < 40000): return '#38f5e8'
    #     elif (price >=40000) & (price < 60000): return '#5fd4da'
    #     elif (price >= 60000) & (price <80000): return '#87b4cb'
    #     elif (price >= 80000) & (price <100000): return '#ae93bd'
    #     else: return '#d572af'

    # for p in range(0, len(locationlist)):
    #     price = data['price'].iloc[p]
    #     month = data['month'].iloc[p]
    #     folium.CircleMarker(
    #         locationlist[p],
    #         radius=3,
    #         popup=popup(price, month),
    #         color=color(price),
    #         fill=True,
    #         fill_opacity=0.6).add_to(m)
    return m.get_root().render()


markdown_text = """
# Visualizing Beijing Housing Price
"""

# set the layout
app.layout = html.Div(
    [
        # the title!
        dcc.Markdown(markdown_text),
        # DIV ELEMENT FOR MONTH SLIDER
        html.Div(
            [
                html.Label("Select the number of month to query"),
                dcc.Slider(id="monthSlider", min=1, max=12, value=12),
                html.P(id="monthSliderValue", children=""),
            ],
            style={
                "width": "250px",
                "margin-right": "auto",
                "margin-left": "auto",
                "text-align": "center",
            },
        ),

        # MAP IFRAME
        html.Div(
            [
                html.Iframe(
                    id="map",
                    height="500",
                    width="800",
                    sandbox="allow-scripts",
                    style={"border-width": "0px", "align": "center"},
                )
            ],
            style={"display": "flex", "justify-content": "center"},
        ),
    ]
)


@app.callback(
    [dash.dependencies.Output("map", "srcDoc"),
    dash.dependencies.Output("monthSliderValue", "children")],
    [dash.dependencies.Input("monthSlider", "value")]
)

def render(month):
    # filter data
    data = filter_data(read, month)
    # make and return our map
    map = get_folium_map(data)
    month_text = "Month = %d" % month
    return map, month_text


if __name__ == "__main__":
    render(12)
    app.run_server(host="0.0.0.0", port=5000, debug=True)
