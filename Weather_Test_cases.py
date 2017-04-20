from weather import *

#Test Case 1-Valid City and Date
location = "San Francisco,California"
Date = "05-21-2017"
result = json.loads(fetch_weather_data(location,Date))
if len(result['Temperature'])==8:
	print "Test Case 1 Passed"
else:
	print "Test Case 1 Failed"
	sys.exit(1)

# Test Case 2-Partial Data Average Mean not present
location = "Hyderabad,India"
Date = "05-21-2017"
result = json.loads(fetch_weather_data(location,Date))
if (result['Temperature']['Average Mean Temperature'])=="N/A":
	print "Test Case 2 Passed"
else:
	print "Test Case 2 Failed"
	sys.exit(1)

# Test Case 3-Future Date entered which is not present
location = "San Francisco,California"
Date = "05-21-2018"

try:
	fetch_weather_data(location,Date)
	print "Test Case 3 Failed"
	sys.exit(1)
except DateFormatException, e:
	print "Test Case 3 Passed"


# Test Case 4-Incorrect City entered
location = "San Fraco,California"
Date = "05-21-2017"
try:
	fetch_weather_data(location,Date)
	print "Test Case 4 Failed"
	sys.exit(1)
except LocationFormatException, e:
	print "Test Case 4 Passed"


# Test Case 5-Incorrect Date entered 
location='Altanta,Georgia'
Date="14-21-2005"

try:
	fetch_weather_data(location,Date)
	print "Test Case 5 Failed"
	sys.exit(1)
except DateFormatException, e:
	print "Test Case 5 Passed"


# Test Case 6 - Finding the temperature values for a remote corner of the world

location="Nairobi,Kenya"
Date="10-10-1998"
result=json.loads(fetch_weather_data(location,Date))
if len(result['Temperature'])!=8 :
	print 'Test Case 6 Failed'
	sys.exit(1)
else :
    print 'Test Case 6 Passed'	


print 'All available test cases passed.'