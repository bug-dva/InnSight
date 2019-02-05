# Innsight

A (machine learning powered) platform providing competitive insights and price prediction on Airbnb rental properties, to help Airbnb hosts optimize their pricing strategy.

## Business Value
There are more than 5M listings on Airbnb and more than 1M hosts worldwide. According to a recent report by Airbnb,hosts in California earned $2 billion, while welcoming 9.5 million guests in 2018. While this market is getting crazy, there are not many smart tools to help these hosts better.  

## Deliverable
A dashboard providing metrics including:
* Geographical Pricing Information (avg price/night, peak/off season)
* 5 Most Comparable Properties (location, size, price, quality, review)
* Price Suggestion (Calculated by Ordinary Least Squares (OLS) model)
* Revenue Estimate

## Data Source
InsideAirbnb at http://insideairbnb.com/get-the-data.html
* Total Data Size: ~100GB
* San Francisco data: ~7GB


## Tech Stack
![alt text][tech stack]

[tech stack]: https://github.com/bug-dva/PriceInsight/blob/master/src/common/images/tech%20stack.png

## Engineering Challenges
1. data is dirty, not well organized
* solution 1: automate the file download and clean process
2. location data comes as longitude and latitude
* solution 1: round to two decimals?
* solution 2: map to zip code?
3. choose the right machine learning model
* solution 1: Ordinary Least Squares(OLS)?

## MVP
Start with San Francisco data: clean data and finish statistics calculation

## Stretch Goals
* Achieve all planed deliverables, including the Machine Learning part
* Finish calculation for all cities
