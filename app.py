######################################################
#   A Virendra Rajput Production
#   
#   Title : Nearme 
#   
#   Authored : 19th Aug, 2012
#
#   Twitter: @bkvirendra
#
#   Github: @bkvirendra
#
#   Blog: http://virendrarajput.tumblr.com
#
#   Available under GNU LESSER GENERAL PUBLIC LICENSE
#
#######################################################

import sys, os, urllib2, re, io, string, json, urlparse
from flask import Flask, request, url_for, render_template

app = Flask(__name__)

@app.route('/')
def index():
    # Get the message, {if not message show user the home page}
    if not request.args.get('txtweb-message'):
        return render_template('home.html')
    #getting the message parameters
    userNumber = request.args.get('txtweb-mobile')
    arg = request.args.get('txtweb-message') #the message
    protocol = request.args.get('txtweb-protocol')
    #split the place and the address
    if len(arg.split()) < 2:
        return render_template('home.html')
    place = arg.split(",")
    q = str(place[0])
    address = str(place[1:])
    q = q.lower()
    pat = re.compile(r'\s+')
    q = pat.sub('',q)
    #if address not present, show user the homepage
    if not address:
        return render_template('home.html')
    #check whether the query matches the keywords
    if q == 'about':
        return render_template('about.html')
    elif q == 'help':
        return render_template('help.html')
    elif q == 'types':
        return render_template('types.html')
    address += ", India"
    geoCodeData = "http://maps.googleapis.com/maps/api/geocode/json?address=" + urllib2.quote(address) + "&sensor=false"
    resp = urllib2.urlopen(geoCodeData)
    geoCodeJSON = json.loads(resp.read())
    if geoCodeJSON['status'] == 'OK':
        for k in geoCodeJSON['results']:
            geometry = k['geometry']
            location = geometry.get('location')
            lat = location.get('lat')
            lng = location.get('lng')
    else:
        return render_template('address.html')
    key = "" #key obtainded from txtweb, http://developer.txtweb.com
    locat = str(lat) + "," + str(lng)
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query="+ str(q) +"&radius=1000&location="+ locat +"&sensor=false&key=AIzaSyAdAQtiMBsm-YfTwePiGTylHFXY6g5xFcs"
    data = urllib2.urlopen(url)
    places = json.loads(data.read())
    status = places['status']
    if status == "OK":
        placesAll = places['results']
        places = placesAll[:4]
        for k in places:
            lenStr = len(k['formatted_address'])
            addressFormatted = k['formatted_address']
            lenStr -= 11
            k['formatted_address'] = addressFormatted[:lenStr]
    else:
        return render_template('types.html')
    return render_template('index.html', places=places)

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
