import os
import re
import uuid
import asyncio
import platform
import numpy as np
import pandas as pd
from google.ads.googleads.client import GoogleAdsClient
from sentence_transformers import SentenceTransformer
from autoads.gads import get_existing_keywords
from autoads.keywords import  get_organic_description
from autoads.models import get_similarity_matrix,get_similarity_api


email = 'weilbacherindustries@gmail.com' # email in data for seo
api_key = '05f014a493983975' # api key for data for seo
match_extract = ['exact', 'phrase']  # exact, phrase, broad
df_path = 'data/df_final.csv' # csv where keywords are stored
save_path = 'data' #all the csvs will be stored on this folder
path = 'data/google-ads.yaml'
customer_id = '8306215642' #google ads customer id
first_threshold = 0.8 # similarity threshold for keyword similarity
second_threshold = 0.8 # similarity threshold for description similarity
third_threshold = 0.35 # similarity threshold for seed keyword and keywords3
conversion_threshold = 1 #  get conversion >= conversion_threshold
allowed_funnels = ['LF','MF'] # available options LF, MF, UF
similarity_model_path = 'Maunish/ecomm-sbert' # this model is already uploaded on huggingface so no need to download

if platform.system()=='Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

os.makedirs(save_path,exist_ok=True)
googleads_client = GoogleAdsClient.load_from_storage(path=path, version="v9")

df = pd.read_csv(df_path)

print("Getting existing keywords")
df_existing = get_existing_keywords(googleads_client,customer_id)
# df_existing = pd.read_csv(save_path+'/df_existing.csv')
keywords_to_remove = df_existing.query("(camp_status == 'ENABLED') & \
                                        (adgroup_status == 'ENABLED') &\
                                        (keyword_status == 'ENABLED')")['keyword_name'].unique().tolist()
df = df[~df["Keywords"].isin(keywords_to_remove)] # if campaign in enabled and keyword clash remove it.
df['keyword_length'] = df['Keywords'].apply(lambda x:len(x))
df = df[df['keyword_length']<=80]

#First pass of filters
print("Applying filters on the data")
df = df[~df["Keywords"].isin(keywords_to_remove)]
df = df[df['similarity'] >= first_threshold]
df = df[df['lf/mf/uf'].isin(allowed_funnels)].reset_index(drop=True)
df = df.drop_duplicates("Keywords")


print("Getting Organic Description")
seed_keywords = df["Keywords2"].unique().tolist()
seed_organic_description = asyncio.get_event_loop().run_until_complete(get_organic_description(email,api_key,seed_keywords))
seed_organic_description = seed_organic_description.rename(columns={'organic_description':'seed_organic_description'})
df = df.merge(seed_organic_description,how='left',left_on='Keywords2',right_on='keyword')

all_keywords = df["Keywords"].unique().tolist()
organic_description = asyncio.get_event_loop().run_until_complete(get_organic_description(email,api_key,all_keywords))
df = df.merge(organic_description,how='left',left_on='Keywords',right_on='keyword')

model = SentenceTransformer(similarity_model_path)

print("Performing similarity using organic description")
for i,row in df.iterrows():
    all_titles = row['seed_organic_description'].split(',')
    all_seed_titles = row['organic_description'].split(',')
    similarity_matrix = get_similarity_matrix(model,all_titles,all_seed_titles)
    df.loc[i,'second_similarity'] = similarity_matrix.max(axis=1).mean()

df = df[df['second_similarity'] >= second_threshold]

if df.shape[0] != 0:
    def remove_word(row):
        keyword1 = re.split("\s|(?<!\d)[,-](?!\d)",row['Keywords'])
        keyword2 = re.split("\s|(?<!\d)[,-](?!\d)",row['Keywords2'])
        keyword = [x for x in keyword1 if x not in keyword2]
        return "" if len(keyword) == 0 else ' '.join(keyword)

    df['Keywords3'] = df.apply(remove_word,axis=1)

    keywords1 = df['Keywords2'].tolist()
    keywords2 = df['Keywords3'].tolist()
    df['third_similarity'] = get_similarity_api(model,keywords1,keywords2)

    df = df[df['third_similarity'] >= third_threshold]

    df_enabled = df_existing.query("(camp_status == 'ENABLED') & \
                                    (adgroup_status == 'ENABLED') &\
                                    (keyword_status == 'ENABLED') & \
                                    (camp_experiment_type != 'EXPERIMENT')")

    df_paused = df_existing.query("camp_status == 'PAUSED'")

    if len(df_enabled) == 0:
        print("No adgroups to expand to")
    else:
        print("Finding similarity with existing keywords")
        new_keywords = df['Keywords'].tolist()
        df_expand = df.copy()
        existing_campaign_id = df_enabled['camp_id'].tolist()
        existing_campaign_status = df_enabled['camp_status'].tolist()
        existing_keywords = df_enabled['keyword_name'].tolist()
        model = SentenceTransformer(similarity_model_path)
        similarity_matrix = get_similarity_matrix(model,existing_keywords,new_keywords)

        similarity_max = similarity_matrix.max(axis=1)
        similarity_index = similarity_matrix.argmax(axis=1)

        df_expand['camp_id'] = [existing_campaign_id[x] for x in similarity_index]
        df_expand = df_expand[(similarity_max>=first_threshold)&(similarity_max!=1)]
        df = df.merge(df_expand.loc[:,['camp_id','Keywords']],how='left',on='Keywords')

    # code for altering campaign names
    paused_campaigns_names = df_paused['camp_name'].unique().tolist()
    df_grouped = df[df['camp_id'].isna()].groupby('Keywords2').groups
    for seed_keyword, i in df_grouped.items():
        if seed_keyword in paused_campaigns_names:
            df.loc[i, 'Keywords2'] = seed_keyword + \
                "_" + str(uuid.uuid4())

df = df.drop_duplicates('Keywords')

if len(df) == 0:
    print("No new keywords to add")

df_existing.to_csv(save_path+'/df_existing.csv',index=False)
df.to_csv(save_path+'/keywords_to_upload.csv',index=False)
