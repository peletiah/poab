import talk2flickr
from optparse import OptionParser
import db_functions
from sqlalchemy import and_
import hashlib
import ConfigParser
import urllib
import os
import hashlib

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

pg_user,pg_passwd,flickrapi_key,flickrapi_secret,wteapi_key=getcredentials('credentials.ini')
database=db_functions.initdatabase(pg_user,pg_passwd)
session=database.db_session()
db_imageinfo=database.db_imageinfo
q=session.query(db_imageinfo).filter(db_imageinfo.flickrphotoid!=None)
for imageinfo in q.all():
    imageexif=talk2flickr.getexif(imageinfo.flickrphotoid,imageinfo.flickrsecret)
    imageinfo.aperture=imageexif['Aperture_clean']
    imageinfo.shutter=imageexif['Exposure_clean']
    imageinfo.focal_length=imageexif['Focal Length_clean']
    imageinfo.iso=imageexif['ISO Speed_raw']
    print imageinfo.flickrtitle
    print 'id:'+str(imageinfo.id)
    print 'aperture:'+imageinfo.aperture
    print 'shutter:'+imageinfo.shutter
    print 'focal length:'+imageinfo.focal_length
    print 'ISO Speed:'+ imageinfo.iso
    print 'http://www.flickr.com/peletiah/'+imageinfo.flickrphotoid   
    session.commit()

