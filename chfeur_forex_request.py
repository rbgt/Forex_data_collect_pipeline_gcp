import requests
import json
import os
from io import StringIO
from google.cloud import storage, pubsub_v1
import pandas as pd
from flask import Flask

app = Flask(__name__)

def get_response(url):
    response = requests.get(url)
    response_json = json.loads(response.text)
    return response_json

# Publish to PubSub topic : forex-topic
def publish_pubsub(project, data):

    file = json.dumps(data)
    file = file.encode("utf-8") # Requis pour PubSub

    publisher = pubsub_v1.PublisherClient()
    topic_name = "projects/{}/topics/forex-topic".format(project)

    publisher.publish(topic_name, data=file)

@app.route("/")
def main():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./our-shield-373717-d72483295e2d.json" # A CHANGER AVEC UN NOUVEAU COMPTE
    project_id = "our-shield-373717" # A CHANGER AVEC UN NOUVEAU COMPTE
    file_name = "resp.txt"

    blobs = storage.Client(project="{}".format(project_id)).bucket("forex_api_bucket").list_blobs() # CHANGER LE NOM DE BUCKET
    blobs_list = list(blobs)
    files = [blobs_list[i].name for i in range(len(blobs_list))]
    
    if file_name in files: 
        dl_file = storage.Client(project="{}".format(project_id)).bucket("forex_api_bucket").blob(file_name).download_as_string() # CHANGER LE NOM DE BUCKET
        dl_file = dl_file.decode("utf-8")
        dl_file = StringIO(dl_file)
        pd.read_csv(dl_file, header=None).to_csv("./data/{}".format(file_name),index=None,header=None) # CHANGER LE DOSSIER


    url = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/chf/eur.json"
    resp = get_response(url)
    
    os.system("echo {} >> ./data/{}".format(resp, file_name))
    with open("./data/{}".format(file_name)) as f:
        print(f.read())

    storage.Client(project="{}".format(project_id)).bucket("forex_api_bucket").blob(file_name).upload_from_filename("./data/{}".format(file_name)) # CHANGER LE NOM DE BUCKET

    try:
        publish_pubsub(project=project_id,data=resp)
    except:
        print("couldn't load to pubsub")

    return resp

@app.route("/reset")
def reset():
    project_id = "our-shield-373717"
    file_name = "resp.txt"
    os.system("rm ./data/{}".format(file_name))
    storage.Client(project="{}".format(project_id)).bucket("forex_api_bucket").blob(file_name).delete()
    return "reset"
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",8080)))