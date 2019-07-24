from bs4 import BeautifulSoup   
import requests
import pandas as pd


page_number = 0  
count_row = 0

all_data={}

while True:
    
    url = 'https://www.programmableweb.com/apis/directory?page=' + str(page_number) #it start at 0 so it means page 1
    response = requests.get(url)

    soup=BeautifulSoup(response.text,'html.parser')
    apis = soup.find_all('tr',{'class':['even','odd'] })
    page_number_limit = soup.find('li',{'class':'pager-next'}).find('a').text  #scrape the last page number

    for api in apis:
        try:
            count_row+=1
            api_name=api.find('a').text
            description = api.find('td',{'class':'views-field views-field-search-api-excerpt views-field-field-api-description hidden-xs visible-md visible-sm col-md-8'}).text
            category = (api.find('td',{'class':'views-field views-field-field-article-primary-category'}).find('a').get('href'))[10:]
            submitted = api.find('td',{'class':'views-field views-field-created'}).text

            all_data[count_row]=[api_name,description,category,submitted]
        except:
            print('data not exists') 
        
    
        
    page_number+=1 #next loop, it will go page 2
    if page_number >= int(page_number_limit): break


csv_data = pd.DataFrame.from_dict(all_data, orient = 'index', columns = ['Api name','Description','Category', 'Submitted'])

csv_data.to_csv('api_list.csv')


