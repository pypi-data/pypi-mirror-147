import os
import re
import asyncio
import platform
from google.ads.googleads.client import GoogleAdsClient
from sentence_transformers import SentenceTransformer
from autoads.models import get_similarity_api, get_similarity_matrix
from autoads.keywords import get_organic_description
from autoads.gads import (get_existing_keywords,
                        get_search_term_report,get_all_ads,
                        get_shared_set_keywords)


email = 'weilbacherindustries@gmail.com' # email in data for seo
api_key = '05f014a493983975' # api key for data for seo
save_path = 'data' #all the csvs will be stored on this folder
path = 'data/google-ads.yaml'
customer_id = '8306215642' #google ads customer id
start_date='2022-01-01'
end_date='2022-01-02'

cost_threshold = 0  # get cost >= cost_threshold
conversion_threshold = 1 #  get conversion >= conversion_threshold
first_threshold = 0.8 # similarity threshold for keyword similarity
second_threshold = 0.8 # similarity threshold for description similarity
third_threshold = 0.35 # similarity threshold for seed keyword and keywords3

negative_first_threshold = 0.8 # if keyword similarity <= negative_threshold and conversion == 0 keyword negative
negative_second_threshold = 0.8 # if keyword similarity <= negative_threshold and conversion == 0 keyword negative
negative_third_threshold = 0.35 # if keyword similarity <= negative_threshold and conversion == 0 keyword negative

similarity_model_path = 'Maunish/ecomm-sbert' # this model is already uploaded on huggingface so no need to download

if platform.system()=='Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

os.makedirs(save_path,exist_ok=True)
os.makedirs(save_path+'/history',exist_ok=True)
googleads_client = GoogleAdsClient.load_from_storage(path=path, version="v9")

print("Getting existing keywords")
df_existing = get_existing_keywords(googleads_client,customer_id)
# df_existing = pd.read_csv('data/df_existing.csv')
keywords_to_remove = df_existing[df_existing['camp_status'].isin(['ENABLED'])]['keyword_name'].unique().tolist()

print("Getting search term report")
df_search_term_report = get_search_term_report(googleads_client,customer_id,start_date,end_date)
# df_search_term_report = pd.read_csv('data/search_term_df.csv')
df_search_term_report = df_search_term_report[~df_search_term_report['stv_status'].isin(['EXCLUDED','ADDED_EXCLUDED'])]
df_search_term_report = df_search_term_report.query("(campaign_status == 'ENABLED') & (adgroup_status == 'ENABLED')")
df_search_term_report['keyword_length'] = df_search_term_report['stv_search_term'].apply(lambda x:len(x))
df_search_term_report = df_search_term_report[df_search_term_report['keyword_length']<=80]
df_search_term_report = df_search_term_report.merge(df_existing.loc[:,['adgroup_id','keyword_name']],on='adgroup_id',how='left')
df_search_term_report['Keywords'] = df_search_term_report['stv_search_term']
df_search_term_report['Keywords2'] = df_search_term_report['keyword_name']

df_search_term_report['sum_conversion'] = df_search_term_report.groupby('date')['metrics_conversions'].transform(sum)
df_search_term_report_negative = df_search_term_report.loc[df_search_term_report['sum_conversion']==0]
# df_search_term_report_negative.to_csv(save_path+'/df_search_term_report_negative.csv',index=False)

df_exclude_from_negative = get_shared_set_keywords(googleads_client,customer_id)
exclude_keywords = df_exclude_from_negative['shared_criterion_keyword_text'].unique().tolist()
df_search_term_report_negative = df_search_term_report_negative.loc[~df_search_term_report_negative['stv_search_term'].isin(exclude_keywords)]
df_search_term_report_negative = df_search_term_report_negative.loc[df_search_term_report_negative['metrics_cost']>=cost_threshold * 1000000]
df_search_term_report_negative = df_search_term_report_negative.drop_duplicates("stv_search_term")
# df_search_term_report_negative.to_csv(save_path+'/df_search_term_report_negative.csv',index=False)

df_search_term_report = df_search_term_report.loc[df_search_term_report['metrics_conversions']>=conversion_threshold]
df_search_term_report = df_search_term_report[~df_search_term_report["Keywords"].isin(keywords_to_remove)]
df_search_term_report['camp_id'] = df_search_term_report['adgroup_camp'].apply(lambda x: x.split('/')[-1])
df_search_term_report =  df_search_term_report.drop_duplicates('Keywords')

print("Getting ads data")
df_ads_data = get_all_ads(googleads_client,customer_id)
# df_ads_data = pd.read_csv('data/df_ads_data.csv')
df_ads_data = df_ads_data.drop_duplicates(['adgroup_id']).reset_index(drop=True)

campaign_id_ads_data = df_ads_data['campaign_id'].unique().tolist()
ad_group_id_ads_data = df_ads_data['adgroup_id'].unique().tolist()

df_search_term_report = df_search_term_report[(df_search_term_report['camp_id'].isin(campaign_id_ads_data)) |
                                            (df_search_term_report['adgroup_id'].isin(ad_group_id_ads_data))].reset_index(drop=True)

model = SentenceTransformer(similarity_model_path)

def calculate_similarity(df,model,first_threshold,second_threshold,third_threshold,negative=False):
    print("Calculating First similarity keywords")
    df['Keywords'] = df['Keywords'].apply(lambda x:str(x))
    df['Keywords2'] = df['Keywords2'].apply(lambda x:str(x))

    keywords1 = df['Keywords'].tolist()
    keywords2 = df['Keywords2'].tolist()
    df['first_similarity'] = get_similarity_api(model,keywords1,keywords2)

    print("Getting Organic Description")
    seed_keywords = df["Keywords2"].unique().tolist()
    print(seed_keywords)
    seed_organic_description = asyncio.get_event_loop().run_until_complete(get_organic_description(email,api_key,seed_keywords))
    seed_organic_description = seed_organic_description.rename(columns={'organic_description':'seed_organic_description'})
    df = df.merge(seed_organic_description,how='left',left_on='Keywords2',right_on='keyword')

    all_keywords = df["Keywords"].unique().tolist()
    organic_description = asyncio.get_event_loop().run_until_complete(get_organic_description(email,api_key,all_keywords))
    df = df.merge(organic_description,how='left',left_on='Keywords',right_on='keyword')

    print("Performing similarity using organic description")
    for i,row in df.iterrows():
        all_titles = row['seed_organic_description'].split(',')
        all_seed_titles = row['organic_description'].split(',')
        similarity_matrix = get_similarity_matrix(model,all_titles,all_seed_titles)
        df.loc[i,'second_similarity'] = similarity_matrix.max(axis=1).mean()

    def remove_word(row):
        keyword1 = re.split("\s|(?<!\d)[,-](?!\d)",row['Keywords'])
        keyword2 = re.split("\s|(?<!\d)[,-](?!\d)",row['Keywords2'])
        keyword = [x for x in keyword1 if x not in keyword2]
        return "" if len(keyword) == 0 else ' '.join(keyword)

    df['Keywords3'] = df.apply(remove_word,axis=1)
    df['Keywords3'] = df['Keywords3'].apply(lambda x:str(x))

    print("Performing third similarity")
    keywords1 = df['Keywords2'].tolist()
    keywords2 = df['Keywords3'].tolist()
    df['third_similarity'] = get_similarity_api(model,keywords1,keywords2)

    if not negative:
        df = df[df['first_similarity']  >= first_threshold]
        df = df[df['second_similarity'] >= second_threshold]
        df = df[df['third_similarity']  >= third_threshold]
    else:
        df = df[df['first_similarity']  <= first_threshold]
        df = df[df['second_similarity'] <= second_threshold]
        df = df[df['third_similarity']  <= third_threshold]

    return df

if df_search_term_report.shape[0] != 0:
    df_search_term_report = calculate_similarity(df_search_term_report,
                                                model,
                                                first_threshold,
                                                second_threshold,
                                                third_threshold,
                                                negative=False)

    df_search_term_report.to_csv(save_path+'/df_search_term_report.csv',index=False)
else:
    print("No new keywords to add from search term report")

if df_search_term_report_negative.shape[0] != 0:
    df_search_term_report_negative = calculate_similarity(df_search_term_report_negative,
                                                model,
                                                negative_first_threshold,
                                                negative_second_threshold,
                                                negative_third_threshold,
                                                negative=True)

    df_search_term_report_negative.to_csv(save_path+'/df_search_term_report_negative.csv',index=False)
else:
    print("No new keywords to add to negative list")
