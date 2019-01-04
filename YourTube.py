import requests
import codecs
from bs4 import BeautifulSoup, SoupStrainer

def get_subs(filename):
    """
    returns a list of xml urls of the channels from the 'subscription_manager' file
    """
    only_outline_tags = SoupStrainer('outline')
    subscriptions = []
    with codecs.open(filename, 'r', 'utf-8') as f:
        soup=BeautifulSoup(f, 'xml', parse_only=only_outline_tags)
        for outline_tag in soup.find_all('outline'):
            link = outline_tag.get('xmlUrl')
            name = outline_tag.get('text')
            subscriptions.append({'name':name, 'link':link})
        subscriptions.remove({'name':'YouTube Subscriptions', 'link':None})
    return subscriptions


sub_manager_link = 'https://www.youtube.com/subscription_manager'

print('-'*80)
print('please navigate to {}, scroll to the\nbottom and click on the "export subscriptions" button  in the "Export to RSS \nreaders" section and place the file in same directory as this script.'.format(sub_manager_link))
print('-'*80)
print('type y/n to continue or cancel')
print('-'*80)
y_or_n = input()

if y_or_n == 'y':
    try:
        open('subscription_manager')
        print('-'*80)
    except:
        print('please place the file in the same directory as this script and ensure the \nfilename is "subscription_manager" with no extension and run this script again')
        print('-'*80)
        exit()
else:
    exit()

subs = get_subs('subscription_manager')

only_entry_tags = SoupStrainer('entry')
for sub in subs:
    print('Channel: {}'.format(sub['name']))
    print('-'*80)
    channel_xml = requests.get(sub['link'])
    xml_doc = channel_xml.text
    soup = BeautifulSoup(xml_doc, 'xml', parse_only=only_entry_tags)
    recent_vids = []
    for entry_tags in soup:
        link_item = entry_tags.find('link').get('href')
        title_item =  entry_tags.find('title').text
        recent_vids.append({'title':title_item, 'link':link_item})
    recent_vids = recent_vids[2:]
    for vid in recent_vids:
        print('Title: {}'.format(vid['title'])+'\t'+'link: {}'.format(vid['link']))
    print('-'*80)


    