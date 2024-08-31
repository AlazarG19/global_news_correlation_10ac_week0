import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import time
import pandas as pd
import re
import psycopg2
from dotenv import load_dotenv
import os
from flask import Flask, jsonify
from flask_cors import CORS
app = Flask(__name__)
import psycopg2
CORS(app)


# Load environment variables from .env file
load_dotenv()

try:
    instance = psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_DATABASE'],
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD']
    )
    print("Connected to instance database!")
except psycopg2.Error as e:
    print(f"Error connecting to database: {e}")
def execute_query( query):
    cur = instance.cursor()
    cur.execute(query)
    return cur,cur.fetchall()    

# start_time = time.time()

cur,results = execute_query("SELECT domain,source_name,article_id, mentioned_countries,title_sentiment from rating")
column_names = [desc[0] for desc in cur.description]
rating = pd.DataFrame(results, columns=column_names)

# print(f"Time taken to execute query and create rating DataFrame: {time.time() - start_time:.2f} seconds")

# print("rating.head()")
print(rating.columns)
# print(rating.count())

# start_time = time.time()
cur,results = execute_query("SELECT * from domains_location")
column_names = [desc[0] for desc in cur.description]
domains_location = pd.DataFrame(results, columns=column_names)
# print(f"Time taken to execute query and create domains_location DataFrame: {time.time() - start_time:.2f} seconds")


# print("domains_location.head()")
print(domains_location.columns)

# start_time = time.time()
cur,results = execute_query("SELECT \"GlobalRank\", \"domain\" from traffic")
column_names = [desc[0] for desc in cur.description]
traffic = pd.DataFrame(results, columns=column_names)
# print(f"Time taken to execute query and create trafficdate DataFrame: {time.time() - start_time:.2f} seconds")


# print("traffic.head()")
print(traffic.columns)

def get_barchartdata_with_grouping(df, x_axis, y_axis, top=10, ascending=True, grouping=""):
    ''' 
    a function to attain the barchart for dataframes that need to 
    be grouped before plotting
    '''
    data = {}
    if grouping == "":
        grouped = df.groupby(x_axis).count()
        sorted_df = grouped.sort_values(by=y_axis,ascending=ascending)

        json_format = {"x_axis":sorted_df.index[:top].tolist(), "y_axis":sorted_df[y_axis][:top].tolist()}
    else:
        grouped = df.groupby(x_axis).agg(Count=(grouping, 'count')).reset_index()
        sorted_df = grouped.sort_values(by="Count",ascending=ascending)
        
        json_format = {"x_axis":sorted_df[x_axis][:top].tolist(), "y_axis":sorted_df[y_axis][:top].tolist()}
    returnable_data = []
    for i in range(len(json_format["x_axis"])):
        returnable_data.append({"x_axis":json_format["x_axis"][i],"y_axis":json_format["y_axis"][i]})
    data = {"data":returnable_data}
    
    return data


def count_items_in_dataframes(dataframes_dict):
    """
    This function takes a dictionary of DataFrames and returns a dictionary
    with the DataFrame names as keys and the count of items (rows) in each DataFrame as values.
    
    :param dataframes_dict: dict, a dictionary where keys are DataFrame names (str)
                            and values are the corresponding DataFrames.
    :return: dict, a dictionary where keys are the DataFrame names and values are the row counts.
    """
    counts = {}
    for name, df in dataframes_dict.items():
        counts[name] = len(df)
    return counts

def get_piechartdata(df,label,count_label):
    grouped_df = df.groupby(label)[count_label].count().reset_index()
    grouped_df.columns = [label, count_label]

    # Convert the DataFrame to a list of dictionaries
    json_format = grouped_df.to_dict(orient='records')
    # json_format = {"x_axis":result[labels].tolist(), "y_axis":result[count_label].tolist()}
    return json_format


    
datafram_dict = {"rating":rating,"domains_location":domains_location,"traffic":traffic}
overview_result = count_items_in_dataframes(datafram_dict)
overview_result["new_features"] = 5
print("number of traffic,domain ",overview_result)
article_count_data = get_barchartdata_with_grouping(df=rating,x_axis="source_name",y_axis="article_id",
                                               ascending=False )
print("article count data",article_count_data)
print("piechartdata",get_piechartdata(rating,"title_sentiment","domain"))

@app.route('/', methods=['GET'])
def index():
    return "dfsdfs"

@app.route('/getoverviewcardvalues', methods=['GET'])
def get_overview_card_values():
    return jsonify(overview_result)

@app.route('/getarticlecountdata', methods=['GET'])
def get_article_count_data():
    return jsonify(article_count_data)

@app.route('/gettitlesentimentcomposition', methods=['GET'])
def get_title_sentiment_composition():
    return jsonify(get_piechartdata(rating,"title_sentiment","domain"))

@app.route('/getrating', methods=['GET'])
def get_rating():
    return jsonify(rating.to_dict(orient="records"))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)