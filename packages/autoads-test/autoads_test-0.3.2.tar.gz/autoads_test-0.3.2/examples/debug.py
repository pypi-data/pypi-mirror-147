import pandas as pd
from autoads.keywords import get_keywords_from_google, get_keywords_metrics_google
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

df_path = 'data/keywords_to_upload.csv' # specify keywords to uplod csv here
save_path = 'data'
path = '/home/maunish/Upwork Projects/Google-Ads-Project/examples/google-ads.yaml'
customer_id = '6554081276'
seed_keywords = ["crypto 401k", "real estate 401k", "esg 401k", "business 401k", "business crypto 401k", "business esg 401k"] 
    
# googleads_client = GoogleAdsClient.load_from_storage(path=path, version="v9")
# df_google = get_keywords_from_google(googleads_client,customer_id,seed_keywords)
# df = get_keywords_metrics_google(googleads_client,customer_id,keywords=seed_keywords)

# campaign = BatchCampaigns()

df = pd.read_csv('data/resource.csv')
resource_names = df['resource_names'].tolist()

resource_names = [x.split(':')[1].replace('"','') for x in resource_names]
campaigns_ids = [x.split('/')[-1] for x in resource_names if x.split('/')[-2] == 'campaigns']

print(campaigns_ids)