import urllib,urllib2
import json
import time

def get_bike_data():
	try:
		url = "https://api.phila.gov/bike-share-stations/v1"
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		response = opener.open(url)
		data = json.loads(response.read())
		response.close()
		return data
	except:
		return []
def get_data(data,station,property):
	try:
		return str([i['properties'][property] for i in data['features'] if i['properties']['name']==station][0])
	except:
		return '?'
def cli():
	while True:
		print time.ctime(time.time()).ljust(40)+"Bikes Docks"
		data = get_bike_data()
		for i in ['33rd & Market','Amtrak 30th Street Station','University City Station','19th & Lombard','23rd & South','17th & Pine']:
			print i.ljust(40)+get_data(data,i,'bikesAvailable').rjust(6) + get_data(data,i,'docksAvailable').rjust(6)
		time.sleep(60*4)

if __name__ == "__main__":
 cli()
