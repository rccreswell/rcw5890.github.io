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
f2 = open('index.html', mode='w')
f2.write(result)
f2.close()
