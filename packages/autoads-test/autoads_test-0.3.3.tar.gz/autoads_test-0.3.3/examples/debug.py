import asyncio
import aiohttp
from time import time
import pandas as pd
from autoads.keywords import get_results
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from autoads.client import AsyncRestClient

df_path = 'data/keywords_to_upload.csv' # specify keywords to uplod csv here
save_path = 'data'
email = 'weilbacherindustries@gmail.com' # email in data for seo
api_key = '05f014a493983975' # api key for data for seo
path = '/home/maunish/Upwork Projects/Google-Ads-Project/examples/google-ads.yaml'
customer_id = '6554081276'
seed_keywords = ["crypto 401k", "real estate 401k", "esg 401k", "business 401k", "business crypto 401k", "business esg 401k"] 

async def make_live_request(keyword, email, api_key, priority=2, depth=2, max_crawl_pages=2):

    async with aiohttp.ClientSession() as session:
        client = AsyncRestClient(email, api_key,session)
        post_data = dict()
        post_data[len(post_data)] = dict(
            language_name="English",
            location_name="United States",
            keyword=keyword,
            priority=priority,
            depth=depth,
            max_crawl_pages=max_crawl_pages,
            tag=f"{keyword} google",
        )
        response = await client.post(
            "/v3/serp/google/organic/live/advanced", post_data)
        if response["status_code"] == 20000:
            print('please wait for sometime.. till we gather data')
            return response
        else:
            print("error. Code: %d Message: %s" %
                (response["status_code"], response["status_message"]))


start_time = time()
async def get_organic_description(keywords):

    tasks = [
        'organic',
    ]
    task_params = {
        'organic': ['description'],
    }

    data = {
        "organic_description":list(),
        "keywords":keywords,
    }

    responses = list()
    for keyword in keywords:
        print(keyword)
        responses.append(asyncio.create_task(make_live_request(keyword,email,api_key,depth=5)))
    
    response_data = await asyncio.gather(*responses)

    for response in response_data:
        if response['tasks'][0]['result']:
            results = get_results(response,tasks,task_params)
            organic_description = str([x.replace(",","") for x in results['organic_description']])
            organic_description = organic_description.replace("[","").replace("]","")
            data["organic_description"].append(organic_description)
        else:
            print("Failed to get organic description")
            data["organic_description"].append(keyword)
    
    return data

data = asyncio.run(get_organic_description(seed_keywords))

print(data)
print(time()-start_time)
