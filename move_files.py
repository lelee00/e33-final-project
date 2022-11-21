import os
import sys

if __name__ == '__main__':
  bucket_name = sys.argv[1]
  os.system('bash ingest_data.sh')
  os.system('gsutil cp CDC_nutrition-legislation.csv gs://' + bucket_name + '/nutrition/')
  os.system('gsutil cp CDC_nutrition-and-activity.csv gs://' + bucket_name + '/nutrition/')
  os.system('gsutil cp us-obesity.html gs://' + bucket_name + '/nutrition/')
