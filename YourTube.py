import requests
import codecs
from bs4 import BeautifulSoup, SoupStrainer

def get_subs_from_xml(filename):
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
        open('subscription_manager.xml')
        print('-'*80)
    except:
        print('please place the file in the same directory as this script and ensure the \nfilename is "subscription_manager.xml" and run this script again')
        print('-'*80)
        exit()
else:
    exit()

subs = get_subs_from_xml('subscription_manager.xml')

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
    'cache-control': 'private, max-age=0, no-cache'
}
only_entry_tags = SoupStrainer('entry')

with codecs.open('output.html', 'w', 'utf-8') as output_file:
    for sub in subs:
        print('Channel: {}'.format(sub['name']))
        output_file.write('<div><h2 class="title">Channel: {}</h2>'.format(sub['name'])+'\n')
        print('-'*80)
        output_file.write('<p>'+'-'*80+'</p>'+'\n')
        channel_xml = requests.get(sub['link'], headers=headers)
        xml_doc = channel_xml.text
        soup = BeautifulSoup(xml_doc, 'xml', parse_only=only_entry_tags)
        recent_vids = []
        for entry_tags in soup:
            link_item = entry_tags.find('link').get('href')
            title_item =  entry_tags.find('title').text
            recent_vids.append({'title':title_item, 'link':link_item})

        for vid in recent_vids:
            print('Title: {}'.format(vid['title'])+'\t'+'link: {}'.format(vid['link']))
            output_file.write('<p><a class="link" href="{}">'.format(vid['link'])+'{}'.format(vid['title'])+'</a></p>')
        print('-'*80)
        output_file.write('<p>'+'-'*80+'</p></div>'+'\n')

print('Completed!')
    