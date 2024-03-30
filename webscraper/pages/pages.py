import json
from format_text import trunc
from llamaexport import make

pages = json.load(open('webscraper/pages/pages.json'))['pages']

count = 0

for page in pages:
    count += 1
    title = trunc(page['title'])
    url = page['url']
    print(f'{title}: {url}, {count} / 48')
    make(title, url)
    if page['sub']:
        for sub in page['subs']:
            count += 1
            sub_title = title + '_' + trunc(sub['title'])
            sub_url = sub['url']
            print(f'{sub_title}: {sub_url}, {count} / 48')
            make(sub_title, sub_url)