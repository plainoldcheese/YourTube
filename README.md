# YourTube

take back control of your youtube consumption. this script uses the [XML rss feed output file from youtube](https://www.youtube.com/subscription_manager) to fetch the last n amount of videos from each channel in your subscriptions.
This does not utilize the Youtube API and thus will not send data back to Youtube

## Usage

1. Download your list of subscriptions from [here](https://www.youtube.com/feed/subscriptions)
2. Download this script 
3. cd into the directory and run in the terminal ``python3 Yourtube.py``
4. follow the instruction given
5. you can view the output files in the ``output`` directory


## examples of output

1. [txt](docs/output.txt)
2. [markdown](docs/output.md)
3. [html](docs/output.html)

## Modules used

this script makes use of the [BeautifulSoup](https://pypi.org/project/BeautifulSoup/) module for parsing as well as the [requests](https://pypi.org/project/requests/) module for fetching the xml files.

## TO DO

the following is yet to be implemented.

- make this script into a command line tool that can take input from anywhere and with any file name
  - example `yourtube path/to/xml/filename.xml -o html`
  - `-o` md/html/txt output
  - `-l` write list of links to stdout for use with piping into other programs such as [youtube-dl](https://github.com/ytdl-org/youtube-dl)
  - `-i` feed in custom input (channel urls comma separated). example `yourtube -i channelurl_a, channelurl_b -o md`
  - `-n` number of videos per channel to fetch
- add ability to choose number of listings per channel ✅
- add ability to input channel urls (as comma separated list)
- add youtube-dl support to download list of videos
