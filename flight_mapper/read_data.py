
import pandas
import datetime

class Airport:
    def __init__(self,
                 code=None,
                 name=None,
                 lat=None,
                 lon=None,
                 iata=None,
                 icao=None,
                 elevation=None,
                 city=None,
                 region=None,
                 country=None,
                 continent=None):
        """
        Parameters
        ----------
        code : str
            Must match the code used in the list of flights.
        """
        if code is None:
            raise ValueError('Must supply id code to airport')
        self.code = code
        self.name = name
        self.lat = lat
        self.lon = lon
        self.iata = iata
        self.icao = icao
        self.elevation = elevation
        self.city = city
        self.region = region
        self.country = country
        self.continent = continent

    def __str__(self):
        if self.country == 'United States':
            final_attr = 'region'
        else:
            final_attr = 'country'

        s = f'{self.name}, {self.city}, {getattr(self, final_attr)}'

        if self.icao is not None and self.icao != '':
             s += f' ({self.icao})'

        return s

    def write_airport(self, airport_type='normal'):
        """Generate the HTML representation of an airport.

        Parameters
        ----------
        airport_type : str
            'normal', 'scheduled' (but never reached), or 'diverted'

        Returns
        -------
        str
            HTML code for the airport with abbreviation
        """
        # Start writing full name in the abbreviation tag
        s = f'<abbr title="{str(self)}'

        # add scheduled or diverted if applicable
        if airport_type == 'scheduled':
            s += ' (scheduled)"><span style="color:gray;font-style:italic;">'
        elif airport_type == 'diverted':
            s += ' (diverted)"><span style="color:red;">'
        else:
            s += '">'

        # add the iata code, or the start of the name if not available
        if self.iata is None or self.iata == '':
            s += self.name[:3] + '&#8230;'
        else:
            s += self.iata

        # close the span if it was used
        if airport_type == 'scheduled' or airport_type == 'diverted':
            s += '</span>'

        s += '</abbr>'
        return s


class Flight:
    def __init__(self,
                 airports,
                 route=None,
                 date=None,
                 desig=None,
                 mkt_cxr=None,
                 number=None,
                 type2=None,
                 type3=None,
                 manufacturer=None,
                 registration=None,
                 seat_type=None,
                 cabin=None,
                 seat=None,
                 msn=None,
                 ln=None,
                 first_flight=None,
                 num_engines=None,
                 engines=None,
                 std=None,
                 sta=None,
                 atd=None,
                 ata=None,
                 pics=None,
                 adm_cxr=None,
                 price=None,
                 notes=None,
                 gates=None,
                 runways=None,
                 fare=None,
                 actual_dist=None,
                 fleet=None,
                 plan=None,
                 config=None):

         self.route_string = route
         self.date = date
         self.desig = desig
         self.mkt_cxr = mkt_cxr
         self.adm_cxr = adm_cxr or ''
         self.number = number
         self.type2 = type2
         self.type3 = type3
         self.manufacturer = manufacturer
         self.registration = registration
         self.seat_type = seat_type
         self.cabin = cabin
         self.seat = seat
         self.msn = msn
         self.ln = ln
         self.first_flight = first_flight
         self.num_engines = num_engines
         self.engines = engines
         self.std = std
         self.sta = sta
         self.atd = atd
         self.ata = ata
         self.pics = pics
         if self.pics is not None:
             self.pics = pics.split(';')

         self.parse_route(self.route_string, airports)

         self.date = datetime.datetime(int(self.date[:4]), int(self.date[4:6]), int(self.date[6:]))

    def parse_route(self, route_string, airports):
        """Generate a list of segments and an HTML route display given a route
        with diversions and scheduled stops.

        It saves the following attributes

        self.route : list
            a list of lists for each segment eg [['ABC','DEF'], ['DEF', 'GHI']]
        self.route_str : str
            HTML for the route with arrows, abbreviations, and line breaks

        Parameters
        ----------
        route_string : str
            hyphenated sequence of airport codes, with a preceding 's'
            indicating that the stop was scheduled but never landed and a
            preceding 'd' indicating that the stop was a diversion.
            for example, 'ABC-sDEF-dxyz' indicates a scheduled flight from ABC
            to DEF which never landed at DEF but diverted to xyz.
        airports : dict
            Airports database dict
        """
        all_nodes = route_string.split('-')

        route = [all_nodes[0]]
        display_rstring = airports[all_nodes[0]].write_airport()

        pos = 1
        for node in all_nodes[1:]:
            if node[0] == 's' and len(node) == 4:
                if pos < 2:
                    display_rstring += ' &#8628; ' + airports[node[1:]].write_airport(airport_type='scheduled')
                else:
                    display_rstring += '<br><span style="visibility:hidden;">' + all_nodes[0] + '</span> &#8628; ' +\
                                       airports[node[1:]].write_airport(airport_type='scheduled')
            elif node[0] == 'd' and len(node) == 4:
                if pos < 2:
                    route.append(node[1:])
                    display_rstring += ' &rarr; ' + airports[node[1:]].write_airport(airport_type='diverted')
                else:
                    route.append(node[1:])
                    display_rstring += '<br><span style="visibility:hidden;">' + all_nodes[0] + '</span> &rarr; ' +\
                                       airports[node[1:]].write_airport(airport_type='diverted')
            else:
                if pos < 2:
                    route.append(node)
                    display_rstring += ' &rarr; ' + airports[node].write_airport()
                else:
                    route.append(node)
                    display_rstring += '<br><span style="visibility:hidden;">' + all_nodes[0] + '</span> &rarr; ' +\
                                       airports[node].write_airport()
            pos += 1

        for i in range(len(route)-1):
            route[i] = (airports[route[i]], airports[route[i+1]])

        del(route[-1])

        self.route = route
        self.route_str = display_rstring


def read_airports(filename):
    """Read airport info from csv database.

    Parameters
    ----------
    filename : str
        file path of airports csv data

    Returns
    -------
    dict
        keys = internal codes, values = Aiports
        All airports in the file
    """
    airports = {}
    df = pandas.read_csv(filename)
    df = df.fillna('')
    for i, row in df.iterrows():
        airport = Airport(**row)
        airports[row['code']] = airport

    return airports


def read_flights(filename, airports):
    """Read flight info from text database.

    Parameters
    ----------
    filename : str
        file path of flights list

    Returns
    -------
    list
        list of Flights
    """
    flights = []
    with open(filename, 'r') as f:
        for row in f.readlines():
            row = row.strip()
            data = dict(zip([x.split('=')[0] for x in row.split(',')],
                        [x.split('=')[1] for x in row.split(',')]))
            flight = Flight(airports, **data)
            flights.append(flight)

    return flights
