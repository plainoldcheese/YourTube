import itertools
import webbrowser
import requests
import codecs
import os
from bs4 import BeautifulSoup, SoupStrainer

#======================================output to file functions=================================#

def write_to_html(subscription, videos):
    '''
    takes in dictionary of subscription and list of dictionaries of recent videos and writes outptu to an html document
    '''
    with codecs.open('output/temp.html', 'a+', 'utf-8') as output_file:
        # start html doc
        output_file.write('<div class="channel-container"><h2 class="title">Channel: {}</h2>'.format(subscription['name'])+'\n')
        output_file.write('<p>'+'-'*80+'</p>'+'\n') # divider

        for vid in videos:
            output_file.write(
                '<div class="video">'+'\n'+
                    '<img class="thumbnail" src="{}"></img>'.format(vid['thumb'])+'\n'+
                    '<a class="link" href="{}">'.format(vid['link'])+'{}'.format(vid['title'])+'</a>'+'\n'+
                '</div>'
                )
        output_file.write('<p>'+'-'*80+'</p></div>'+'\n') # divider
        
        output_file.write('''</body>\n</html>''') # end tags
        

def prepend_html():
    '''
    prepend html_template to beginning of file
    '''
    html_template = ''' <!DOCTYPE html>
                        <html>
                        <head>
                            <meta charset="utf-8" />
                            <meta http-equiv="X-UA-Compatible" content="IE=edge">
                            <title>YourTube</title>
                            <meta name="viewport" content="width=device-width, initial-scale=1">
                            <link rel="stylesheet" type="text/css" media="screen" href="main.css" />
                            <style>
                            @media only screen and (max-width: 600px) {
                                div {
                                    width: 40ch !important;
                                }
                            }

                            body {
                                background: white;
                                color: black;
                                font-family: Consolas, monospace;
                                text-decoration: none;
                                text-align: left;
                                align-content: center;
                            }

                            div {
                                width: 80ch;
                                margin-left: auto;
                                margin-right: auto;
                                overflow-wrap: break-word;
                                word-wrap: break-word;
                            }

                            a:visited, a:hover, a:active, a:any-link {
                                text-decoration: none;
                                color: black;
                            }

                            a:hover {
                                color: gray;
                            }

                            img {
                                height: 100px;
                                width: auto;
                                order: 0;
                                margin: 0px 10px 0px 0px;
                            }

                            .link {
                                order: 1;
                            }

                            .video {
                                display: flex;
                                position: relative;
                                flex-direction: row;
                                margin: 20px 0px 20px 0px;
                            }

                            .video a {
                                position: relative;
                                vertical-align: middle;
                            }
                            </style>
                        </head>
                        <body>'''
    with codecs.open('output/temp.html', 'r', 'utf-8') as f:
        with codecs.open('output/output.html','w', 'utf-8') as f2: 
            f2.write(html_template)
            f2.write(f.read())
    os.remove('output/temp.html')

def write_to_txt(subscription ,videos):
    '''
    takes in disctionary of subscription and list of dictionaries of recent videos and writes outptu to an txt file
    '''
    
    with codecs.open('output/output.txt', 'a+', 'utf-8') as output_file:
        output_file.write('Channel: {}'.format(subscription['name'])+'\n')
        output_file.write('-'*80+'\n') # divider
        for vid in videos:
            output_file.write('Title: {}'.format(vid['title'])+'\t'+'link: {}'.format(vid['link'])+'\n')
        output_file.write('-'*80+'\n') # divider


def write_to_md(subscription, videos):
    '''
    takes in disctionary of subscription and list of dictionaries of recent videos and writes outptu to a markdown file
    '''
    
    with codecs.open('output/output.md', 'a+', 'utf-8') as output_file:
        output_file.write('\n'+'## Channel: {}'.format(subscription['name'])+'\n'*2)
        count = 0
        for vid in videos:
            count += 1
            output_file.write('{}. [{}]({})'.format(count, vid['title'], vid['link'])+'\n')


#=======================================scraping functions=======================================#
def get_subs_from_xml(filename):
    '''
    returns a list of xml urls of the channels from the 'subscription_manager' file
    '''
    only_outline_tags = SoupStrainer('outline')
    subscriptions = []
    with codecs.open(filename, 'r', 'utf-8') as f:
        soup=BeautifulSoup(f, 'xml', parse_only=only_outline_tags)
        for outline_tag in  itertools.islice(soup.find_all('outline'),1,None):
            link = outline_tag.get('xmlUrl')
            name = outline_tag.get('text')
            subscriptions.append({'name':name, 'link':link})
        # subscriptions.remove({'name':'YouTube Subscriptions', 'link':None})
    return subscriptions


def get_videos_from_sub(subscription, num_vids): 
    '''
    takes a dictionary with info about subscriptions and returns list of dictionaries with videos, titles and thumbnails for each channel
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36',
        'cache-control': 'private, max-age=0, no-cache'
    }
    only_entry_tags = SoupStrainer('entry')

    channel_xml = requests.get(subscription['link'], headers=headers)
    xml_doc = channel_xml.text
    soup = BeautifulSoup(xml_doc, 'xml', parse_only=only_entry_tags)

    recent_vids = []
    stop_count = 0
    for entry_tags in soup:
        if stop_count == num_vids:
            break
        else:
            stop_count += 1
        link_item = entry_tags.find('link').get('href')
        title_item =  entry_tags.find('title').text
        thumbnail_item = entry_tags.find('media:thumbnail').get('url')
        recent_vids.append(
            {
                'title':title_item, 
                'link':link_item, 
                'thumb':thumbnail_item
            }
        )
    return recent_vids

#==============================================main==============================================#
if __name__ == "__main__":

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

    
    # make output directory if none exists
    if not os.path.isdir('output'):
        os.mkdir('output')
    # delete existing output files if they exist
    if os.path.isdir('output/output.txt'):
        os.remove('output/output.txt')
    if os.path.isdir('output/output.html'):
        os.remove('output/output.html')
    if os.path.isdir('output/output.md'):
        os.remove('output/output.md')
    
    subs = get_subs_from_xml('subscription_manager.xml')
    videos = []

    num_vids_per_channel = int(input('please enter teh number of recent videos per channel'))
    NUMBERS = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    
    if num_vids_per_channel > 15 or num_vids_per_channel not in NUMBERS or num_vids_per_channel == 0:
        num_vids_per_channel = 15

    for sub in subs:
        print('fetching videos for {}...'.format(sub['name']))
        videos = get_videos_from_sub(sub, num_vids_per_channel)
        write_to_html(sub, videos)
        write_to_txt(sub, videos)
        write_to_md(sub, videos)
    prepend_html()
    
    print('-'*80)
    print('Completed!')
    # open output file in browser
    webbrowser.open('output/output.html')    
    
