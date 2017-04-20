from selenium import webdriver  # Class for emulating web actions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import json
import sys
from Weather_Exceptions import * # Class for exceptions

import urllib2

from BeautifulSoup import BeautifulSoup # Class for scraping web pages


'''
This function is used to generate the appropriate name of the temperature record,
given the row number and column names

'''
def get_key_name(row,column) :

	if row==0 and 'Actual' in column :
		return 'Actual Mean Temperature'

	if row==0 and 'Average' in column :
	    return 'Average Mean Temperature'

	if row==0 and 'Record' in column :
	    return 'Record Mean Temperature'

	if row==1 and 'Actual' in column :
	    return 'Actual Max Temperature'

	if row==1 and 'Average' in column :
	    return 'Average Max Temperature'

	if row==1 and 'Record' in column :
	    return 'Record Max Temperature'

	if row==2 and 'Actual' in column :
	    return 'Actual Min Temperature'
	                	
	if row==2 and 'Average' in column :
	    return 'Average Min Temperature'

	if row==2 and 'Record' in column :
	    return 'Record Min Temperature'



'''
This function is used to validate the input location and date.
If there are any validation errors,it will raise an exception.
If there are no errors,it returns the space trimmed input

'''

def validate_input(location,date) :

 location=location.strip()
 date=date.strip()

 if ',' not in location : # If the city and state are not separated by a comma
	raise LocationFormatException('Please enter the location in the following format [city],[State]')
	sys.exit(1)

 if '-' not in date :	# If the date parts are not separated by a hyphen
	raise DateFormatException('Please enter the date in the following format mm-dd-yyyy')
	sys.exit(1)
 

 dates=map(int,date.split('-'))

 if len(dates)!=3 : # Invalid number of date parts
	raise DateFormatException('Please enter the date in the following format mm-dd-yyyy')
	sys.exit(1)



 month,day,year=dates[0],dates[1],dates[2]

 # Invalid date values
 if (month<0 or month>12) or (day<0 or day>31) or (year<0)  or (year-2017)>0 :
	raise DateFormatException('Please enter the date in the following format mm-dd-yyyy')
	sys.exit(1)
 
 return location,[month,day,year] 	


'''
This function is responsible
for querying the input data and 
starting the selenium driver to 
submit the form.After the response
page is loaded,the BeautifulSoup object
parses the web page and extracts the
temperature variables

'''
def fetch_weather_data(location,date) :

 location,date=validate_input(location,date)

 print 'Accepted the location and the date ...'
 print 'Starting the firefox selenium driver ...'

 
 try :

  # Initializing the firefox web driver
  driver = webdriver.Firefox()
  driver.implicitly_wait(30)
  driver.maximize_window()

 except : 
    raise SeleniumDriverException("Error starting the selenium driver") 

 month,day,year=date[0],date[1],date[2]

 print 'Selenium driver started successfully ...'



 base_url="https://www.wunderground.com/history"

 # Connecting to the url
 driver.get(base_url)

 # Selecting the date drop down element
 select_month=Select(driver.find_element_by_name('month'))
 select_month.select_by_index(month-1)

 select_day=Select(driver.find_element_by_name('day'))
 select_day.select_by_index(int(day))

 select_year=Select(driver.find_element_by_name('year'))
 select_year.select_by_index(2017-int(year))

 field=driver.find_element_by_id('histSearch')
 
 # Adding the input into the text field
 field.send_keys(location)

 
 # Submitting the form
 field.submit()

 # Fetching the current url
 result_url=driver.current_url

 # Closing the Selenium driver
 driver.quit()


 # If the page does not submit
 if result_url==base_url :
	raise LocationFormatException("Invalid location")
 
 # Error page
 if result_url.endswith('error=NOTFOUND') or 'error' in result_url:
	raise LocationFormatException('Invalid location')
	sys.exit(1)

 
 # Making a HTTP connection with the response page
 response=urllib2.urlopen(result_url)
 html=response.read()
 # Creating the beautiful soup object with the response html
 soup=BeautifulSoup(html)

 # Finding the temperature table 
 table=soup.find({"table" : {"id" : "historyTable"}})
 r=table.findAll("tr") # Extracting the rows
 headers=table.findAll('th') # Extracting the available headers
 all_columns=['Actual','Average','Record']  # All the headers


 columns=[]

 
 # Finding all columns which are available
 for header in headers :
    if header.text in all_columns : 
      columns.append(header.text)

    elif  'Average' in header.text : 
      columns.append('Average') 

    elif 'Actual' in  header.text :
      columns.append('Actual')

    elif 'Record' in header.text :
      columns.append('Record')

 
 # Extracting the min,max and mean temperature rows
 
 temperature_rows=r[2:5]



 index=0

 keys=[2,5,8]

 i,j=0,0

 # dictionary with its corresponding indices
 d=dict()

 while i<len(columns) and j<len(keys) :
	d[keys[j]]=columns[i]
	i+=1
	j+=1



 # The final dictionary which will be converted to json
 results=dict()

 print 'Fetching the data ...'

 for row in temperature_rows :
	l=row.findAll({'span' : {'class' : 'wx-value'}}) # Extracting the value field


	for tag_index in range(0,len(l)) :

		tag=l[tag_index]

		if ('class','wx-value') in tag.attrs : # Extracting the corresponding value field
			results[(d[tag_index],index)]=tag.text

	index+=1		



 rows=[0,1,2]
 columns=['Actual','Average','Record']
 temperature_values=dict()

 for row in rows :
	for column in columns :
		key_name=get_key_name(row,column)
		if (column,row) in results :
			temperature_values[key_name]=results[(column,row)]
		else :
		    temperature_values[key_name]='N/A'	# Records which are available

 data=dict()
 del temperature_values['Record Mean Temperature']  # deleting the invalid field
 data['Temperature']=temperature_values

 return json.dumps(data)  # converting the dictionary to json






if __name__ == "__main__":

	location=raw_input('Please enter the location in the format [city],[state] (without the square brackets) : ')
	date=raw_input('Please enter the date in the format mm-dd-yyyy : ')
	print 
	print fetch_weather_data(location,date)












