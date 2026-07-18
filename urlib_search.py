import json
from urllib.request import urlopen
from urllib.parse import urlencode

params=dict(q='Sausages',format='json')
encoded=urlencode(params)
handle=urlopen("http://api.duckduckgo.com/"+'?'+encoded)
raw_text=handle.read().decode('utf8')
parsed=json.loads(raw_text)
results=parsed['RelatedTopics']

for r in results:
    if 'Text' in r:
        print(r['FirstURL']+' - '+r['Text'])


