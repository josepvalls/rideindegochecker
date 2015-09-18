import rumps
import random
import rideindego
import time

@rumps.timer(60*4)
def updateit(sender):
    changeit(None)

@rumps.clicked('Check now')
def changeit(_):
	checked = time.strftime("%d %b %Y %H:%M:%S", time.localtime())
	str = 'Bikes: '
	data = rideindego.get_bike_data()
	app.menu.clear()
	app.menu.update([
		rumps.MenuItem('Check now',callback=changeit),
		rumps.MenuItem("Checked: " + checked),
		rumps.MenuItem('Quit',callback=rumps.quit_application),
		rumps.separator,
		])
	for i in ['33rd & Market','Amtrak 30th Street Station','University City Station',None,'19th & Lombard','23rd & South','17th & Pine']:
		if i:
			app.menu.update(rumps.MenuItem(i+": "+rideindego.get_data(data,i,'bikesAvailable') +'/' + rideindego.get_data(data,i,'docksAvailable') + ''))
		else:
			app.menu.update([rumps.separator])
			pass
		pass
	str+= rideindego.get_data(data,'33rd & Market','bikesAvailable') +', ' + rideindego.get_data(data,'19th & Lombard','bikesAvailable')

	app.title = str

app = rumps.App('Bike checker', quit_button=rumps.MenuItem('Quit', key='q'))
app.menu = [
    ('Check now'),
]
app.run()
