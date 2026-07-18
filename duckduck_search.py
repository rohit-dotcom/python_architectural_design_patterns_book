import duckduckpy

for r in duckduckpy.search('Sausages').relatedTopics:
    if 'Text' in r:
        print(r['FirstURL']+' - '+r['Text'])