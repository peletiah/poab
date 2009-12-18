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
import time, datetime
from time import strftime

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


def parsexml(basepath,xmlfile):
    tree = etree.parse(basepath+xmlfile)
    root = tree.getroot()
    logs=root.getiterator("log")
    for log in logs:
        try:
            done =  log.find('done').text
            if done == 'true':
                return done
        except AttributeError:
            pass
        print log.find('topic').text
        topic =  log.find('topic').text.replace("&gt;",">").replace("&lt;","<")
        logtext =  log.find('logtext').text.replace("&gt;",">").replace("&lt;","<")
        filepath =  log.find('filepath').text
        print filepath
        photosetname =  log.find('photoset').text
        phototitle =  log.find('phototitle').text
        createdate =  log.find('createdate').text
        num_of_img =  int(log.find('num_of_img').text)
        createdate = time.strptime(createdate,'%Y-%m-%d %H:%M:%S')
        images = root.getiterator("img")
        xmlimglist=list()
        for image in images:
            class imgfromxml:
                number = image.find('number')
                name = image.find('name')
                hash_full = image.find('hash_full')
                hash_resized = image.find('hash_resized')
                description = image.find('description')
                logphoto = image.find('logphoto')
            xmlimglist.append(imgfromxml)
        xmltaglist=list()
        query_xmltaglist='//tag'
        for element in tree.xpath(query_xmltaglist):
            xmltaglist.append(element.text)
        

    return topic,logtext,filepath,photosetname,phototitle,xmlimglist,xmltaglist		

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
    pg_user,pg_passwd,flickrapi_key,flickrapi_secret,wteapi_key=getcredentials('/root/poab/credentials.ini')
    print 'basepath: '+basepath
    for xmlfile in os.listdir(basepath):
        if xmlfile.lower().endswith('.xml'):
            print 'xmlfile: '+xmlfile
            if parsexml(basepath,xmlfile) == 'true':
                print xmlfile+' has already been parsed'
            else:
                topic,logtext,filepath,photosetname,phototitle,xmlimglist,xmltaglist=parsexml(basepath,xmlfile)
			       # topic - topic of the log-entry
			       # logtext - content-text of the log-entry
			       # filepath - where are the files belonging to this xml-file situated 
			       # photosetname - name of the set for flickr
			       # phototitle - title of the photos for flickr
			       # xmlimglist - list of the images in the xml
			       # xmltaglist - list of the images in the xml
            imagepath_fullsize=filepath+'images/best/'
            imagepath_smallsize=filepath+'images/best_990/'
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
            database=db_functions.initdatabase(pg_user,pg_passwd)
    
            #USE "database"-CLASS in the following functions
            tz_detail=geo_functions.get_timezone(trackpath,wteapi_key,database)
            infomarker_id=geo_functions.gpx2database(trackpath,wteapi_key,database,tz_detail)
            #geo_functions.geotag(imagepath_fullsize,imagepath_smallsize,trackpath)
            #imglist=image_functions.img2flickr(imagepath,xmlimglist,xmltaglist,photosetname,phototitle,flickrapi_key,flickrapi_secret,infomarker_id,database)
#Session,db_trackpoint,db_imageinfo,db_image2tag,db_phototag,db_photosets)
    #		  print imglist
    #		  log_detail=log_functions.log2db(topic,logtext,imglist,infomarker_id,Session,db_log)
    #		  print 'image_functions'
    #		  image_functions.logid2images(log_detail,imglist,Session,db_imageinfo)
    #		  finishxml(xmlfile)		

main(basepath)
print 'DONE'
