import rumps
import random
import rideindego
import time

prev_num_bikes = {}

USE_ICON = True

@rumps.timer(60*4)
def updateit(sender):
    changeit(None)

def test(_):
	window = rumps.Window('Enter new interval')
	window.add_button('dsdsdas')
	response = window.run()
	for i in prev_num_bikes.keys():
		prev_num_bikes[i] = int(response.text)

def set_alert(sender):
	sender.state = not sender.state
	prev_num_bikes[sender.title.split(':',1)[0].strip()] = -1 if not sender.state else 0

@rumps.clicked('Check now')
def changeit(sender):
	checked = time.strftime("%d %b %Y %H:%M:%S", time.localtime())
	if USE_ICON:
		str = ''
	else:
		str = 'Bikes: '
	
	data = rideindego.get_bike_data()
	app.menu.clear()
	app.menu.update([
		rumps.MenuItem('Check now',callback=changeit),
		rumps.MenuItem('Checked: ' + checked),
		rumps.MenuItem('Quit',callback=rumps.quit_application,key='q'),
		#rumps.MenuItem('Test',callback=test),
		rumps.separator,
		])
	for i in ['33rd & Market','Amtrak 30th Street Station','University City Station',None,'19th & Lombard','23rd & South','17th & Pine']:
		if i:
			state = True if prev_num_bikes.get(i,-1)>-1 else False

			bikes = rideindego.get_data(data,i,'bikesAvailable')
			if state:
				try:
					num_bikes = int(bikes)
					my_data = {'sender': sender}
					if prev_num_bikes[i] == 0 and num_bikes > 0:
						rumps.notification(title='Bike Update', subtitle=i, message='There are %d bikes available now' % num_bikes, sound=True, data=my_data)
					elif num_bikes > 0 and num_bikes<=3:
						rumps.notification(title='Bike Update', subtitle=i, message='There are only %d bikes available' % num_bikes, sound=True, data=my_data)
					prev_num_bikes[i] = num_bikes
				except Exception as e:
					print e
					pass
			item = rumps.MenuItem(i+": "+bikes +'/' + rideindego.get_data(data,i,'docksAvailable') + '',callback=set_alert)
			item.state = state
			app.menu.update(item)
		else:
			app.menu.update([rumps.separator])
			pass
		pass
	str+= rideindego.get_data(data,'33rd & Market','bikesAvailable') +', ' + rideindego.get_data(data,'19th & Lombard','bikesAvailable')

	app.title = str

app = rumps.App('Bike checker', quit_button=rumps.MenuItem('Quit', key='q'), icon='bike.png')
app.menu = [
    ('Check now'),
]
app.run()
