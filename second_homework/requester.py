import urllib.request
import urllib.error
import urllib.parse

while True:
    req = urllib.request.Request('http://localhost:8000/')
    try:
        response = urllib.request.urlopen(req)
        print ("Response body: {}; status code = {}.".format(response.read(), response.getcode()))

    except urllib.error.HTTPError as e:
        print(e.code)
        print(e.read())
