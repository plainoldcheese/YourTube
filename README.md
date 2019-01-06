# YourTube

take back control of your youtube consumption. this script uses the [XML rss feed output file from youtube](https://www.youtube.com/subscription_manager) to fetch the last 15 videos from each channel in your subscriptions.

## examples of output

1. [txt](docs/output/output.txt)
2. [markdown](docs/output/output.md)
3. [html](docs/output/output.html)

## Modules used

this script makes use of the [BeautifulSoup](https://pypi.org/project/BeautifulSoup/) module for parsing as well as the [requests](https://pypi.org/project/requests/) module for fetching the xml files.

## TO DO

the following is yet to be implemented.

- make script a command line tool that can take input from anywhere and with any file name
  - example `yourtube path/to/xml/filename.xml -o html`
  - `-o` md/html/txt output
  - `-l` write list of links to stdout for use with piping into other scripts
  - `-i` feed in custom input (channel urls comma separated). example `yourtube -i channelurl, channelurl2 -o md`
  - `-n` number of videos per channel to fetch
- add ability to choose number of listings per channel
- add ability to input channel urls (as comma separated list)
