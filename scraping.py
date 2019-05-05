import urllib.request as Ulib
import requests
import json
import csv
import time

def req_data_from_url(url):
    response = requests.get(url)
    success = False
    while success is False :
        try:
            if response.status_code == 200:
                success = True

        except Exception as e :
            print(e)
            time.sleep(3)
        
    return response.text

def get_data(page,access_token):

    website = "https://graph.facebook.com/v3.3/"

    location = "%s/posts/" % page

    fields = "?fields=message,type,name,id," + \
            "comments.limit(0).summary(true),shares"

    authentication = "&limit=100&access_token=%s" % (access_token)

    request_url = website + location + fields + authentication
    data = json.loads(req_data_from_url(request_url))

    return data

def process_post(post, access_token):

    post_id = post['id']
    
    post_message = 'No_message' if 'message' not in post else \
            post['message']

    post_type = post['type']

    num_comments = 0 if 'comments' not in post else \
            post['comments']['summary']['total_count']

    num_shares = 0 if 'shares' not in post else post['shares']['count']

    return(post_id,post_message,post_type,num_comments,num_shares)


def scrape_data(page_id, access_token):
    
    with open("facebook_data.csv",'w') as file :
        w = csv.writer(file)

        w.writerow(["post_id", "post_message", "post_type","num_comments", "num_shares"])
        
        has_next_page = True
        num_processed = 0

        print("Scraping %s Facebook Page ... \n" % page_id)

        posts = get_data(page_id, access_token)

        while has_next_page:

            if num_processed == 200:
                break
                
            for post in posts['data']:

                w.writerow(process_post(post, access_token))
                    
                num_processed += 1

            if 'paging' in posts.keys():
                posts = json.loads(req_data_from_url(
                                        posts['paging']['next']))
            
            else:
                has_next_page = False


        print ("Completed!")


page_id = input("Please Paste Public Page Name: ")
access_token = input("Please Paste Your Access Token: ")

if __name__ == '__main__':
    scrape_data(page_id,access_token)