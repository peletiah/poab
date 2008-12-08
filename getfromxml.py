#!/usr/bin/python2.5

from lxml import etree
from xml.etree import ElementTree
import os
import string
import tktogpx2	    #custom
import image_functions #custom
import geo_timezone #custom
import urllib
import ConfigParser
import initdatabase #custom
from sqlalchemy import and_
import re
from decimal import Decimal
import decimal

basepath='/srv/trackdata/bydate/'

def getcredentials(credentialfile):
    config=ConfigParser.ConfigParser()
    open(credentialfile)
    config.read(credentialfile)
    pg_user=config.get("postgresql","username")
    pg_passwd=config.get("postgresql","password")
    flickrapi_key=config.get("flickrcredentials","api_key")
    flickrapi_secret=config.get("flickrcredentials","api_secret")
    wteapi_key=config.get("worldtimeengine","api_key")
    return pg_user,pg_passwd,flickrapi_key,flickrapi_secret,wteapi_key


def parsexml(xmlfile):
    tree = etree.fromstring(file(basepath+xmlfile, "r").read())
    topic =  (tree.xpath('//topic')[0]).text.replace("&gt;",">").replace("&lt;","<")
    logtext =  (tree.xpath('//logtext')[0]).text.replace("&gt;",">").replace("&lt;","<")
    filepath =  (tree.xpath('//filepath')[0]).text
    trackfile =  (tree.xpath('//trackfile')[0]).text
    photoset =  (tree.xpath('//photoset')[0]).text
    i=1
    imglist=dict()
    while i < 100:
	try:
	    imglist[i]=(tree.xpath('//img'+str(i))[0]).text
	    i=i+1
	except IndexError:
	    i=i+1
	    pass
    return topic,logtext,filepath,trackfile,photoset,imglist		

def main(basepath):
    pg_user,pg_passwd,flickrapi_key,flickrapi_secret,wteapi_key=getcredentials('/root/scripts/credentials.ini')
    for xmlfile in os.listdir(basepath):
	if xmlfile.lower().endswith('.xml'):
	    topic,logtext,filepath,trackfile,photoset,imglist=parsexml(xmlfile)
				# topic - topic of the log-entry
				# logtext - content-text of the log-entry
				# filepath - where are the files belonging to this xml-file situated 
				# trackfile - the gps-trackfile
				# photoset - name of the set for flickr
				# imglist - list of the images in the xml
	    imagepath=filepath+'images_sorted/'
	    try:
		trackpath=filepath+'trackfile/'
		#passes outputDir,gpx-filename and tkFileName to tk2togpx.interactive to convert the tk1 to gpx
		tktogpx2.interactive(trackpath,filepath.rsplit('/',2)[1]+'.gpx',trackpath+trackfile) 
		gpxfile=trackpath+filepath.rsplit('/',2)[1]+'.gpx'
	    except IOError:
		print 'trackfile missing!'
		gpxfile=None
	    Session,blog,comments,continent,country,photosets,imageinfo,infomarker,track,trackpoint,timezone,image2tag,phototag=initdatabase.initdatabase(pg_user,pg_passwd)
	    tz_detail=geo_timezone.get_timezone(gpxfile,wteapi_key,Session,timezone)
	    infomarker_id=geo_timezone.gpx2database(gpxfile,wteapi_key,Session,infomarker,track,trackpoint,timezone,tz_detail)
	    geo_timezone.geotag(imagepath,gpxfile)
	    tags='simpletag "double tag" anothersimpletag'
	    image_functions.img2flickr(imagepath,imglist,photoset,tags,flickrapi_key,flickrapi_secret,infomarker_id,Session,trackpoint,imageinfo,image2tag,phototag,photosets)

main(basepath)

