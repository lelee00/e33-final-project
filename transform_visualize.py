!pip install pandas
import pandas as pd
!pip install numpy
import numpy as np
!pip install altair
import altair as alt
from altair.expr import datum
!pip install vega_datasets
from vega_datasets import data
import re
import os

def create_interactive_chart(bucket_name, folder_name):
  activity = pd.read_csv('gs://' + bucket_name + '/' + folder_name + '/' + 'CDC_nutrition-and-activity.csv')
  legislation = pd.read_csv('gs://' + bucket_name + '/' + folder_name + '/' + 'CDC_nutrition-legislation.csv')
  ansi = pd.read_csv('https://www2.census.gov/geo/docs/reference/state.txt', sep='|')
  ansi.columns = ['id', 'abbr', 'LocationDesc', 'statens']
  ansi = ansi[['id', 'abbr', 'LocationDesc']]

  legislation_obesity = legislation.groupby(
     ['LocationDesc','GeoLocation']
  )[['Citation']].agg(
    'count'
  ).reset_index().merge(
     activity[(activity.Question == 'Percent of adults aged 18 years and older who have obesity') 
              & (activity.StratificationCategoryId1 == 'OVR')].groupby(
      ['LocationDesc']
      ).Data_Value.agg(
      'mean'
     ).reset_index()
  ).merge(
      ansi
  ).rename(
     columns = {'Citation':'Number of Relevant Bills Proposed', 
                'Data_Value':'Percent of Obese Adults','LocationDesc':'State'}
  )

  legislation_obesity['lat'] = legislation_obesity.GeoLocation.apply(lambda x: float(re.sub('[()]','',x).split(', ')[0]))
  legislation_obesity['lon'] = legislation_obesity.GeoLocation.apply(lambda x: float(re.sub('[()]','',x).split(', ')[1]))
  
  alt.data_transformers.disable_max_rows()
  states = alt.topo_feature(data.us_10m.url,'states')
  hover = alt.selection(type='single', on='mouseover', nearest=True,
                      fields=['lat', 'lon'])

  base = alt.Chart(states).mark_geoshape(fill = 'lightgrey', stroke = 'white').properties(
     title='Obesity in the United States versus Related Legislature Proposed, 2011 - 2017',
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
                           ['Percent of Obese Adults',
                           'State'])
  )

  points = alt.Chart(legislation_obesity).encode(
      longitude='lon:Q',
      latitude='lat:Q',
  ).mark_circle().encode(
     color= alt.Color('Number of Relevant Bills Proposed:Q', 
                       scale = alt.Scale(scheme = 'redyellowgreen'), 
                       sort = 'ascending'
                     ),
     stroke = alt.value('white'),
     size=alt.condition(~hover, 
                        'Number of Relevant Bills Proposed:Q', 
                        alt.value(1)
                        ),
      tooltip = ['State',
                 'Number of Relevant Bills Proposed',
                'Percent of Obese Adults']
  ).add_selection(
     hover)


  out = alt.layer(base, colors, points).resolve_scale(color = 'independent', size = 'independent')
  out.save('us-obesity.html')
  
if __name__ == '__main__':
  bucket_name = os.sysdir[0]
  folder_name = os.sysdir[1]
  
