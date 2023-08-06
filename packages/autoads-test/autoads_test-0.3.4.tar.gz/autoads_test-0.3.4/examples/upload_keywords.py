import os
import uuid
import pandas as pd
from datetime import datetime
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from autoads.keywords import get_keywords_metrics2
from autoads.gads import BatchOperations, _handle_googleads_exception


df_path = 'data/keywords_to_upload.csv' # specify keywords to uplod csv here
save_path = 'data'
path = 'data/google-ads.yaml'
customer_id = '8306215642' 

email = 'weilbacherindustries@gmail.com'  # email in data for seo
api_key = '05f014a493983975'  # api key for data for seo

match_extract = ['exact', 'phrase']
budget = 100  # pass in USD

os.makedirs(save_path, exist_ok=True)
os.makedirs(save_path+'/history', exist_ok=True)
googleads_client = GoogleAdsClient.load_from_storage(path=path, version="v9")

df = pd.read_csv(df_path)
df = df.drop_duplicates("Keywords")
df_expand = df[~df['camp_id'].isna()].reset_index(drop=True)
df_create = df[df['camp_id'].isna()].reset_index(drop=True)

print("Getting keyword metrics")
df_create = get_keywords_metrics2(email, api_key, df_create, match_extract)

values = ['volume', 'cpc_exact', 'cpc_phrase']
df_create.loc[:, values] = df_create.loc[:, values] / 30
df_create['total_cost'] = 0.33 * df_create['volume'] * \
    ((df_create['cpc_exact'] + df_create['cpc_phrase']) / 2)
df_create['total_cost'] = df_create['total_cost'].cumsum()
df_create = df_create.sort_values(by=['total_cost'], na_position='last')
df_create = df_create[df_create['total_cost'] <= budget].reset_index(drop=True)

spendings = df_create['total_cost'].iloc[-1]

batch_operations = BatchOperations(
    googleads_client,
    customer_id
)

if len(df_expand) != 0:
    # code for expanding existing campaign
    print("Adding to existing campaign")
    for i, row in df_expand.iterrows():
        keyword = row['Keywords']
        campaign_id = str(int(row['camp_id']))
        batch_operations.create_adgroup(
            ad_group_name=keyword, campaign_id=campaign_id)
        batch_operations.create_keyword(keyword, kw_type='PHRASE')
        batch_operations.create_keyword(keyword, kw_type='EXACT')

    print(f"{df_expand.shape[0]} campaigns will be expanded")
else:
    print("No keywords to add into existing campaigns")

# Creating Campaigns
if len(df_create) != 0:
    spending_lt_budget = (spendings < budget)

    seed_keywords = df_create.groupby(['Keywords2']).groups
    for k, d in seed_keywords.items():
        batch_operations.create_budget(
            budget_name=k+'_budget_'+f"{uuid.uuid4()}", budget_dollars=budget)

        campaign_name = f'beta_{k}' if spending_lt_budget else k
        batch_operations.create_campaign(
            campaign_name=campaign_name + f"{uuid.uuid4()}")

        keywords = df_create.iloc[d]['Keywords'].tolist()
        for keyword in keywords:
            batch_operations.create_adgroup(ad_group_name=keyword)
            if spending_lt_budget:
                batch_operations.create_keyword(keyword, kw_type='BROAD')
            else:
                batch_operations.create_keyword(keyword, kw_type='EXACT')
                batch_operations.create_keyword(keyword, kw_type='PHRASE')

    if spending_lt_budget:
        print(f"{len(seed_keywords)} new beta campaigns will be created")
    else:
        print(f"{len(seed_keywords)} new campaigns will be created")
else:
    print("No new campaigns to create")

try:
    resource_names = batch_operations.run()  # runs all operations
except GoogleAdsException as ex:
    _handle_googleads_exception(ex)
