# coding=utf-8
import flickrapi
from lxml import etree
import ConfigParser
import sys

credentialfile='/root/poab/credentials.ini'
config=ConfigParser.ConfigParser()
open(credentialfile)
config.read(credentialfile)
api_key=config.get("flickrcredentials","api_key")
api_secret=config.get("flickrcredentials","api_secret")


flickr = flickrapi.FlickrAPI(api_key, api_secret, format='etree')


def imgupload(filename,title,description,tags):
    try:
        # coding=utf-8
        if tags:
            pass
        else:
            if description==None:
                description=''
            tags=''
            result=flickr.upload(filename=filename,title=title,description=description,tags=tags)
            #result_xml=etree.fromstring(result.xml)
            #query_photoid='//photoid'
            #photoid=etree.tostring(result_xml.xpath(query_photoid)[0]).split(">")[1].split("<")[0]
            photoid=result.find('photoid').text
            return photoid
    except flickrapi.FlickrError, (value):     
 	     sys.stderr.write("%s\n" % (value, ))
	     sys.exit(1)                         

def imgreplace(filename,photo_id):
    try:
        # coding=utf-8
        result=flickr.replace(filename=filename,photo_id=photo_id)
        result_xml=etree.fromstring(result.xml)
        query_photoid='//photoid'
        photoid=etree.tostring(result_xml.xpath(query_photoid)[0]).split(">")[1].split("<")[0]
        return photoid
    except flickrapi.FlickrError, (value):     
 	sys.stderr.write("%s\n" % (value, ))
	sys.exit(1)                         

def create_photoset(photosetname,description,photoid):
    try:
        # coding=utf-8
        result=flickr.photosets_create(title=photosetname,description=description,primary_photo_id=photoid)
        photosetid=result.find('photoset').attrib['id']
        return photosetid
    except flickrapi.FlickrError, (value):     
 	sys.stderr.write("%s\n" % (value, ))
	sys.exit(1)                         
 
def get_photosetinfo(photoset_id):
    try:
        photosetinfo=flickr.photosets_getInfo(photoset_id=photoset_id)
        owner=photosetinfo.find('photoset').attrib['owner']
        primary=photosetinfo.find('photoset').attrib['primary']
        count=photosetinfo.find('photoset').attrib['photos']
        title=photosetinfo.find('photoset/title').text
        description=photosetinfo.find('photoset/description').text
        return owner,primary,count,title,description
    except flickrapi.FlickrError, (value):     
 	sys.stderr.write("%s\n" % (value, ))
	sys.exit(1)                         

def get_photosetphotos(photoset_id):
    try:
        photoset=flickr.photosets_getPhotos(photoset_id=photoset_id)
        photolist=list()
        for photo in photoset.find('photoset'):
            class photodetails:
                title=photo.attrib['title']
                farm=photo.attrib['farm']
                server=photo.attrib['server']
                photoid=photo.attrib['id']
                secret=photo.attrib['secret']
                isprimary=photo.attrib['isprimary']
            photolist.append(photodetails)
        return photolist
    except flickrapi.FlickrError, (value):
        sys.stderr.write("%s\n" % (value, ))
        sys.exit(1)

def photoset_addphoto(photoset_id,photoid):
    try:
        result=flickr.photosets_addPhoto(photoset_id=photoset_id,photo_id=photoid)
	return result
    except flickrapi.FlickrError, (value):     
 	sys.stderr.write("%s\n" % (value, ))
	sys.exit(1)                         


def addtags(photoid,tags):
    try:
	result=flickr.photos_addTags(photo_id=photoid,tags=tags)
	return result
    except flickrapi.FlickrError, (value):
        sys.stderr.write("%s\n" % (value, ))
        sys.exit(1)

def getimginfo(photoid):
    try:
        photoinfo=flickr.photos_getInfo(photo_id=photoid)
        secret=photoinfo.find('photo').attrib['secret']
        originalsecret=photoinfo.find('photo').attrib['originalsecret']
        server=photoinfo.find('photo').attrib['server']
        farm=photoinfo.find('photo').attrib['farm']
        views=photoinfo.find('photo').attrib['views']
        dateuploaded=photoinfo.find('photo').attrib['dateuploaded']
        originalformat=photoinfo.find('photo').attrib['originalformat']
        title=photoinfo.find('photo/title').text
        description=photoinfo.find('photo/description').text
        date_taken=photoinfo.find('photo/dates').attrib['taken']
        tags=list()
        for tag in photoinfo.find('photo/tags'):
	   tags.append((tag.attrib['id'],tag.attrib['author'],tag.attrib['raw']))
        url=photoinfo.find('photo/urls/url').text 
	return(farm,server,photoid,secret,originalsecret,originalformat,date_taken,tags,url,title,description)
    except flickrapi.FlickrError, (value):
	sys.stderr.write("%s\n" % (value, ))
	sys.exit(1)
	

def getexif(photoid,secret):
    try:
        photoexif=flickr.photos_getExif(photo_id=photoid,secret=secret)
        exifdata=dict()
        for exif in photoexif.find('photo'):
            try:
                exifdata[exif.attrib['label']+'_raw']=exif.find('raw').text
            except:
                continue
            try:
                exifdata[exif.attrib['label']+'_clean']=exif.find('clean').text
            except:
                continue
        return exifdata
    except flickrapi.FlickrError, (value):
        sys.stderr.write("%s\n" % (value, ))
        sys.exit(1)
        


def setlocation(photoid,lat,lon,accuracy):
    try:
        success=flickr.photos_geo_setLocation(photo_id=photoid,lat=lat,lon=lon,accuracy=accuracy)
	return success
    except flickrapi.FlickrError, (value):     
 	sys.stderr.write("%s\n" % (value, ))
	sys.exit(1)                         

def removelocation(photoid):
    try:
	success=flickr.photos_geo_removeLocation(photo_id=photoid)
	return success
    except flickrapi.FlickrError, (value):     
 	sys.stderr.write("%s\n" % (value, ))
	sys.exit(1)                         


def findplace(lat,lon,accuracy):
    try:
        place=flickr.places_findByLatLon(lat=lat,lon=lon,accuracy=accuracy)
        try:
            name=place.find('places/place').attrib['name']
            return name
        except AttributeError:
            return None
    except flickrapi.FlickrError, (value):
        sys.stderr.write("%s\n" % (value, ))
        sys.exit(1)

#url_square='http://farm%s.static.flickr.com/%s/%s_%s_s.%s' % (farm,server,photoid,secret,originalformat)
#url_thumb='http://farm%s.static.flickr.com/%s/%s_%s_t.%s' % (farm,server,photoid,secret,originalformat)
#url_small='http://farm%s.static.flickr.com/%s/%s_%s_m.%s' % (farm,server,photoid,secret,originalformat)
#url_medium='http://farm%s.static.flickr.com/%s/%s_%s.%s' % (farm,server,photoid,secret,originalformat)
#url_large='http://farm%s.static.flickr.com/%s/%s_%s_b.%s' % (farm,server,photoid,secret,originalformat)
#url_original='http://farm%s.static.flickr.com/%s/%s_%s_o.%s' % (farm,server,photoid,originalsecret,originalformat)
#photopage='http://www.flickr.com/photos/peletiah/' + photoid

