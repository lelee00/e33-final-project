import pandas as pd
import numpy as np
import altair as alt
from altair.expr import datum
from vega_datasets import data
import os
import re
import sys

def create_interactive_chart():
  legislation = pd.read_csv('https://chronicdata.cdc.gov/api/views/nxst-x9p4/rows.csv?accessType=DOWNLOAD')
  activity = pd.read_csv('https://chronicdata.cdc.gov/api/views/hn4x-zwk7/rows.csv?accessType=DOWNLOAD')
  ansi = pd.read_csv('https://www2.census.gov/geo/docs/reference/state.txt', sep='|')
  ansi.columns = ['id', 'abbr', 'LocationDesc', 'statens']
  ansi = ansi[['id', 'abbr', 'LocationDesc']]
  
  print('transforming data...')
  count_passed_bills = legislation[legislation.Status == 'Enacted'].drop_duplicates().groupby(
    ['LocationDesc','GeoLocation'])[['ProvisionID']].agg('count').reset_index()
  
  legislation_obesity = count_passed_bills.merge(
    activity[(activity.Question == 'Percent of adults aged 18 years and older who have obesity') 
              & (activity.StratificationCategoryId1 == 'OVR')].groupby(
      ['LocationDesc']
      ).Data_Value.agg(
      'mean'
     ).reset_index()
  ).merge(
      ansi
  ).rename(
     columns = {'ProvisionID':'Number of Relevant Bills Enacted', 
                'Data_Value':'Percent of Obese Adults','LocationDesc':'State'}
  )

  legislation_obesity['lat'] = legislation_obesity.GeoLocation.apply(lambda x: float(re.sub('[()]','',x).split(', ')[0]))
  legislation_obesity['lon'] = legislation_obesity.GeoLocation.apply(lambda x: float(re.sub('[()]','',x).split(', ')[1]))
  
  print('visualizing data...')
  
  alt.data_transformers.disable_max_rows()
  states = alt.topo_feature(data.us_10m.url,'states')
  hover = alt.selection(type='single', on='mouseover', nearest=True,
                      fields=['lat', 'lon'])

  base = alt.Chart(states).mark_geoshape(fill = 'lightgrey', stroke = 'white').properties(
     title='Obesity in the United States versus Related Legislature Enacted, 2011 - 2017',
     width=650,
     height=400
  ).project('albersUsa')


  colors = alt.Chart(states).mark_geoshape().project(
      'albersUsa'
  ).encode(
     color = alt.Color('Percent of Obese Adults:Q', 
                       scale = alt.Scale(scheme = 'redyellowgreen'), 
                       sort = 'descending'), 
      tooltip = ['Percent of Obese Adults:Q',
                'State:N']
  ).transform_lookup(
     lookup = 'id', 
     from_=alt.LookupData(legislation_obesity, 
                          'id',
                           ['State', 'Percent of Obese Adults'])
  )

  points = alt.Chart(legislation_obesity).encode(
      longitude='lon:Q',
      latitude='lat:Q',
  ).mark_circle().encode(
     color= alt.Color('Number of Relevant Bills Enacted:Q', 
                       scale = alt.Scale(scheme = 'redyellowgreen'), 
                       sort = 'ascending'
                     ),
     stroke = alt.value('white'),
     size=alt.condition(~hover, 
                        'Number of Relevant Bills Enacted:Q', 
                        alt.value(1)
                        ),
      tooltip = ['State:N', 'Number of Relevant Bills Enacted:Q','Percent of Obese Adults:Q']
  ).add_selection(hover)
 
  scatter_points = alt.Chart(legislation_obesity).mark_point().encode(
    alt.X('Number of Relevant Bills Enacted:Q'),
    alt.Y('Percent of Obese Adults:Q')
  )
  scatter_line = alt.Chart(legislation_obesity).mark_line().encode(
    alt.X('Number of Relevant Bills Enacted:Q'),
    alt.Y('Percent of Obese Adults:Q')
  )
  
 
  scattered = alt.layer(scatter_line, scatter_points)
  out = alt.layer(base, colors, points).resolve_scale(color = 'independent', size = 'independent')
  
  out.save('us-obesity.html')
  scattered.save('us-scatter.html')
  
  
if __name__ == '__main__':
#   os.system('bash requirements.sh')
  os.system('bash cdc_data.sh')
  
  bucket_name = sys.argv[1]
  create_interactive_chart()
  
  os.system('gsutil cp CDC_nutrition-legislation.csv gs://' + bucket_name + '/nutrition/')
  os.system('gsutil cp CDC_nutrition-and-activity.csv gs://' + bucket_name + '/nutrition/')
  os.system('gsutil cp us-obesity.html gs://' + bucket_name + '/nutrition/')
  os.system('gsutil cp us-scatter.html gs://' + bucket_name + '/nutrition/')
  
