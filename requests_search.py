import requests
import json
from urllib.parse import urlencode

url="http://duckduckgo.com/"

params=dict(q='sausages', format='json')

response=requests.get(url,params).json()

results=response['RelatedTopics']


for r in results:
    if 'Text' in r:
        print(r['FirstURL']+' - '+r['Text'])

