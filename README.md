# Innsight

InnSight is a platform to provide Airbnb hosts competitive insights on Airbnb rental properties and local market dynamics.

[Presentation Slide](http://bit.ly/innsightslide)

[Demo](http://bit.ly/innsight)

## Introduction
There are more than 5M listings on Airbnb and more than 1M hosts worldwide.

## Architecture
![alt text][tech stack]

[tech stack]: https://github.com/bug-dva/PriceInsight/blob/master/common/images/architecture.png

## Dataset
1. InsideAirbnb at http://insideairbnb.com/get-the-data.html
* Historical Data: 250GB
* New Data Crawled: ~10GB/Month

2. Real-time Data
* Local events data and real booking record data is simulated in the project for now.
* In the future, the real-time data can be fetched from APIs like PredictHD Events data API.

## Engineering Challenges

1. While the raw data comes in various schemas, a flexible data processing pipeline is needed. In order to be able to ingest data with different schemas, data format unification is needed at first. Also, there are lots of redundant data comes in the raw data, a clean step is necessary.
* solution: divide the spark batch processing job into two spark jobs. The first job is responsible for data cleaning and data format unification. The second spark job is for key metrics calculation.

2. The whole batch processing run time is long. In order to increase efficiency, parquet file format is used intermedium state.
* What is Parquet?:
* Why Parquet?:
* Performance Metrics: insert table

## Project Future
1. Add more metrics calculations
2. Add ML model to calculate weight of each feature, providing pricing model to hosts.
