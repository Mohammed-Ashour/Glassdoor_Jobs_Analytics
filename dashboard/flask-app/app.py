
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
 

def plot(x_data, y_data, title):
    x = list(x_data)[:10]
    y = list(y_data)[:10]
    
    p = figure(x_range=x, plot_height=500, title=title,
           toolbar_location=None)
    p.vbar(x=x, top=y, width=1)

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    p.xaxis.major_label_orientation = 1
    script, div = components(p)
    return script, div
@app.route('/', methods=['GET', 'POST'])

def chart():

    script_industries,  div_industries = plot(df["Industry"].value_counts().index\
                                              , df["Industry"].value_counts(),
                                              title="Industry Job Posts Count")
    script_companies, div_companies = plot(df["Company Name"].value_counts().index\
                                              , df["Company Name"].value_counts(),\
                                              title="Company Job Posts Count")
    script_titles, div_titles = plot(df["Job Title"].value_counts().index\
                                              , df["Job Title"].value_counts(),\
                                              title="Titles Job Posts Count")
    
    
    kwargs = {'script': script_industries, 'div': div_industries,  'script_titles':script_titles\
              ,'div_titles': div_titles,\
             'script_companies':script_companies\
              ,'div_companies': div_companies}
    return render_template('index.html', **kwargs)   


if __name__ == '__main__':
    app.run(debug=True)