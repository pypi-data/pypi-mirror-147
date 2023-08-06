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
- `Timezone`_
- `Zone management (API only)`_

For further details, please visit:

- homepage_

.. _homepage: https://addresshunt.com.au
.. _`Autocomplete address`: https://addresshunt.com.au/api/docs/#/Address%20APIs/get_api_v1_0_address_autocomplete
.. _`Matching address`: https://addresshunt.com.au/api/docs/#/Address%20APIs/get_api_v1_0_address_match
.. _`Address validation`: https://addresshunt.com.au/api/docs/#/Address%20APIs/get_api_v1_0_address_validate
.. _`Split address`: https://addresshunt.com.au/api/docs/#/Address%20APIs/get_api_v1_0_address_split
.. _`Forward geocoding`: https://addresshunt.com.au/api/docs/#/Address%20APIs/get_api_v1_0_address_forward_geocode
.. _`Reverse geocoding`: https://addresshunt.com.au/api/docs/#/Address%20APIs/get_api_v1_0_address_reverse_geocode
.. _`Timezone`: https://addresshunt.com.au/api/docs/#/[object%20Object]/get_api_v1_0_address_timezone
.. _`Zone management (API Only)`: https://addresshunt.com.au/api/docs/#/Zone%20APIs/get_api_v1_0_zone_check


Requirements
-----------------------------
addresshunt-py is tested against Python 3.6, 3.7, 3.8 and 3.9, and PyPy3.6 and PyPy3.7.

Installation
------------------------------
To install from PyPI, simply use pip::

	pip install addresshunt


Usage
---------------------------------

Examples
^^^^^^^^^^^^^^^^^^^^
.. code:: python

    import addresshunt

    autocomplete_address = "11 NICHOLSON STREET"
    match_address = "NICHOLSON STREET"
    forward_geocode_address = "MELBOURNE MUSEUM, 11 NICHOLSON STREET, CARLTON, VIC, 3053"
    reverse_geocode_address_latitude = "-37.803165"
    reverse_geocode_address_longitude = "144.971802"
    split_address = "MELBOURNE MUSEUM, 11 NICHOLSON STREET, CARLTON, VIC, 3053"
    timezone_address = "MELBOURNE MUSEUM, 11 NICHOLSON STREET, CARLTON, VIC, 3053"
    validate_address = "MELBOURNE MUSEUM, 11 NICHOLSON STREET, CARLTON, VIC, 3053"

    client = addresshunt.Client(api_key='') # Specify your personal API key

    autocomplete = client.autocomplete(autocomplete_address)
    print("autocomplete: \n" + str(autocomplete) + str('\n'))

    match = client.match(match_address)
    print("match: \n" + str(match) + str('\n'))

    forward_geocode = client.forward_geocode(forward_geocode_address)
    print("forward_geocode: \n" + str(forward_geocode) + str('\n'))

    reverse_geocode = client.reverse_geocode(reverse_geocode_address_latitude, reverse_geocode_address_longitude)
    print("reverse_geocode: \n" + str(reverse_geocode) + str('\n'))

    split = client.split(split_address)
    print("split: \n" + str(split) + str('\n'))

    timezone = client.timezone(timezone_address)
    print("timezone: \n" + str(timezone) + str('\n'))

    validate = client.validate(validate_address)
    print("validate: \n" + str(validate) + str('\n'))


For convenience, all request performing module methods are wrapped inside the ``client`` class.


Dry run
^^^^^^^^^^^^^^^^^^^^
Although errors in query creation should be handled quite decently, you can do a dry run to print the request and its parameters:

.. code:: python

    import addresshunt

    autocomplete_address = "11 NICHOLSON STREET"

    client = addresshunt.Client(api_key='') # Specify your personal API key
    address_list = client.autocomplete(autocomplete_address, dry_run='true')


Support
--------

For issues/bugs/enhancement suggestions, please use https://github.com/AddressHunt/addresshunt-py/issues.