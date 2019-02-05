#!/bin/bash

# Usage: ./data_fetch.sh [city_name]

city=$1     # i.e. los-angeles

mkdir -p download_links
if [ -z "$city" ]
then
    city="all"
    curl -s http://insideairbnb.com/get-the-data.html | grep -Eo "http://[^\"]+gz" > download_links/data_download_links_$city.txt
else
    curl -s http://insideairbnb.com/get-the-data.html | grep -Eo "http://[^\"]+gz" | grep $city > download_links/data_download_links_$city.txt
fi

mkdir -p dataset/$city/
python3 download_rename.py download_links/data_download_links_$city.txt dataset/$city/
gzip -df dataset/$city/*.gz
aws s3 sync dataset/$city/ s3://airbnbdataset/$city/
