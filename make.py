import datetime
import matplotlib.pyplot as plt
import cartopy.feature
import cartopy.crs as ccrs
from cartopy.feature.nightshade import Nightshade
import cartopy.feature as cfeature



import flight_mapper as fm


airports = fm.read_airports('data/airports.csv')
flights = fm.read_flights('flights.txt', airports)


result = fm.make_html(flights, airports)
f2 = open('public/index.html', mode='w')
f2.write(result)
f2.close()


fig = fm.plot_map(flights, airports)
plt.savefig('public/earth.png', bbox_inches='tight')

fig = fm.plot_map(flights, airports, europe=True)
plt.savefig('public/europe.png', bbox_inches='tight')

fig = fm.plot_map(flights, airports, america=True)
plt.savefig('public/america.png', bbox_inches='tight')
