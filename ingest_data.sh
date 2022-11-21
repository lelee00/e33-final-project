#!/bin/bash

sudo apt-get install wget

# remove older copy of file, if it exists
rm -f CDC_Nutrition__Physical_Activity__and_Obesity_-_Legislation.csv
rm -f CDC_nutrition-legislation.csv

rm -f Nutrition__Physical_Activity__and_Obesity_-_Behavioral_Risk_Factor_Surveillance_System.csv
rm -f CDC_nutrition-and-activity.csv

# download latest data from CDC
wget https://chronicdata.cdc.gov/api/views/nxst-x9p4/rows.csv?accessType=DOWNLOAD -O CDC_nutrition-legislation.csv
wget https://chronicdata.cdc.gov/api/views/hn4x-zwk7/rows.csv?accessType=DOWNLOAD -O CDC_nutrition-and-activity.csv
