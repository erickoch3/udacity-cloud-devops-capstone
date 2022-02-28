
from flask import Flask, render_template
from flask.logging import create_logger
import logging
import pandas as pd
from scrape_articles import WebsiteDatabase
from params import Globals as glob


app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)


@app.route("/update_db")
def update_db():
    webdb = WebsiteDatabase(glob.sites)
    result = webdb.update_db()
    html = f"<h3>Database Update</h3><p>{result}</p>"
    return html.format(format)


@app.route("/")
def home():
    html = f"<h3>Chinese Military News Topics Home</h3>"
    return html.format(format)

@app.route("/get_topics", methods=['GET'])
def get_topics():

    webdb = WebsiteDatabase(glob.sites)
    # Log the websites that we're using for topics
    sites = '\n\t'.join([site.name for site in webdb.sites])
    # TO DO:  Log the output prediction value
    LOG.info(f"Sites: \n{sites}")
    
    topics = pd.DataFrame(webdb.compute())
    # Ref: https://stackoverflow.com/questions/52644035/how-to-show-a-pandas-dataframe-into-a-existing-flask-html-table
    return render_template("simple.html", column_names=topics.columns.values, row_data=list(topics.values.tolist()),
                           zip=zip)

if __name__ == "__main__":
    # load pretrained model as clf
    app.run(host='0.0.0.0', port=80, debug=True) # specify port=80