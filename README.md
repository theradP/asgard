# asgard

clone the repo and run pip install requirements.txt to install all dependencies 

steps to run scraper:-
1 - add the category urls in start_urls variable in ebay_scraper/ebay_scraper/spiders/ebay.py
2 - open the ebay_scarper directory from the terminal 
3 - run "scrapy crawl ebay -o ebay_test.csv"  --- will store all response in the csv file 


For AWS script
1 - update all related info for the servers ( the variable and explanations are in aws_boto.py)
2- run the script in asgard folder directly from terminal "python aws_boto.py"

urls constraint - either search results page or any page with list of products 
