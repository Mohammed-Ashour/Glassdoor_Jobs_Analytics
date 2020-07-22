
import math
import numpy as np
import pandas as pd

from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool, PrintfTickFormatter
from bokeh.plotting import figure
from bokeh.transform import factor_cmap

from flask import Flask, render_template, request

df = pd.read_csv("../data/salaries_analysis_cleaned.csv")
    

app = Flask(__name__)
 
@app.route('/', methods=['GET', 'POST'])
def chart():
    x_data = list(df["Industry"].value_counts().index)[:10]
    y_data = list(df["Industry"].value_counts())[:10]
    
    p = figure(x_range=x_data, plot_height=500, title="Industry Counts",
           toolbar_location=None, tools="", plot_width=1000)
    p.vbar(x=x_data, top=y_data, width=2)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    # x = np.arange(2, 50, step=.5)
    # y = np.sqrt(x) + np.random.randint(2,50)
    # plot = figure(plot_width=400, plot_height=400,title=None, toolbar_location="below")
    # plot.circle(x,y)
    p.xaxis.major_label_orientation = 1
    script, div = components(p)
    kwargs = {'script': script, 'div': div}
    kwargs['title'] = 'bokeh-with-flask'    
    return render_template('index.html', **kwargs)   


if __name__ == '__main__':
    app.run(debug=True)