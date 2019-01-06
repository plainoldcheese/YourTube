# YourTube

take back control of your youtube consumption. this script uses the [XML rss feed output file from youtube](https://www.youtube.com/subscription_manager) to fetch the last 15 videos from each channel in your subscriptions

## Modules used

this script makes heavy use of the [BeautifulSoup](https://pypi.org/project/BeautifulSoup/) module as well as the [requests](https://pypi.org/project/requests/) module

## todo

[] make script a command line tool that can take input from anywhere and with any file name
[] add ability to choose number of listings per channel
[] add ability to input channel urls (as comma separated list)
[x] add more comments
[x] give script output to a file
[x] improve output file (less convoluted method), ✔ made file more modular by separating it into functions that can write a txt andhtml file 
[x] fetch thumbnails
