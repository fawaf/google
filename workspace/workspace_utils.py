def verify_site(site, client):
    wr_client = client.webResource()

    print(wr_client.get(id=site).execute())

    body = {
        "site": {
            "identifier": site,
            "type": "INET_DOMAIN",
        },
        "verificationMethod": "DNS",
    }

    # get token (txt record) for dns
    print(f"getting token (txt record) for site {site}")
    token = wr_client.getToken(body=body).execute()["token"]
    print(token)

    # add to dns

    # ask google to verify
    body.pop("verificationMethod")
    print(f"asking google to verify site {site}")
    print(wr_client.insert(verificationMethod="DNS", body=body).execute())
