from flask import Flask, request, render_template
import pandas as pd
import altair as alt

# initialize the app
app = Flask(__name__)


# read the data
read = pd.read_csv("BJ_houseprice_prediction.csv", engine='python')
# filter dates in 2011-2017
filtered = read.loc[(read['year']>2010) & (read['year']<2018)]

# price (sq m)
# average home price per year and per month (price per square meter)
ave_price = filtered.groupby(['year', 'month'])['price'].mean().round().reset_index()
ave_price['date'] = pd.to_datetime(ave_price[['year', 'month']].assign(Day=1))
# average home price per year and per month and per district
price_dist = filtered.groupby(['year', 'month', 'district_name'])['price'].mean().round().reset_index()
price_dist['date'] = pd.to_datetime(price_dist[['year', 'month']].assign(Day=1))

# total price
# average total price per year and per month
ave_totalprice = filtered.groupby(['year', 'month'])['totalPrice'].mean().round().reset_index()
ave_totalprice['date'] = pd.to_datetime(ave_totalprice[['year', 'month']].assign(Day=1))
# average total price per year and per month and per district
totalprice_dist = filtered.groupby(['year', 'month', 'district_name'])['totalPrice'].mean().round().reset_index()
totalprice_dist['date'] = pd.to_datetime(price_dist[['year', 'month']].assign(Day=1))



def altair1(mydata):
    # basic line
    line = alt.Chart().mark_line().encode(
        x='date:T', y='price:Q',
        tooltip=[alt.Tooltip('price:Q', title='Price/m²'), alt.Tooltip('date:T', timeUnit='yearmonth', title='Date')]).properties(width=400)

    # add interactive line tooltips
    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['date'], empty='none')

    # Transparent selectors across the chart. This is what tells us the x-value of the cursor
    selectors = alt.Chart().mark_point().encode(
        x='date:T',
        opacity=alt.value(0),
    ).add_selection(nearest)

    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    # Draw a rule at the location of the selection
    rules = alt.Chart().mark_rule(color='gray').encode(
        x='date:T',
    ).transform_filter(nearest)

    # Put the layers into a chart and bind the data
    line_price = alt.layer(line, selectors, points, rules, data=mydata)
    return line_price


def altair2(mydata):
    # basic line
    line = alt.Chart().mark_line().encode(
        x='date:T', y='price:Q', color='district_name:N',
        tooltip=[alt.Tooltip('price:Q', title='Price/m²'),
                 alt.Tooltip('date:T', timeUnit='yearmonth', title='Date'),
                 alt.Tooltip('district_name:N', title="District")]).properties(width=400)

    # add interactive line tooltips: https://altair-viz.github.io/gallery/multiline_tooltip.html
    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['date'], empty='none')

    # Transparent selectors across the chart. This is what tells us the x-value of the cursor
    selectors = alt.Chart().mark_point().encode(
        x='date:T',
        opacity=alt.value(0)
    ).add_selection(
        nearest
    )

    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    # Draw a rule at the location of the selection
    rules = alt.Chart().mark_rule(color='gray').encode(
        x='date:T',
    ).transform_filter(
        nearest
    )

    # Put the layers into a chart and bind the data
    line_price_dist = alt.layer(line, selectors, points, rules, data=mydata)
    return line_price_dist


def altair3(mydata):
    # basic line
    line = alt.Chart().mark_line().encode(
        x='date:T', y='totalPrice:Q',
        tooltip=[alt.Tooltip('totalPrice:Q', title='Total Price (million)'), alt.Tooltip('date:T', timeUnit='yearmonth', title='Date')]).properties(width=400)

    # add interactive line tooltips: https://altair-viz.github.io/gallery/multiline_tooltip.html
    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['date'], empty='none')

    # Transparent selectors across the chart. This is what tells us the x-value of the cursor
    selectors = alt.Chart().mark_point().encode(
        x='date:T',
        opacity=alt.value(0),
    ).add_selection(
        nearest
    )

    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    # Draw a rule at the location of the selection
    rules = alt.Chart().mark_rule(color='gray').encode(
        x='date:T',
    ).transform_filter(
        nearest
    )

    # Put the layers into a chart and bind the data
    line_totalprice = alt.layer(line, selectors, points, rules, data=mydata)
    return line_totalprice


def altair4(mydata):
    # basic line
    line = alt.Chart().mark_line().encode(
        x='date:T', y='totalPrice:Q', color='district_name:N',
        tooltip=[alt.Tooltip('totalPrice:Q', title='Total Price (million)'),
                 alt.Tooltip('date:T', timeUnit='yearmonth', title='Date'),
                 alt.Tooltip('district_name:N', title="District")]).properties(width=400)

    # add interactive line tooltips: https://altair-viz.github.io/gallery/multiline_tooltip.html
    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(type='single', nearest=True, on='mouseover',
                            fields=['date'], empty='none')

    # Transparent selectors across the chart. This is what tells us the x-value of the cursor
    selectors = alt.Chart().mark_point().encode(
        x='date:T',
        opacity=alt.value(0),
    ).add_selection(
        nearest
    )

    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(
        opacity=alt.condition(nearest, alt.value(1), alt.value(0))
    )

    # Draw a rule at the location of the selection
    rules = alt.Chart().mark_rule(color='gray').encode(
        x='date:T',
    ).transform_filter(
        nearest
    )

    # Put the layers into a chart and bind the data
    line_totalprice_dist = alt.layer(line, selectors, points, rules, data=mydata)
    return line_totalprice_dist


def hconcat(chart1, chart2):
    return alt.hconcat(chart1, chart2)



@app.route('/')
def index():
    return render_template("template.html")

@app.route('/altair-price')
def chart_1():
    chart1 = altair1(ave_price)
    chart2 = altair2(price_dist)
    combined1 = hconcat(chart1, chart2)
    return combined1.to_json()

@app.route('/altair-totalprice')
def chart_2():
    chart3 = altair3(ave_totalprice)
    chart4 = altair4(totalprice_dist)
    combined2 = hconcat(chart3, chart4)
    return combined2.to_json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
