from google.ads.googleads.client import GoogleAdsClient
from autoads.gads import (get_all_ads,get_search_term_report,get_existing_keywords)

path = 'data/google-ads.yaml'
customer_id = '8306215642' #google ads customer id
start_date='2022-01-01'
end_date='2022-01-02'

googleads_client = GoogleAdsClient.load_from_storage(path=path, version="v9")
df_ads_data = get_all_ads(googleads_client,customer_id)

df_existing = get_existing_keywords(googleads_client,customer_id)
keywords_to_remove = df_existing[df_existing['camp_status'].isin(['ENABLED'])]['keyword_name'].unique().tolist()

df_search_term_report = get_search_term_report(googleads_client,customer_id,start_date,end_date)
df_search_term_report['camp_id'] = df_search_term_report['adgroup_camp'].apply(lambda x: x.split('/')[-1])
df_search_term_report['Keywords'] = df_search_term_report['stv_search_term']
df_search_term_report['Keywords2'] = df_search_term_report['keyword_name']
df_search_term_report = df_search_term_report[~df_search_term_report["Keywords"].isin(keywords_to_remove)]
df_search_term_report = df_search_term_report.loc[df_search_term_report['metrics_conversions']>=0]

print(df_search_term_report.shape)
print(df_ads_data.shape)

campaign_id_ads_data = df_ads_data['campaign_id'].unique().tolist()
ad_group_id_ads_data = df_ads_data['adgroup_id'].unique().tolist()

df_search_term_report = df_search_term_report[(df_search_term_report['camp_id'].isin(campaign_id_ads_data)) |
                                            (df_search_term_report['adgroup_id'].isin(ad_group_id_ads_data))].reset_index(drop=True)

print(df_search_term_report.shape)