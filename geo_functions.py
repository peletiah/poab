#!/usr/bin/python2.5

from lxml import etree
from xml.etree import ElementTree
import os
import string
import glineenc	    #custom
import tktogpx2	    #custom
import urllib
import ConfigParser
from sqlalchemy import and_
import re
from decimal import Decimal
import decimal
from commands import *
import sys
from datetime import timedelta


basepath='/srv/trackdata/bydate/'


def gentrkptlist(trackpath):
    for gpxfile in os.listdir(trackpath):
	if gpxfile.lower().endswith('.gpx'):
            tree = etree.fromstring(file(trackpath+gpxfile, "r").read())
	    query_trkptlon='//@lon'
	    query_trkptlat='//@lat'
            i=0
	    trkpt=list()
	    for latitude in tree.xpath(query_trkptlat):
                trkptlat=float(tree.xpath(query_trkptlat)[i])
                trkptlon=float(tree.xpath(query_trkptlon)[i])
                trkpt.append((trkptlat,trkptlon))
                i=i+1
    return trkpt

def query_wte(wteapi_key,lat,long):
    f = urllib.urlopen("http://worldtimeengine.com/api/"+wteapi_key+"/"+str(lat)+"/"+str(long))
    tzdetails=f.read()
    f.close()
    return tzdetails

def get_timezone(trackpath,wteapi_key,Session,db_timezone):
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

    #we find out the timezone by getting the timezone for the first and the last coordinate of our trackfiles
    trkptlist=gentrkptlist(trackpath)
    lat,long=trkptlist[0] #first point in the track
    tzdetailsfirst=etree.fromstring(query_wte(wteapi_key,lat,long))
    lat,long=trkptlist[-1] #last point in the track
    tzdetailslast=etree.fromstring(query_wte(wteapi_key,lat,long))
    
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
    query_timezone=session.query(db_timezone).filter(and_(db_timezone.abbreviation==tz_abbreviation,db_timezone.utcoffset==tz_utcoffset))
    if query_timezone.count() == 1:
	for detail in query_timezone.all():
	    tz_detail=detail
	    print 'timezone found - id:'+ str(tz_detail.id) + ' - details:' + str(tz_detail)
    elif query_timezone.count() > 1:
	for detail in query_timezone.all():
	    tz_detail=detail
	    print 'ERROR - more than one timezone-id for the same timezone! - id:'+ str(tz_detail.id) + ' - details:' + str(tz_detail)
    else:
	print 'creating timezone'   
        tz_detail=db_timezone(tz_utcoffset,tz_abbreviation,tz_description,tz_region)
        session.add(tz_detail)
        session.commit()
    	for detail in query_timezone.all():
	    tz_detail=detail
	    print 'timezone created - id:'+ str(tz_detail.id) + ' - details:' + str(tz_detail)
   	
    return tz_detail


def gpx2database(trackpath,wteapi_key,Session,db_infomarker,db_track,db_trackpoint,db_timezone,tz_detail):
    session=Session()
    i=1
    trk_ptnum=dict()
    trk_ptnum[0]=0
    trk_distance=dict()
    trk_distance[0]=0
    trk_span=dict()
    trk_span[0]=timedelta(hours=0,minutes=0,seconds=0)
    trkpts=list()
    latlonlist=list()

    for gpxfile in os.listdir(trackpath):
	if gpxfile.lower().endswith('.gpx'):
	    tree = etree.parse(trackpath+gpxfile)
	    gpx_ns = "http://www.topografix.com/GPX/1/1"
	    ext_ns = "http://gps.wintec.tw/xsd/"
	    root = tree.getroot()
	    fulltrack = root.getiterator("{%s}trk"%gpx_ns)
	    trackSegments = root.getiterator("{%s}trkseg"%gpx_ns)
	    
	    for trk in fulltrack:
		print i
		track_desc=trk.find('{%s}desc'% gpx_ns).text #get the desc-tag from the gpx-file
		trk_ptnum[i]=trk_ptnum[i-1]+int(track_desc.split()[3][:-1])	     #cut out the value from the string e.g. "Total track points: 112."
		trk_rspan=track_desc.split()[6][:-1]	     #cut out the value from the string e.g. "Total time: 0h18m25s."
		trk_distance[i]=trk_distance[i-1]+float(track_desc.split()[8][:-2])	     #cut out the value from the string e.g. "Journey: 4.813Km"
		trk_tspan=re.compile(r'(?P<h>\d+)h(?P<m>\d+)m(?P<s>\d+)s').match(trk_rspan) #find the values of h,m,s and add them to "groups"
		trk_span[i]=trk_span[i-1]+timedelta(hours=int(trk_tspan.group("h")), minutes=int(trk_tspan.group("m")),seconds=int(trk_tspan.group("s"))) #get the values from groups "h","m","s" and save them in a timeformat
		i=i+1
		
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
    print i
    print 'total desc-values - ptnum:' + str(trk_ptnum[i-1]) + ' distance:' + str(trk_distance[i-1]) + ' time:' + str(trk_span[i-1])
    trk_ptnumtotal=trk_ptnum[i-1]
    trk_distancetotal=trk_distance[i-1]
    trk_spantotal=trk_span[i-1]

    #create a encoded polyline from the latitude-longitude-list
    gencpoly=glineenc.encode_pairs(latlonlist)

    trkpt_1ts=trkpts[0][7] #first timestamp in the trackpoint-list
    query_track=session.query(db_track).filter(and_(db_track.date==trkpt_1ts,db_track.trkptnum==trk_ptnumtotal,db_track.distance==trk_distancetotal,db_track.timespan==trk_spantotal,db_track.gencpoly_pts==gencpoly[0],db_track.gencpoly_levels==gencpoly[1]))
    if query_track.count() == 1:
	for detail in query_track.all():
	    track_detail=detail
	    print 'track found - id:'+ str(track_detail.id) + ' - details:' + str(track_detail)
    elif query_track.count() > 1:
	for detail in query_track.all():
	    track_detail=detail
	    print 'more than one track found! - id:'+ str(track_detail.id) + ' - details:' + str(track_detail)
    else:
        session.add(db_track(trkpt_1ts,trk_ptnumtotal,trk_distancetotal,trk_spantotal,gencpoly[0],gencpoly[1]))
	session.commit()
    	for detail in query_track.all():
	    track_detail=detail
	    print 'track created! - id:'+ str(track_detail.id) + ' - details:' + str(track_detail)

    i=0
    for trkpt in trkpts:
	lat,lon,altitude,velocity,temperature,direction,pressure,time=trkpts[i]
	query_trackpoint=session.query(db_trackpoint).filter(and_(db_trackpoint.track_id==track_detail.id,db_trackpoint.timezone_id==tz_detail.id,db_trackpoint.latitude==lat,db_trackpoint.longitude==lon,db_trackpoint.altitude==float(altitude),db_trackpoint.velocity==velocity,db_trackpoint.temperature==temperature,db_trackpoint.direction==direction,db_trackpoint.pressure==pressure,db_trackpoint.timestamp==time))
	if query_trackpoint.count() == 1:
	    for detail in query_trackpoint.all():
		trkpt_detail=detail
		print 'Trackpoint already exists - id:'+ str(trkpt_detail.id) + ' details:' + str(trkpt_detail)
        elif query_trackpoint.count() > 1:
	    for detail in query_trackpoint.all():
		trkpt_detail=detail
		print 'trackpoint duplicate found! - id:'+ str(trkpt_detail.id) + ' - details:' + str(trkpt_detail)
	else:
	    #trackpoints are unique, insert them now
	    session.add(db_trackpoint(track_detail.id,tz_detail.id,lat,lon,float(altitude),velocity,temperature,direction,pressure,time)) 
            session.commit()
	    for detail in query_trackpoint.all():
		trkpt_detail=detail

	#in the middle of the track, we create an infomarker-entry with the current trackpoint_id
	if i==track_detail.trkptnum/2:
	  query_infomarker=session.query(db_infomarker).filter(db_infomarker.trackpoint_id==trkpt_detail.id)
	  if query_infomarker.count() == 1:
	    for detail in query_infomarker.all():
		print 'infomarker already exists! id:'+str(detail.id)+' - trackpoint_id:' + str(detail.trackpoint_id)
		infomarker_id=detail.id
	  elif query_infomarker.count() > 1:
    	    for detail in query_infomarker.all():
		print 'infomarker duplicate exists! id:'+str(detail.id)+' - trackpoint_id:' + str(detail.trackpoint_id)
		infomarker_id=detail.id
	  else:
	    session.add(db_infomarker(trkpt_detail.id))
    	    for detail in query_infomarker.all():
		print 'infomarker created! id:'+str(detail.id)+' - trackpoint_id:' + str(detail.trackpoint_id)
		infomarker_id=detail.id
	i=i+1
    return infomarker_id	
	    

def geotag(imagepath,trackpath):#geotag the pictures in imagepath with data from gpxfile
    if os.system("/usr/bin/perl /root/scripts/gpsPhoto.pl --dir "+imagepath+" --gpsdir "+trackpath+" --timeoffset 0 --overwrite-geotagged > /var/log/poab/geotag.log 2>&1") == 0:
	pass
    else:
	print 'An error occured at geotag'
			
