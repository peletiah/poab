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
import talk2flickr
import progress #custom
import datetime

basepath='/srv/trackdata/bydate/'

def gentrkptlist(trackpath):
    for gpxfile in os.listdir(trackpath):
        if gpxfile.lower().endswith('.gpx'):
            tree = etree.fromstring(file(trackpath+gpxfile, "r").read())
            query_trkptlon='//@lon'
            query_trkptlat='//@lat'
            i=0
            trkptlist=list()
            latlist=tree.xpath(query_trkptlat)
            lonlist=tree.xpath(query_trkptlon)
            for latitude in latlist:
                trkptlist.append((float(latlist[i]),float(lonlist[i])))
                i=i+1
    return trkptlist


def gpx2database(trackpath,wteapi_key,database,trk_color):
    print 'FUNCTION GPX2DATABASE'
    session=database.db_session()
    db_track=database.db_track
    db_trackpoint=database.db_trackpoint
    db_country=database.db_country
    trk_ptnum=dict()
    trk_ptnum[0]=0
    trk_distance=dict()
    trk_distance[0]=0
    trk_span=dict()
    trk_span[0]=timedelta(hours=0,minutes=0,seconds=0)
    trkptlist=list()
    latlonlist=list()
    
    for gpxfile in os.listdir(trackpath):
        if gpxfile.lower().endswith('.gpx'):
            tree = etree.parse(trackpath+gpxfile)
            gpx_ns = "http://www.topografix.com/GPX/1/1"
            ext_ns = "http://gps.wintec.tw/xsd/"
            root = tree.getroot()
            fulltrack = root.getiterator("{%s}trk"%gpx_ns)
            trackSegments = root.getiterator("{%s}trkseg"%gpx_ns)
            i=1
            for trk in fulltrack:
                print 'gpxfile trk no.' + str(i)
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
                    velocity=0
                    direction=0
                    for value in desc:
			               if value.split('=')[0] == 'Speed':
			                   velocity=value.split('=')[1][:-4]
			               elif value.split('=')[0] == 'Course':
			                   direction=value.split('=')[1][:-4]
                    try:
			               temperature=trackPoint.find("{%s}extensions/{%s}TrackPointExtension/{%s}Temperature" % (gpx_ns,ext_ns,ext_ns)).text
			               pressure=trackPoint.find("{%s}extensions/{%s}TrackPointExtension/{%s}Pressure" % (gpx_ns,ext_ns,ext_ns)).text
                    except AttributeError:
			               temperature=None
			               pressure=None
                    print lat,lon,time
                    trkptlist.append((lat,lon,altitude,velocity,temperature,direction,pressure,time))
                    latlonlist.append((float(lat),float(lon)))
    
    #get the last value of each "desc"-segment, this value represents the total from the several gpx-files
    trk_ptnumtotal=trk_ptnum[i-1]
    trk_distancetotal=trk_distance[i-1]
    trk_spantotal=trk_span[i-1]
    
    #create an encoded polyline from the latitude-longitude-list
    gencpoly=glineenc.encode_pairs(latlonlist)
    
    trkpt_firsttimestamp=trkptlist[0][7] #first timestamp in the trackpoint-list
    query_track=session.query(db_track).filter(and_(db_track.date==trkpt_firsttimestamp,db_track.trkptnum==trk_ptnumtotal,db_track.distance==trk_distancetotal,db_track.timespan==trk_spantotal,db_track.gencpoly_pts==gencpoly[0].replace('\\','\\\\'),db_track.gencpoly_levels==gencpoly[1]))
    if query_track.count() == 1:
        for detail in query_track.all():
            track_detail=detail
            print 'track found - id:'+ str(track_detail.id)# + ' - details:' + str(track_detail)
    elif query_track.count() > 1:
        for detail in query_track.all():
            track_detail=detail
            print 'more than one track found! - id:'#+ str(track_detail.id) + ' - details:' + str(track_detail)
    else:
        session.add(db_track(trkpt_firsttimestamp,trk_ptnumtotal,trk_distancetotal,trk_spantotal,gencpoly[0].replace('\\','\\\\'),gencpoly[1],trk_color))
        session.commit()
        for detail in query_track.all():
            track_detail=detail
            print 'track created! - id:'+ str(track_detail.id)# + ' - details:' + str(track_detail)

    i=0
    print "\nAdding trackpoints to database:\n"
    pb=progress.progressbarClass(track_detail.trkptnum,"=")
    for trkpt in trkptlist:
        lat,lon,altitude,velocity,temperature,direction,pressure,time=trkptlist[i]
        query_trackpoint=session.query(db_trackpoint).filter(and_(db_trackpoint.track_id==track_detail.id,db_trackpoint.latitude==lat,db_trackpoint.longitude==lon,db_trackpoint.timestamp==time))
        if query_trackpoint.count() == 1:
            for detail in query_trackpoint.all():
                trkpt_detail=detail
                #print 'Trackpoint already exists - id:'+ str(trkpt_detail.id) + ' details:' + str(trkpt_detail)
        elif query_trackpoint.count() > 1:
            for detail in query_trackpoint.all():
                trkpt_detail=detail
                print 'trackpoint duplicate found! - id:'+ str(trkpt_detail.id) + ' - details:' + str(trkpt_detail)
        else:
            #trackpoints are unique, insert them now
            session.add(db_trackpoint(track_detail.id,None,None,lat,lon,float(altitude),velocity,temperature,direction,pressure,time,False,None))
            session.commit()
            for detail in query_trackpoint.all():
                trkpt_detail=detail
                #print 'trackpoint added! - id:'+ str(trkpt_detail.id) + ' - details:' + str(trkpt_detail)
        #in the middle of the track, we set the current infomarker.trackpoint_id to true as this is our infomarker-point
        if i==track_detail.trkptnum/2:
            for column in query_trackpoint.all():
                column.infomarker=True
                session.commit()
                infomarker_id=trkpt_detail.id
        pb.progress(i)
        i=i+1
    return infomarker_id	






def get_country(lat,lon,database):
    session=database.db_session()
    db_country=database.db_country
    accuracy=1 #level of region-detail in flickr, 1 is world, 8 is district
    flickr_countryname=talk2flickr.findplace(lat,lon,accuracy)
    query_country=session.query(db_country).filter(db_country.flickr_countryname==flickr_countryname)
    country=query_country.one()
    print 'country found - id:'+ str(country.iso_numcode) + ' - details:' + str(country)
    return country


def query_wte(wteapi_key,lat,long):
    f = urllib.urlopen("http://worldtimeengine.com/api/"+wteapi_key+"/"+str(lat)+"/"+str(long))
    tzdetails=f.read()
    f.close()
    print 'tzdetails: '+tzdetails
    return tzdetails



def get_timezone(database,lat,lon,date,wteapi_key):
    tzdetails=etree.fromstring(query_wte(wteapi_key,lat,lon))
    #wte delivers current daylight-saving-time(dst)-end and next dst
    #to get the most probable timezone for the $date, we check if it is within
    #current or "modified" next dst-dates
    xml_curr_dst=(tzdetails.xpath('/timezone/time/zone/current/effectiveUntil')[0]).text
    xml_next_dst=(tzdetails.xpath('/timezone/time/zone/next/effectiveUntil')[0]).text
    curr_year=xml_curr_dst.split('-',1)[0]
    next_month_day=xml_next_dst.split('-',1)[1]
    next_last_dst=curr_year+'-'+next_month_day
    current_dst_end=datetime.datetime.strptime(xml_curr_dst,'%Y-%m-%d %H:%M:%S')
    next_last_dst_end=datetime.datetime.strptime(next_last_dst,'%Y-%m-%d %H:%M:%S')
    if date < next_last_dst_end or date > current_dst_end:
        tz_path='next'
    else:
        tz_path='current'
    tz_utcoffset=(tzdetails.xpath('/timezone/time/zone/'+tz_path+'/utcoffset')[0]).text
    tz_abbreviation=(tzdetails.xpath('/timezone/time/zone/'+tz_path+'/abbreviation')[0]).text	
    tz_description=(tzdetails.xpath('/timezone/time/zone/'+tz_path+'/description')[0]).text
    tz_region=(tzdetails.xpath('/timezone/location/region')[0]).text	
    session=database.db_session()
    db_timezone=database.db_timezone
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




def add_tz_country_location(xmlimglist_plus_db_details,wteapi_key,infomarker_id,database):
    #find associated trackpoints of images
    session=database.db_session()
    db_imageinfo=database.db_imageinfo
    db_trackpoint=database.db_trackpoint
    for imgdetail in xmlimglist_plus_db_details:
        trkptid=imgdetail.imageinfo_detail.trackpoint_id
        q = session.query(db_trackpoint).filter(db_trackpoint.id==trkptid)
        if q.count() == 1:
            trackpoint=q.one()
            lat=trackpoint.latitude
            lon=trackpoint.longitude
            country=get_country(lat,lon,database)
            location=talk2flickr.findplace(lat,lon,8)
            tz_detail=get_timezone(database,lat,lon,trackpoint.timestamp,wteapi_key)
            trackpoint.timezone_id=tz_detail.id
            trackpoint.country_id=country.iso_numcode
            trackpoint.location=location
            session.commit()
            print "Added trkpt-details for imgid:"+str(imgdetail.imageinfo_detail.id)+", trkptid:"+str(trackpoint.id)+", tzabb:"+tz_detail.abbreviation+", location:"+location
        else:
            print "No trackpoint for this image - therefore no timezone, location or country-details :-("
    q = session.query(db_trackpoint).filter(db_trackpoint.id==infomarker_id)
    trackpoint=q.one()
    lat=trackpoint.latitude
    lon=trackpoint.longitude
    country=get_country(lat,lon,database)
    location=talk2flickr.findplace(lat,lon,8)
    tz_detail=get_timezone(database,lat,lon,trackpoint.timestamp,wteapi_key)
    trackpoint.timezone_id=tz_detail.id
    trackpoint.country_id=country.iso_numcode
    trackpoint.location=location
    session.commit()
         
     

       
def defunct_get_timezone(trackpath,wteapi_key,database):
    print 'FUNCTION GET_TIMEZONE'
######################### replace this shit by worldtimeengine-query when finished #############
#    tzdetailsfirst=etree.fromstring('''<?xml version="1.0" encoding="UTF-8" ?>
#<timezone xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://worldtimeengine.com/timezone.xsd">
#    <version>1.1</version>
#    <location>
#        <region>Austria</region>
#        <latitude>47.160992</latitude>
#        <longitude>11.5210216</longitude>
#    </location>
#    <time>
#        <utc>2008-12-30 15:45:32</utc>
#        <local>2008-12-30 16:45:32</local>
#        <zone>
#            <hasDST>true</hasDST>
#            <current>
#                <abbreviation>CET</abbreviation>
#                <description>Central European Time</description>
#                <utcoffset>+1:00</utcoffset>
#                <isdst>false</isdst>
#                <effectiveUntil>2009-03-29 01:00:00</effectiveUntil>
#            </current>
#            <next>
#                <abbreviation>CEST</abbreviation>
#                <description>Central European Summer Time</description>
#                <utcoffset>+2:00</utcoffset>
#                <isdst>true</isdst>
#                <effectiveUntil>2009-10-25 01:00:00</effectiveUntil>
#            </next>
#        </zone>
#    </time>
#</timezone>''')
##
#    tzdetailslast=etree.fromstring('''<?xml version="1.0" encoding="UTF-8" ?>
#<timezone xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://worldtimeengine.com/timezone.xsd">
#    <version>1.1</version>
#    <location>
#        <region>Austria</region>
#        <latitude>47.160992</latitude>
#        <longitude>11.5210216</longitude>
#    </location>
#    <time>
#        <utc>2008-12-30 15:45:32</utc>
#        <local>2008-12-30 16:45:32</local>
#        <zone>
#            <hasDST>true</hasDST>
#            <current>
#                <abbreviation>CET</abbreviation>
#                <description>Central European Time</description>
#                <utcoffset>+1:00</utcoffset>
#                <isdst>false</isdst>
#                <effectiveUntil>2009-03-29 01:00:00</effectiveUntil>
#            </current>
#            <next>
#                <abbreviation>CEST</abbreviation>
#                <description>Central European Summer Time</description>
#                <utcoffset>+2:00</utcoffset>
#                <isdst>true</isdst>
#                <effectiveUntil>2009-10-25 01:00:00</effectiveUntil>
#            </next>
#        </zone>
#    </time>
#</timezone>''')
#    ################################################################################

#we find out the timezone by getting the timezone for the first and the last coordinate of our trackfiles
    trkptlist=gentrkptlist(trackpath)
    lat,long=trkptlist[0] #first point in the track
    tzdetailsfirst=etree.fromstring(query_wte(wteapi_key,lat,long))
    print tzdetailsfirst
    lat,long=trkptlist[-1] #last point in the track
    tzdetailslast=etree.fromstring(query_wte(wteapi_key,lat,long))
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
        
    #function to check the tracklist toroughly goes here

    session=database.db_session()
    db_timezone=database.db_timezone
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


