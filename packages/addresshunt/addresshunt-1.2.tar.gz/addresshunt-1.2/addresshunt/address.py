
def autocomplete(client, text, dry_run=None):
    params = {"api_key": client._api_key,
              "text": text}
    return client.request("/address/autocomplete", params, dry_run=dry_run)

def match(client, text, dry_run=None):
    params = {"api_key": client._api_key,
              "text": text}
    return client.request("/address/match", params, dry_run=dry_run)

def forward_geocode(client, text, dry_run=None):
    params = {"api_key": client._api_key,
              "text": text}
    return client.request("/address/forward_geocode", params, dry_run=dry_run)

def reverse_geocode(client, latitude, longitude, dry_run=None):
    params = {"api_key": client._api_key,
              "latitude": latitude,
              "longitude": longitude}
    return client.request("/address/reverse_geocode", params, dry_run=dry_run)

def split(client, text, dry_run=None):
    params = {"api_key": client._api_key,
              "text": text}
    return client.request("/address/split", params, dry_run=dry_run)

def timezone(client, text, dry_run=None):
    params = {"api_key": client._api_key,
              "text": text}
    return client.request("/address/timezone", params, dry_run=dry_run)

def validate(client, text, dry_run=None):
    params = {"api_key": client._api_key,
              "text": text}
    return client.request("/address/validate", params, dry_run=dry_run)