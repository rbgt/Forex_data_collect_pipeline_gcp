# GCP forex data collect pipeline
In this project we implement a Data collection pipeline in GCP collecting forex data on the CHF/EUR pair
We have the following component :
- A Cloud Scheduler triggering the pipeline every day
- A Containerized Flask API collecting the data from a Forex API and publishing the data to a PubSub topic
- A Cloud PubSub stream processing service collecting the data
- An ETL Apache Beam script to subscribe to our PubSub topic, transforming the data and sinking it to a BigQuery Datawarehouse
- A BigQuery datawarehouse preparing views for Data visualization
- A Data visualization tool with Looker Studio
