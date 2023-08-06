Quickstart
==================================================

Description
--------------------------------------------------
The addresshunt package gives you painless access to the addresshunt API's.
It performs requests against our API's for

- `Autocomplete address`_
- `Matching address`_
- `Address validation`_
- `Split address`_
- `Forward geocoding`_
- `Reverse geocoding`_
- `Zone management`_

For further details, please visit:

- homepage_


.. _homepage: https://addresshunt.com.au
.. _`Autocomplete address`: https://addresshunt.com.au/api/docs/#/Address%20APIs/get_api_v1_0_address_autocomplete
.. _`Matching address`: https://addresshunt.com.au/api/docs/#/Address%20APIs/get_api_v1_0_address_match
.. _`Address validation`: https://addresshunt.com.au/api/docs/#/Address%20APIs/get_api_v1_0_address_validate
.. _`Split address`: https://addresshunt.com.au/api/docs/#/Address%20APIs/get_api_v1_0_address_split
.. _`Forward geocoding`: https://addresshunt.com.au/api/docs/#/Address%20APIs/get_api_v1_0_address_forward_geocode
.. _`Reverse geocoding`: https://addresshunt.com.au/api/docs/#/Address%20APIs/get_api_v1_0_address_reverse_geocode
.. _`Zone management`: https://addresshunt.com.au/api/docs/#/Zone%20APIs/get_api_v1_0_zone_check


Requirements
-----------------------------
addresshunt-py is tested against Python 3.6, 3.7, 3.8 and 3.9, and PyPy3.6 and PyPy3.7.

Installation
------------------------------
To install from PyPI, simply use pip::

	pip install addresshunt


Usage
---------------------------------

For an interactive Jupyter notebook have a look on `mybinder.org <https://mybinder.org/v2/gh/GIScience/openrouteservice-py/master?filepath=examples%2Fbasic_example.ipynb>`_.

Basic example
^^^^^^^^^^^^^^^^^^^^
.. code:: python

	import addresshunt

	coords = ((8.34234,48.23424),(8.34423,48.26424))

	client = addresshunt.Client(key='') # Specify your personal API key
	routes = client.directions(coords)

	print(routes)

For convenience, all request performing module methods are wrapped inside the ``client`` class. This has the
disadvantage, that your IDE can't auto-show all positional and optional arguments for the
different methods. And there are a lot!

The slightly more verbose alternative, preserving your IDE's smart functions, is

.. code:: python

    import addresshunt
    from addresshunt.directions import directions

	coords = ((8.34234,48.23424),(8.34423,48.26424))

	client = addresshunt.Client(key='') # Specify your personal API key
	routes = directions(client, coords) # Now it shows you all arguments for .directions

Optimize route
^^^^^^^^^^^^^^^^^^^^^^^^^^
If you want to optimize the order of multiple waypoints in a simple `Traveling Salesman Problem <https://en.wikipedia.org/wiki/Travelling_salesman_problem>`_,
you can pass a ``optimize_waypoints`` parameter:

.. code:: python

	import addresshunt

	coords = ((8.34234,48.23424),(8.34423,48.26424), (8.34523,48.24424), (8.41423,48.21424))

	client = addresshunt.Client(key='') # Specify your personal API key
	routes = client.directions(coords, profile='cycling-regular', optimize_waypoints=True)

	print(routes)

Decode Polyline
^^^^^^^^^^^^^^^^^^^^^^^^^^
By default, the directions API returns `encoded polylines <https://developers.google.com/maps/documentation/utilities/polylinealgorithm>`_.
To decode to a ``dict``, which is a GeoJSON geometry object, simply do

.. code:: python

    import addresshunt
    from addresshunt import convert

    coords = ((8.34234,48.23424),(8.34423,48.26424))

    client = addresshunt.Client(key='') # Specify your personal API key

    # decode_polyline needs the geometry only
    geometry = client.directions(coords)['routes'][0]['geometry']

    decoded = convert.decode_polyline(geometry)

    print(decoded)

Dry run
^^^^^^^^^^^^^^^^^^^^
Although errors in query creation should be handled quite decently, you can do a dry run to print the request and its parameters:

.. code:: python

    import addresshunt

    coords = ((8.34234,48.23424),(8.34423,48.26424))

    client = addresshunt.Client()
    client.directions(coords, dry_run='true')

Local ORS instance
^^^^^^^^^^^^^^^^^^^^
If you're hosting your own ORS instance, you can alter the ``base_url`` parameter to fit your own:

.. code:: python

    import addresshunt

    coords = ((8.34234,48.23424),(8.34423,48.26424))

    # key can be omitted for local host
    client = addresshunt.Client(base_url='http://localhost/ors')

    # Only works if you didn't change the ORS endpoints manually
    routes = client.directions(coords)

    # If you did change the ORS endpoints for some reason
    # you'll have to pass url and required parameters explicitly:
    routes = client.request(
      url='/new_url',
      post_json={
          'coordinates': coords,
          'profile': 'driving-car',
          'format': 'geojson'
      })

Support
--------

For issues/bugs/enhancement suggestions, please use https://github.com/AddressHunt/addresshunt-py/issues.