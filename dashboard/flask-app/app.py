import logging
import itertools

import math
import numpy as np
import pandas as pd
import flask
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool, PrintfTickFormatter
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
import sys
from flask import Flask, render_template, request
from bokeh.palettes import Spectral6

df = pd.read_csv("../data/salaries_analysis_cleaned.csv")
    

app = Flask(__name__)
TECHNOLOGIES = ["python", " r ", "scala", "java", "sql", "nosql",\
                "julia", "matlab","spark", "hadoop", "tensorflow",\
                "pytorch", "pandas", "numpy", "scipy", "nodejs",\
                "js", "javascript", "aws", "azure"]

def plot(x_data, y_data, title):
    x = [str(i) for i in list(x_data)[:10]]
    y = list(y_data)[:10]
    
    p = figure(x_range=x, plot_height=500, title=title,
           toolbar_location=None)
    p.vbar(x=x, top=y, width=1, fill_color=factor_cmap('x', palette=Spectral6, factors=x))

    p.xgrid.grid_line_color = None
    p.y_range.start = 0

    p.xaxis.major_label_orientation = 1
    script, div = components(p)
    return script, div

def job_desc_analysis(job):
    counts = []
    jobs_desc = df[df["Job Title"]==job]["job_description_cleaned"]
    total_jobs_desc = ""
    for i in jobs_desc:
        total_jobs_desc +=" " + i
    # jobs_desc =  list(itertools.chain.from_iterable(jobs_desc))
    # print(jobs_desc)
    for w in TECHNOLOGIES:
        counts.append(total_jobs_desc.count(w))
    w_counts = list(zip(TECHNOLOGIES, counts))
    app.logger.info(w_counts)
    w_counts.sort(key = lambda x : x[1], reverse=True)
    return w_counts[:10]
            
    








@app.route('/', methods=['GET', 'POST'])
def chart():
    cat_cols = ["Industry", "python", "R","is_headquarters", "seniority", "Job Title"]
    kwargs = dict()
    for i in cat_cols:
        script, div = plot(df[i].value_counts().index\
                                              , df[i].value_counts(),
                                              title= i + " Job Posts Count")
        kwargs[i.replace(" ", "_") + "_script"] = script
        kwargs[i.replace(" ", "_") + "_div"] = div
    print(kwargs.keys(),  file=sys.stderr)

    # script_industries,  div_industries = plot(df["Industry"].value_counts().index\
    #                                           , df["Industry"].value_counts(),
    #                                           title="Industry Job Posts Count")
    # script_companies, div_companies = plot(df["Company Name"].value_counts().index\
    #                                           , df["Company Name"].value_counts(),\
    #                                           title="Company Job Posts Count")
    # script_titles, div_titles = plot(df["Job Title"].value_counts().index\
    #                                           , df["Job Title"].value_counts(),\
    #                                           title="Titles Job Posts Count")
    
    
    # kwargs = {'script': script_industries, 'div': div_industries,  'script_titles':script_titles\
    #           ,'div_titles': div_titles,\
    #           'script_companies':script_companies\
    #           ,'div_companies': div_companies}
    total_analysis = []
    for i in df["Job Title"].unique():
        analysis = job_desc_analysis(i)
        # final = ""
        # for j in analysis:
        #     final += str(j[0]) + " -> " + str(j[1]) + " <br> "
        # kwargs[i.replace(" ", "_")] = analysis
        analysis = [i,analysis]
        
        total_analysis.append(analysis)
    kwargs["total_analysis"] = total_analysis
    
        
        
    return render_template('index.html', **kwargs)   




if __name__ == '__main__':
    # chart()
    app.run(debug=True)