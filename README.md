# web_scraper_admiral_markets

This script is used to scrap admiral markets website and export the data to csv files.  
  
The script is supposed to be excuted every few days and the new data is added to the same csv files.

The script collects the data for multiple currency pair.  
  
The login credintials (email and password) are saved in a config.py file.
  
The code requires a one time acess code that is sent to the email each run.   

Data required is MACD and the data.  
  
data required is dynamic, so the script captures the network traffic to collect the data.    
  
selenium module is used to intiante a web driver and then selenium-wire is used to capture the required data from the network traffic.  
  
  

