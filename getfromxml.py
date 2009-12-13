#!/usr/bin/python2.5

from lxml import etree
from xml.etree import ElementTree
import os
import string
import tktogpx2	    #custom
import image_functions #custom
import geo_functions #custom
import urllib
import ConfigParser
import db_functions #custom
from sqlalchemy import and_
import re
from decimal import Decimal
import decimal
import log_functions #custom

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
    try:
        done =  (tree.xpath('//done')[0]).text
        if done == 'true':
            return done
    except IndexError:
        pass
    print tree.xpath('//topic')[0].text
    topic =  (tree.xpath('//topic')[0]).text.replace("&gt;",">").replace("&lt;","<")
    logtext =  (tree.xpath('//logtext')[0]).text.replace("&gt;",">").replace("&lt;","<")
    filepath =  (tree.xpath('//filepath')[0]).text
    photosetname =  (tree.xpath('//photoset')[0]).text
    photodescription =  (tree.xpath('//photodescription')[0]).text
    phototitle =  (tree.xpath('//phototitle')[0]).text
    xmlimglist=list()
    xmltaglist=list()
    query_xmlimglist='//img'
    for element in tree.xpath(query_xmlimglist):
	xmlimglist.append(element.text)
    query_xmltaglist='//tag'
    for element in tree.xpath(query_xmltaglist):
	xmltaglist.append(element.text)

    return topic,logtext,filepath,photosetname,photodescription,phototitle,xmlimglist,xmltaglist		

def finishxml(xmlfile):
    tree = etree.fromstring(file(basepath+xmlfile,"r").read())
    query='//log'
    element = tree.xpath(query)
    finishtext='''<done>true</done>'''
    element[0].append(etree.fromstring(finishtext))
    f=file(basepath+xmlfile,"w")
    f.write(etree.tostring(tree))
    f.close()
    tree = etree.fromstring(file(basepath+xmlfile, 'r').read())     

def main(basepath):
    pg_user,pg_passwd,flickrapi_key,flickrapi_secret,wteapi_key=getcredentials('/root/poab_upload/poab/credentials.ini')
    print basepath
    for xmlfile in os.listdir(basepath):
	if xmlfile.lower().endswith('.xml'):
	    print xmlfile
	    if parsexml(xmlfile) == 'true':
		pass
	    else:
		topic,logtext,filepath,photosetname,photodescription,phototitle,xmlimglist,xmltaglist=parsexml(xmlfile)
			# topic - topic of the log-entry
			# logtext - content-text of the log-entry
			# filepath - where are the files belonging to this xml-file situated 
			# photosetname - name of the set for flickr
			# photodescription - description of the photos for flickr
			# phototitle - title of the photos for flickr
			# xmlimglist - list of the images in the xml
			# xmltaglist - list of the images in the xml
		imagepath=filepath+'images/best/'
		try:
		    trackpath=filepath+'trackfile/'
		    for trackfile in os.listdir(trackpath):
		        print trackfile
		        if trackfile.lower().endswith('.tk1'):
			    #passes outputDir,gpx-filename and tkFileName to tk2togpx.interactive to convert the tk1 to gpx
			    if os.path.exists(trackpath+trackfile[:-3]+'gpx'): # is there already a gpx-file with this name?
			       print 'gpx-file already exists, passing'
			    else:
			        tktogpx2.interactive(trackpath,trackfile.split('.')[0]+'.gpx',trackpath+trackfile)
			else:
			    pass 
		except IOError:
		    print 'No Trackfile found!'
		Session,db_log,db_comments,db_continent,db_country,db_photosets,db_imageinfo,db_track,db_trackpoint,db_timezone,db_image2tag,db_phototag=db_functions.initdatabase(pg_user,pg_passwd)
		tz_detail=geo_functions.get_timezone(trackpath,wteapi_key,Session,db_timezone)
		infomarker_id=geo_functions.gpx2database(trackpath,wteapi_key,Session,db_track,db_trackpoint,db_timezone,db_country,tz_detail)
		geo_functions.geotag(imagepath,trackpath)
		imglist=image_functions.img2flickr(imagepath,xmlimglist,xmltaglist,photosetname,photodescription,phototitle,flickrapi_key,flickrapi_secret,infomarker_id,Session,db_trackpoint,db_imageinfo,db_image2tag,db_phototag,db_photosets)
		print imglist
		log_detail=log_functions.log2db(topic,logtext,imglist,infomarker_id,Session,db_log)
		print 'image_functions'
		image_functions.logid2images(log_detail,imglist,Session,db_imageinfo)
		finishxml(xmlfile)		
main(basepath)
print 'DONE'
