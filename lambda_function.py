import http.client
from bs4 import BeautifulSoup
import tweepy
from configs import *

def tweet(data):
    try:
        client = tweepy.Client(
            consumer_key=api_key, consumer_secret=api_key_secret,
            access_token=access_key, access_token_secret=access_secret
        )
        response=client.create_tweet(text=data)
    except Exception as e:
        print("Failed to tweet the data with exception %s" %(str(e)))
        return -1
    return response

def get_data():
    try: 
        conn = http.client.HTTPSConnection("olympics.com")
        boundary = ''
        payload=''
        headers = {
            'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
        }
        conn.request("GET", "/en/paris-2024/medals",payload, headers)
        res = conn.getresponse()
        data = res.read()

        soup=BeautifulSoup(data,'html.parser')
        rows = soup.find_all('div', {'data-testid': 'noc-row'})
        data = []
        for index, row in enumerate(rows):
            country_info = row.find('div', {'class': 'emotion-srm-157if6k elhe7kv2'})
            country_code = country_info.find_all('span')[1].text
            medals = row.find_all('span', {'class': 'e1oix8v91 emotion-srm-81g9w1'})
            gold = medals[0].text
            silver = medals[1].text
            bronze = medals[2].text
            data.append({
                'Country': country_code,
                'Gold': gold,
                'Silver': silver,
                'Bronze': bronze
            })
            if len(data)>=5:
                break
    except Exception as e:
        print("failed to get the data with exception %s" %(str(e)))
        return {}
    return data

def format_data(data):
    table_header = f"| {'NOC':<5} | {'G':<2} | {'S':<2} | {'B'} |\n"
    table_sep = "-" *19 + "\n"
    table_rows = [f"| {item['Country']:<5} | {item['Gold']:<2} | {item['Silver']:<2} | {item['Bronze']} |" for item in data]
    table = table_sep + table_header + table_sep + "\n".join(table_rows) +"\n" + table_sep
    return table

def main():
    olympics_data=get_data()
    if olympics_data:
        formatted_data=format_data(olympics_data)
        send_tweet=tweet(formatted_data)
        
    else:
        print("No data returned by HTTP!")
    

if __name__ == "__main__":
    main()
