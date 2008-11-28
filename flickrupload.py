# coding=utf-8
import flickrapi
from lxml import etree
import ConfigParser

credentialfile='credentials.ini'
config=ConfigParser.ConfigParser()
open(credentialfile)
config.read('credentials.ini')
api_key=config.get("flickrcredentials","api_key")
api_secret=config.get("flickrcredentials","api_secret")


flickr = flickrapi.FlickrAPI(api_key, api_secret, format='etree')
#filename='/root/flickr_api/kobenzl.jpg'
title='Kobenzl'
description=unicode(u'Berries!')
tags='''"kobenzl" wien herbst'''

def imgupload(filename,title,description,tags):
    # coding=utf-8
    result=flickr.upload(filename=filename,title=title,description=description,tags=tags)
    result_xml=etree.fromstring(result.xml)
    query_photoid='//photoid'
    photoid=etree.tostring(result_xml.xpath(query_photoid)[0]).split(">")[1].split("<")[0]
    return photoid

def getimginfo(photoid):
    photoinfo=flickr.photos_getInfo(photo_id=photoid)
    secret=photoinfo.find('photo').items()[8][1]
    originalsecret=photoinfo.find('photo').items()[0][1]
    server=photoinfo.find('photo').items()[6][1]
    farm=photoinfo.find('photo').items()[4][1]
    views=photoinfo.find('photo').items()[3][1]
    dateuploaded=photoinfo.find('photo').items()[7][1]
    originalformat=photoinfo.find('photo').items()[9][1]
    return(farm,server,photoid,secret,originalformat)


#url_square='http://farm%s.static.flickr.com/%s/%s_%s_s.%s' % (farm,server,photoid,secret,originalformat)
#url_thumb='http://farm%s.static.flickr.com/%s/%s_%s_t.%s' % (farm,server,photoid,secret,originalformat)
#url_small='http://farm%s.static.flickr.com/%s/%s_%s_m.%s' % (farm,server,photoid,secret,originalformat)
#url_medium='http://farm%s.static.flickr.com/%s/%s_%s.%s' % (farm,server,photoid,secret,originalformat)
#url_large='http://farm%s.static.flickr.com/%s/%s_%s_b.%s' % (farm,server,photoid,secret,originalformat)
#url_original='http://farm%s.static.flickr.com/%s/%s_%s_o.%s' % (farm,server,photoid,originalsecret,originalformat)
#photopage='http://www.flickr.com/photos/peletiah/' + photoid

