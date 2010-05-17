import os
from lxml import etree
from xml.etree import ElementTree
import os
import string
import glineenc


latlonlist=list()
trackpath='/srv/trackdata/bydate/2009-09-01/trackfile/'


for gpxfile in os.listdir(trackpath):
    if gpxfile.lower().endswith('.gpx'):
        tree = etree.parse(trackpath+gpxfile)
        gpx_ns = "http://www.topografix.com/GPX/1/1"
        ext_ns = "http://gps.wintec.tw/xsd/"
        root = tree.getroot()
        fulltrack = root.getiterator("{%s}trk"%gpx_ns)
        trackSegments = root.getiterator("{%s}trkseg"%gpx_ns)
        
        for trackSegment in trackSegments:
            for trackPoint in trackSegment:
                lat=trackPoint.attrib['lat']
                lon=trackPoint.attrib['lon']
                latlonlist.append((float(lat),float(lon)))
        gencpoly=glineenc.encode_pairs(latlonlist)
        print gencpoly[0].replace('\\','\\\\')
        print gencpoly[1]
