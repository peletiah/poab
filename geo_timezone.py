#!/usr/bin/python2.5

from lxml import etree
from xml.etree import ElementTree
import os
import string
import gpx2list	    #custom
import glineenc	    #custom
import tktogpx2	    #custom
import flickrupload #custom
import urllib
import ConfigParser
import initdatabase #custom
from sqlalchemy import and_
import re
from decimal import Decimal
import decimal

basepath='/srv/trackdata/bydate/'

def query_wte(wteapi_key,lat,long):
    f = urllib.urlopen("http://worldtimeengine.com/api/"+wteapi_key+"/"+str(lat)+"/"+str(long))
    tzdetails=f.read()
    f.close()
    return tzdetails

def get_timezone(gpxfile,wteapi_key,Session,timezone):
######################### replace this shit by worldtimeengine-query when finished #############
    tzdetailsfirst=etree.fromstring('''<?xml version="1.0" encoding="UTF-8" ?>
<timezone xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://worldtimeengine.com/timezone.xsd">
    <version>1.1</version>
    <location>
        <region>Taiwan</region>
        <latitude>25.0684016</latitude>
        <longitude>121.6382592</longitude>
    </location>
    <time>
        <utc>2008-11-28 21:35:12</utc>
        <local>2008-11-29 05:35:12</local>
        <zone>
            <hasDST>false</hasDST>
            <current>
                <abbreviation>CST</abbreviation>
                <description>Chinese Standard Time</description>
                <utcoffset>-8:00</utcoffset>
            </current>
        </zone>
    </time>
</timezone>''')

    tzdetailslast=etree.fromstring('''<?xml version="1.0" encoding="UTF-8" ?>
<timezone xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://worldtimeengine.com/timezone.xsd">
    <version>1.1</version>
    <location>
        <region>Taiwan</region>
        <latitude>24.9993056</latitude>
        <longitude>121.49152</longitude>
    </location>
    <time>
        <utc>2008-11-28 21:35:12</utc>
        <local>2008-11-29 05:35:12</local>
        <zone>
            <hasDST>false</hasDST>
            <current>
                <abbreviation>CST</abbreviation>
                <description>Chinese Standard Time</description>
                <utcoffset>-8:00</utcoffset>
            </current>
        </zone>
    </time>
</timezone>''')
    ################################################################################

    trkptlist=gpx2list.trkptlist(gpxfile)
    lat,long=trkptlist[0] #first point in the track
   # tzdetailsfirst=etree.fromstring(query_wte(wteapi_key,lat,long))
    lat,long=trkptlist[-1] #last point in the track
   # tzdetailslast=etree.fromstring(query_wte(wteapi_key,lat,long))
    print tzdetailsfirst
    print tzdetailslast
    
    if (tzdetailsfirst.xpath('//utcoffset')[0]).text == (tzdetailslast.xpath('//utcoffset')[0]).text:
	tz_utcoffset=(tzdetailslast.xpath('//utcoffset')[0]).text
	tz_abbreviation=(tzdetailslast.xpath('//abbreviation')[0]).text	
	tz_description=(tzdetailslast.xpath('//description')[0]).text
	tz_region=(tzdetailslast.xpath('//region')[0]).text	
	print tz_utcoffset,tz_abbreviation,tz_description,tz_region	
    else:
	print 'We need to check this tracklist in more detail, as there was a shift in the timezone'
	print 'between the first and the last trackpoint'
	i=False
	#function to check the tracklist toroughly goes here
    
    session=Session()
    query=session.query(timezone).filter(and_(timezone.abbreviation==tz_abbreviation,timezone.utcoffset==tz_utcoffset))
    if query.count() == 1:
	for detail in query.all():
	    tz_detail=detail
	    print 'timezone found - id:'+ str(tz_detail.id) + ' - details:' + str(tz_detail)
    elif query.count() > 1:
	for detail in query.all():
	    tz_detail=detail
	    print 'ERROR - more than one timezone-id for the same timezone! - id:'+ str(tz_detail.id) + ' - details:' + str(tz_detail)
    else:
	print 'creating timezone'   
        tz_detail=timezone(tz_utcoffset,tz_abbreviation,tz_description,tz_region)
        session.add(tz_detail)
        session.commit()
    	for detail in query.all():
	    tz_detail=detail
	    print 'timezone created - id:'+ str(tz_detail.id) + ' - details:' + str(tz_detail)
   	
    return tz_detail


def gpx2database(gpxfile,wteapi_key,Session,infomarker,track,trackpoint,timezone,tz_detail):
    session=Session()
    tree = etree.parse(gpxfile)
    gpx_ns = "http://www.topografix.com/GPX/1/1"
    ext_ns = "http://gps.wintec.tw/xsd/"
    root = tree.getroot()
    fulltrack = root.getiterator("{%s}trk"%gpx_ns)
    trackSegments = root.getiterator("{%s}trkseg"%gpx_ns)
    lat=dict()
    lon=dict()
    altitude=dict()
    time=dict()
    temperature=dict()
    pressure=dict()
    i=0
    trkpts=list()
    latlonlist=list()
    for trk in fulltrack:
	track_desc=trk.find('{%s}desc'% gpx_ns).text
	trk_ptnum=track_desc.split()[3][:-1]
	trk_rspan=track_desc.split()[6][:-1]
	trk_distance=track_desc.split()[8][:-2]
	trk_tspan=re.compile(r'(?P<h>\d+)h(?P<m>\d+)m(?P<s>\d+)s').match(trk_rspan)
	trk_span=trk_tspan.group("h")+':'+trk_tspan.group("m")+':'+trk_tspan.group("s")
	
    for trackSegment in trackSegments:
	for trackPoint in trackSegment:
	    lat=trackPoint.attrib['lat']
	    lon=trackPoint.attrib['lon']
	    altitude=trackPoint.find('{%s}ele'% gpx_ns).text
	    time=trackPoint.find('{%s}time'% gpx_ns).text.replace('T',' ')[:-1] #replace the "T" with " " and remove the "Z" from the end of the string
	    desc=trackPoint.find('{%s}desc'% gpx_ns).text.split(', ') #split the description to get "speed" and "direction"-values
	    velocity=None
	    direction=None
	    for value in desc:
		if value.split('=')[0] == 'Speed':
		    velocity=value.split('=')[1][:-4]
		elif value.split('=')[0] == 'Course':
		    direction=value.split('=')[1][:-4]
	    temperature=trackPoint.find("{%s}extensions/{%s}TrackPointExtension/{%s}Temperature" % (gpx_ns,ext_ns,ext_ns)).text
	    pressure=trackPoint.find("{%s}extensions/{%s}TrackPointExtension/{%s}Pressure" % (gpx_ns,ext_ns,ext_ns)).text
	    trkpts.append((lat,lon,altitude,velocity,temperature,direction,pressure,time))
	    latlonlist.append((float(lat),float(lon)))
	    i=i+1

    #create a encoded polyline from the latitude-longitude-list
    gencpoly=glineenc.encode_pairs(latlonlist)

    trkpt_1ts=trkpts[0][7] #first timestamp in the trackpoint-list
    query=session.query(track).filter(and_(track.date==trkpt_1ts,track.trkptnum==trk_ptnum,track.distance==trk_distance,track.timespan==trk_span,track.gencpoly_pts==gencpoly[0],track.gencpoly_levels==gencpoly[1]))
    if query.count() == 1:
	for detail in query.all():
	    track_detail=detail
	    print 'track found - id:'+ str(track_detail.id) + ' - details:' + str(track_detail)
    elif query.count() > 1:
	for detail in query.all():
	    track_detail=detail
	    print 'more than one track found! - id:'+ str(track_detail.id) + ' - details:' + str(track_detail)
    else:
        session.add(track(trkpt_1ts,trk_ptnum,trk_distance,trk_span,gencpoly[0],gencpoly[1]))
	session.commit()
    	for detail in query.all():
	    track_detail=detail
	    print 'track created! - id:'+ str(track_detail.id) + ' - details:' + str(track_detail)

    i=0
    for trkpt in trkpts:
	lat,lon,altitude,velocity,temperature,direction,pressure,time=trkpts[i]
	query=session.query(trackpoint).filter(and_(trackpoint.track_id==track_detail.id,trackpoint.timezone_id==tz_detail.id,trackpoint.latitude==lat,trackpoint.longitude==lon,trackpoint.altitude==float(altitude),trackpoint.velocity==velocity,trackpoint.temperature==temperature,trackpoint.direction==direction,trackpoint.pressure==pressure,trackpoint.timestamp==time))
	if query.count() == 1:
	    for detail in query.all():
		trkpt_detail=detail
		print 'Trackpoint already exists - id:'+ str(trkpt_detail.id) + ' details:' + str(trkpt_detail)
        elif query.count() > 1:
	    for detail in query.all():
		trkpt_detail=detail
		print 'trackpoint duplicate found! - id:'+ str(trkpt_detail.id) + ' - details:' + str(trkpt_detail)
	else:
	    #trackpoints are unique, insert them now
	    session.add(trackpoint(track_detail.id,tz_detail.id,lat,lon,float(altitude),velocity,temperature,direction,pressure,time)) 
            session.commit()
	    for detail in query.all():
		trkpt_detail=detail
		#in the middle of the track, we create an infomarker-entry with the current trackpoint_id
		if i==track_detail.trkptnum/2:
		  query2=session.query(infomarker).filter(infomarker.trackpoint_id==trkpt_detail.id)
		  if query2.count() == 1:
		    for detail in query2.all():
			print 'infomarker already exists! id:'+str(detail.id)+' - trackpoint_id:' + str(detail.trackpoint_id)
		  elif query2.count() > 1:
    		    for detail in query2.all():
			print 'infomarker duplicate exists! id:'+str(detail.id)+' - trackpoint_id:' + str(detail.trackpoint_id)
		  else:
    		    session.add(infomarker(trkpt_detail.id))
	i=i+1
	    

def geotag(imagepath,gpxfile):#geotag the pictures in imagepath with data from gpxfile
    if os.system("/usr/bin/perl /root/scripts/gpsPhoto.pl --dir "+imagepath+" --gpsfile "+gpxfile+" --timeoffset 0 --overwrite-geotagged > /var/log/poab/geotag.log 2>&1") == 0:
	pass
    else:
	print 'An error occured at geotag'
			


