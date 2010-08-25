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


def parsexml(basepath,xmlfile,parsed):
    tree = etree.parse(basepath+xmlfile)
    root = tree.getroot()
    logs=root.getiterator("log")
    num_img_log=0
    for log in logs:
        try:
            done =  log.find('done').text
            if done == 'true' and parsed==True:
                return True
            elif done == 'true' and parsed==False:
                pass
        except AttributeError:
            if parsed==True:
                return False
            else:
                pass
        print log.find('topic').text
        topic =  log.find('topic').text.replace("&gt;",">").replace("&lt;","<")
        logtext =  log.find('logtext').text.replace("&gt;",">").replace("&lt;","<")
        filepath =  log.find('filepath').text
        print filepath
        photosetname =  log.find('photoset').text
        phototitle =  log.find('phototitle').text
        createdate =  log.find('createdate').text
        try:
            latitude =  log.find('latitude').text
        except:
            latitude = ''
        try:
            longitude =  log.find('longitude').text
        except:
            longitude = ''
        trk_color =  log.find('trk_color').text
        num_img_xml =  int(log.find('num_of_img').text)
        print 'NUMBER OF IMAGES: '+str(num_img_xml)
        createdate = datetime.datetime.strptime(createdate,'%Y-%m-%d %H:%M:%S')
        images = root.getiterator("img")
        xmlimglist=list()
        for image in images:
            try:
                numberinxml=image.find('no').text
            except:
                numberinxml=''
            class imgfromxml:
                number = numberinxml
                name = image.find('name').text
                hash_full = image.find('hash_full').text
                hash_resized = image.find('hash_resized').text
                description = image.find('description').text
                logphoto = image.find('logphoto').text
            xmlimglist.append(imgfromxml)
            if imgfromxml.logphoto == 'True':
                num_img_log=num_img_log+1
        xmltaglist=list()
        query_xmltaglist='//tag'
        for element in tree.xpath(query_xmltaglist):
            xmltaglist.append(element.text)
        

    return topic,logtext,filepath,photosetname,phototitle,num_img_xml,createdate,latitude,longitude,trk_color,xmlimglist,xmltaglist,num_img_log		

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
            if parsexml(basepath,xmlfile,True) == True:
                print xmlfile+' has already been parsed'
            else:
                topic,logtext,filepath,photosetname,phototitle,num_img_xml,createdate,latitude,longitude,trk_color,xmlimglist,xmltaglist,num_img_log=parsexml(basepath,xmlfile,False)
			       # topic - topic of the log-entry
			       # logtext - content-text of the log-entry
			       # filepath - where are the files belonging to this xml-file situated 
			       # photosetname - name of the set for flickr
			       # phototitle - title of the photos for flickr
			       # xmlimglist - list of the images in the xml
			       # xmltaglist - list of the images in the xml
                imagepath_fullsize=filepath+'images/sorted/'
                imagepath_resized=filepath+'images/sorted/990/'
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
    
                infomarker_id=geo_functions.gpx2database(trackpath,wteapi_key,database,trk_color,latitude,longitude,createdate)
                #files listed in xml should be geotagged already, otherwise the hash would not match anymore, image_functions.geotag is useless therefore
                #image_functions.geotag(imagepath_fullsize,imagepath_resized,trackpath)
                hashcheck,upload2flickrpath,fullsize=image_functions.checkimghash(imagepath_fullsize,imagepath_resized,xmlimglist,num_img_xml,num_img_log)
                print 'Fullsize images found:'+str(fullsize)
                if hashcheck > 0:
                    return upload2flickrpath
                image_functions.xmlimglist2db(photosetname,xmlimglist,database)
                xmlimglist_plus_db_details=image_functions.img2flickr(upload2flickrpath,fullsize,imagepath_resized,xmlimglist,xmltaglist,photosetname,phototitle,flickrapi_key,flickrapi_secret,infomarker_id,database)
                geo_functions.add_tz_country_location(xmlimglist_plus_db_details,wteapi_key,infomarker_id,database)
                log_detail=log_functions.log2db(topic,logtext,createdate,xmlimglist_plus_db_details,num_img_xml,infomarker_id,database)
                photoset_id=image_functions.getphotosetid(photosetname,database)
                if photoset_id == 0:
                    return 'Photoset not found!!!!!'
                image_functions.logid2images(log_detail,xmlimglist,photoset_id,infomarker_id,database)
                finishxml(xmlfile)
                infomarker_id=''
    return 'Everything went fine i think'


if __name__ == "__main__":
    finished=main(basepath)
    print finished
    print 'DONE'
