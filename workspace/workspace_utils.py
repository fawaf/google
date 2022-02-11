def verify_site(site, client):
    list_sites = client.webResource().list().execute()
    import json
    print(json.dumps(list_sites))
