
from flask import Flask, render_template, request
from flask.logging import create_logger
import logging
import pandas as pd
from cn_news_cluster.scrape_articles import WebsiteDatabase
from cn_news_cluster.params import Globals as glob
from cn_news_cluster.lexical_analysis import translate_df_cn_to_en


app = Flask(__name__)
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

DEFAULT_CLUSTERS = 10

@app.route("/update_db")
def update_db():
    webdb = WebsiteDatabase(glob.sites)
    result = webdb.update_db()
    html = f"<h3>Database Update</h3><p>{result}</p>"
    return html.format(format)


@app.route("/")
def home():
    # html = "<h3>Chinese Military News Topics Home</h3>"
    return render_template("home.html")
    # return html.format(format)


@app.route("/get_topics", methods=['GET','POST'])
def get_topics():
    try:
        num_clusters = int(request.args['num_clusters'])
    except ValueError:
        num_clusters = DEFAULT_CLUSTERS
    print(num_clusters)
    webdb = WebsiteDatabase(glob.sites)
    # Log the websites that we're using for topics
    sites = '\n\t'.join([site.name for site in webdb.sites])
    # TO DO:  Log the output prediction value
    LOG.info(f"Sites: \n{sites}")
    
    topics = pd.DataFrame(webdb.compute(num_clusters))
    # Ref: https://stackoverflow.com/questions/52644035/how-to-show-a-pandas-dataframe-into-a-existing-flask-html-table
    return render_template("simple.html", column_names=topics.columns.values, row_data=list(topics.values.tolist()),
                           zip=zip)

@app.route("/translated", methods=['GET','POST'])
def translated():
    try:
        num_clusters = int(request.args['num_clusters'])
    except ValueError:
        num_clusters = DEFAULT_CLUSTERS
    print(num_clusters)
    webdb = WebsiteDatabase(glob.sites)
    # Log the websites that we're using for topics
    sites = '\n\t'.join([site.name for site in webdb.sites])
    # TO DO:  Log the output prediction value
    LOG.info(f"Sites: \n{sites}")
    
    topics = pd.DataFrame(webdb.compute(num_clusters))
    # Ref: https://medium.com/analytics-vidhya/translate-list-and-pandas-data-frame-using-googletrans-library-in-python-f28b8cb84f21#:~:text=googletrans%20is%20really%20helpful%20in%20translating%20pandas%20data,you%20and%20save%20a%20good%20amount%20of%20time.
    t_df = translate_df_cn_to_en(topics)
    # Ref: https://stackoverflow.com/questions/52644035/how-to-show-a-pandas-dataframe-into-a-existing-flask-html-table
    return render_template("translated.html", column_names=topics.columns.values, row_data=list(topics.values.tolist()),
                           en_col_names=t_df.columns.values, en_row_data=list(t_df.values.tolist()),
                           zip=zip)


if __name__ == "__main__":
    # load pretrained model as clf
    app.run(host='0.0.0.0', port=80, debug=False) # specify port=80