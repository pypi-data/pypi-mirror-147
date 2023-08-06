import pandas as pd
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from autoads.gads import (add_negative_keywords, get_existing_keywords,get_all_ads,create_ad,
                        create_keyword,_handle_googleads_exception,
                        create_adgroup, get_all_shared_sets)


email = 'weilbacherindustries@gmail.com' # email in data for seo
api_key = '05f014a493983975' # api key for data for seo
save_path = 'data' #all the csvs will be stored on this folder
path = 'data/google-ads.yaml'
customer_id = '8306215642' #google ads customer id
start_date='2022-01-01'
end_date='2022-01-02'

googleads_client = GoogleAdsClient.load_from_storage(path=path, version="v9")

df_existing = get_existing_keywords(googleads_client,customer_id)
df_ads_data = get_all_ads(googleads_client,customer_id)
# df_ads_data = pd.read_csv('data/df_ads_data.csv')
df_ads_data = df_ads_data.drop_duplicates(['adgroup_id']).reset_index(drop=True)

campaign_id_ads_data = df_ads_data['campaign_id'].unique().tolist()
ad_group_id_ads_data = df_ads_data['adgroup_id'].unique().tolist()

df_search_term_report = pd.read_csv(save_path+'/df_search_term_report.csv')
df_search_term_report_negative = pd.read_csv(save_path+'/df_search_term_report_negative.csv')


if len(df_search_term_report) != 0:

    ads_to_copy_dict = {
        'headlines_to_copy': list(),
        'descriptions_to_copy': list(),
        'final_url_to_copy': list(),
        'path1_to_copy' : list(),
        'path2_to_copy' : list(),
        'adgroup_id_created' : list(),
        'campaign_to_copy_to': list()
    }

    print("Copying data for creating ads")
    for i,row in df_search_term_report.iterrows():
        ad_group_id = row['adgroup_id']
        campaign_id = row['camp_id']
        if ad_group_id in ad_group_id_ads_data:
            headlines_to_copy = df_ads_data.loc[df_ads_data['adgroup_id']==ad_group_id,'headline_keywords'].tolist()[0]

            existing_keywords = df_existing.loc[df_existing['adgroup_id']==ad_group_id,'keyword_name'].unique().tolist()
            keyword_in_search_term = row['stv_search_term']
            headlines_to_copy = list(set([keyword_in_search_term]+headlines_to_copy))

            descriptions_to_copy = df_ads_data.loc[df_ads_data['adgroup_id']==ad_group_id,'ad_description'].tolist()[0]

            final_url_to_copy = df_ads_data.loc[df_ads_data['adgroup_id']==ad_group_id,'final_url'].tolist()[0][0]

            path1_to_copy = df_ads_data.loc[df_ads_data['adgroup_id']==ad_group_id,'path1'].tolist()[0]
            path2_to_copy = df_ads_data.loc[df_ads_data['adgroup_id']==ad_group_id,'path2'].tolist()[0]

            ads_to_copy_dict['headlines_to_copy'].append(headlines_to_copy)
            ads_to_copy_dict['descriptions_to_copy'].append(descriptions_to_copy)
            ads_to_copy_dict['final_url_to_copy'].append(final_url_to_copy)
            ads_to_copy_dict['path1_to_copy'].append(path1_to_copy)
            ads_to_copy_dict['path2_to_copy'].append(path2_to_copy)
        
        elif campaign_id in campaign_id_ads_data:
            headlines_to_copy = df_ads_data.loc[df_ads_data['campaign_id']==campaign_id,'headline_keywords'].tolist()[0]

            existing_keywords = df_existing.loc[df_existing['campaign_id']==campaign_id,'keyword_name'].unique().tolist()
            keyword_in_search_term = row['stv_search_term']
            headlines_to_copy = list(set([keyword_in_search_term]+headlines_to_copy))

            descriptions_to_copy = df_ads_data.loc[df_ads_data['campaign_id']==campaign_id,'ad_description'].tolist()[0]

            final_url_to_copy = df_ads_data.loc[df_ads_data['campaign_id']==campaign_id,'final_url'].tolist()[0][0]

            path1_to_copy = df_ads_data.loc[df_ads_data['campaign_id']==campaign_id,'path1'].tolist()[0]
            path2_to_copy = df_ads_data.loc[df_ads_data['campaign_id']==campaign_id,'path2'].tolist()[0]

            ads_to_copy_dict['headlines_to_copy'].append(headlines_to_copy)
            ads_to_copy_dict['descriptions_to_copy'].append(descriptions_to_copy)
            ads_to_copy_dict['final_url_to_copy'].append(final_url_to_copy)
            ads_to_copy_dict['path1_to_copy'].append(path1_to_copy)
            ads_to_copy_dict['path2_to_copy'].append(path2_to_copy)

    if len(df_search_term_report) != 0:
        answer = input("Upload the keywords from the report and create ads for it ? (y/n)  ")
        #code for expanding existing campaign
        if answer == 'y' or answer == 'Y':
            print("Adding to existing campaign")
            try:
                for i, row in df_search_term_report.iterrows():
                    keyword = row['Keywords']
                    campaign_id = str(int(row['camp_id']))
                    ad_group = create_adgroup(googleads_client,customer_id,campaign_id, adgroupName=keyword)
                    if ad_group is None:
                        continue
                    ad_group_id = ad_group.split('/')[-1]
                    keyword_id1 = create_keyword(
                        googleads_client,customer_id,
                        ad_group_id, keyword, kw_type='PHRASE')
                    keyword_id1 = keyword_id1.split('~')[-1]
                    keyword_id2 = create_keyword(
                        googleads_client,customer_id,
                        ad_group_id, keyword, kw_type='EXACT')
                    keyword_id2 = keyword_id2.split('~')[-1]
                    ads_to_copy_dict['adgroup_id_created'].append(ad_group_id)
                    ads_to_copy_dict['campaign_to_copy_to'].append(campaign_id)

                print(f"{df_search_term_report.shape[0]} campaigns expanded")
            except GoogleAdsException as ex:
                _handle_googleads_exception(ex)
            
            print("Copying ads to created ad groups")
            df_ads_to_copy = pd.DataFrame(ads_to_copy_dict)
            df_ads_to_copy['path1_to_copy'].fillna("",inplace=True)
            df_ads_to_copy['path2_to_copy'].fillna("",inplace=True)
            df_ads_to_copy.to_csv(save_path+'/df_ads_to_copy.csv',index=False)

            for i,row in df_ads_to_copy.iterrows():
                adgroup_id_created = row['adgroup_id_created']
                headlines_to_copy = row['headlines_to_copy']
                descriptions_to_copy = row['descriptions_to_copy']
                final_url_to_copy = row['final_url_to_copy']
                path1_to_copy = row['path1_to_copy']
                path2_to_copy = row['path2_to_copy']

                headlines_to_copy = [x for x in headlines_to_copy if len(x) <= 30][:15]
                descriptions_to_copy = descriptions_to_copy[:3]

                if len(headlines_to_copy) != 0 and len(descriptions_to_copy) != 0:
                    create_ad(googleads_client,customer_id,adgroup_id_created,
                                final_url_to_copy,headlines_to_copy,descriptions_to_copy,
                                path1_to_copy,path2_to_copy)
                else:
                    print("Missing headlines or descriptions")
    else:
        print("No keywords to add into existing campaigns")
else:
    print("No keywords to add into existing campaigns") 



if len(df_search_term_report_negative) != 0:
    answer = input("Do you want to upload negative keywords? (y/n): ")
    if answer == 'y' or answer == 'Y':
        print("Get Shared Set List")
        df_shared_set = get_all_shared_sets(googleads_client,customer_id)
        for i,row in df_shared_set.iterrows():
            print("No - Id - Name")
            print(f"{i} - {row['shared_set_id']} - {row['shared_set_name']}")
        answer = int(input("Select the number from above list: "))
        shared_set_id = df_shared_set.loc[i].at['shared_set_id']
        negative_keywords = df_search_term_report_negative['stv_search_term'].unique().tolist()
        negative_keywords = [x for x in negative_keywords if len(x) <= 80]
        if len(negative_keywords) != 0:
            resourse_names_list1 = add_negative_keywords(googleads_client,customer_id,shared_set_id,negative_keywords,kw_type='PHRASE')
            resourse_names_list2 = add_negative_keywords(googleads_client,customer_id,shared_set_id,negative_keywords,kw_type='EXACT')

            keyword_ids1 = [x.resource_name.split('~')[-1] for x in resourse_names_list1]
            keyword_ids2 = [x.resource_name.split('~')[-1] for x in resourse_names_list2]
        else:
            print("No keywords to add in negative list")
else:
    print("No keywords to add in negative list")
