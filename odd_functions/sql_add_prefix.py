from sqlalchemy import and_, or_
import hashlib
import ConfigParser
import urllib
import os
import hashlib
import sys
sys.path.append('/root/poab')
from image_functions import sortedlistdir as sortedlistdir
from fill_photos_db import resize_990 as resize_990
import talk2flickr
import db_functions
from getfromxml import parsexml as parsexml
import time,datetime

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

pg_user,pg_passwd,flickrapi_key,flickrapi_secret,wteapi_key=getcredentials('/root/poab/credentials.ini')
database=db_functions.initdatabase(pg_user,pg_passwd)
session=database.db_session()
db_imageinfo=database.db_imageinfo
db_log=database.db_log
q = session.query(db_imageinfo)
images = q.all()
for image in images:
    q = session.query(db_log).filter(db_log.id==image.log_id)
    log=q.one()
    createdate=log.createdate.strftime('%Y-%m-%d')
    q = session.query(db_imageinfo).filter(db_imageinfo.id==image.id)
    image=q.one()
    if image.imgname[47:51]=='/srv':
        print image.imgname
        print '/trackdata/bydate/'+str(createdate)+'/images/sorted/990/'+image.imgname
        print '/trackdata/bydate/'+str(createdate)+'/images/sorted/990/'+image.imgname[-12:-4]+'.jpg'
        image.imgname='/trackdata/bydate/'+str(createdate)+'/images/sorted/990/'+image.imgname[-12:-4]+'.jpg'
        session.commit()
        session.close()
