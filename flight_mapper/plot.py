import collections
import matplotlib.pyplot as plt
import cartopy.feature
import cartopy.crs as ccrs
from cartopy.feature.nightshade import Nightshade
import cartopy.feature as cfeature


def plot_map(flights,
             airports,
             europe=False,
             america=False):

    if europe:
        labels = True
        states = False
        projection = ccrs.Mercator(max_latitude=71.5, min_latitude=35.5,)
        projection._threshold = projection._threshold / 100.0

        fig = plt.figure(figsize=(10.5, 10.5))
        ax = fig.add_subplot(1, 1, 1, projection=projection)
        # ax.set_global()
        ax.set_extent((-24, 30, 35.5, 71.5), crs=ccrs.PlateCarree())
        bounds = (-24, 30, 35.5, 71.5)

    elif america:
        labels = True
        states = True
        projection = ccrs.Mercator(max_latitude=62, min_latitude=-65)
        projection._threshold = projection._threshold / 100.0

        fig = plt.figure(figsize=(14, 14))
        ax = fig.add_subplot(1, 1, 1, projection=projection)
        # ax.set_global()
        ax.set_extent((-160, -58, 16.5, 62), crs=ccrs.PlateCarree())
        bounds = (-160, -58, 16.5, 62)

    else:
        labels = False
        states = False
        projection = ccrs.Mercator(max_latitude=80, min_latitude=-65)
        projection._threshold = projection._threshold / 100.0

        fig = plt.figure(figsize=(15, 15))
        ax = fig.add_subplot(1, 1, 1, projection=projection)
        ax.set_global()
        bounds = (-180, 180, -90, 90)


    ax.add_feature(cartopy.feature.LAND, color='moccasin')
    ax.add_feature(cartopy.feature.OCEAN, color='cornflowerblue', alpha=0.6)
    ax.add_feature(cartopy.feature.LAKES, color='cornflowerblue', alpha=0.6)
    ax.add_feature(cartopy.feature.COASTLINE,linewidth=0.3)
    ax.add_feature(cartopy.feature.BORDERS, linewidth=0.3)
    if states:
        usa_states = cfeature.NaturalEarthFeature(
            category='cultural',
            name='admin_1_states_provinces_lines',
            scale='110m',
            edgecolor='k',
            facecolor='none')
        ax.add_feature(usa_states, linewidth=0.3)

    airport_counts = collections.Counter()
    for flight in flights:
        for leg in flight.route:
            airport_counts[leg[0]] += 1
            airport_counts[leg[1]] += 1
            start = (leg[0].lat, leg[0].lon)
            end = (leg[1].lat, leg[1].lon)
            ax.plot((start[1], end[1]),
                    (start[0], end[0]),
                    color='k',
                    lw=1,
                    zorder=100,
                    transform=ccrs.Geodetic())

    texts = []
    for airport in airports.values():
        ax.scatter(
            airport.lon, airport.lat,
            color='k', s=20, zorder=101, transform=ccrs.PlateCarree())
        ax.scatter(
            airport.lon, airport.lat,
            color='white', s=3.25, zorder=102, transform=ccrs.PlateCarree())

        if labels:
            if bounds[0] < airport.lon < bounds[1] and bounds[2] < airport.lat < bounds[3]:
                t = ax.text(airport.lon, airport.lat, airport.iata, size=6.75,
                    zorder=103 + airport_counts[airport],
                    transform=ccrs.PlateCarree(), ha='center', va='center',
                    bbox={'facecolor': 'white', 'alpha': 1.0, 'edgecolor': 'k',
                          'boxstyle': 'round'})

    return fig
