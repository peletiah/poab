# checks for newly uploaded "big-size" images, adds to db and flickr and links to corresponding ids
# replaces 990px-images on flickr with full-size

import talk2flickr
import db_functions
from sqlalchemy import and_, or_
import hashlib
import ConfigParser
import urllib
import os
import hashlib
from image_functions import sortedlistdir as sortedlistdir
from fill_photos_db import resize_990 as resize_990

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

def checkimgindb(fullpath,image,imghash_full,imghash_resized,database):
    session=database.db_session()
    db_imageinfo=database.db_imageinfo
    q = session.query(db_imageinfo).filter(or_(db_imageinfo.photohash==imghash_full,db_imageinfo.photohash_990==imghash_resized))
    if q.count() == 0:
        print image+': Image not found in db, adding to db and flickr'
        
        
    else:
        for imageinfo in q.all():
            print image+': '+str(imageinfo.id)
    
    

def roundup_images(database):
    for path in os.listdir('/srv/trackdata/bydate/'):
        if os.path.isdir('/srv/trackdata/bydate/'+path) == True:
            fullpath='/srv/trackdata/bydate/'+path+'/images/sorted/'
            resizepath='/srv/trackdata/bydate/'+path+'/images/sorted/'
            print 'current directory is '+fullpath
            filetypes=('.png','.jpg','.jpeg','.gif','.tif')
            for image in sortedlistdir(fullpath):
                if image.lower().endswith(filetypes):
                    imghash_full=hashlib.sha256(open(fullpath+image).read()).hexdigest()
                    imghash_resized=hashlib.sha256(open(resizepath+image).read()).hexdigest()
#                    print image+' full: '+imghash_full
#                    print image+' 990px: '+imghash_resized
                    imageinfo=checkimgindb(fullpath,image,imghash_full,imghash_resized,database)


if __name__ == "__main__":
    pg_user,pg_passwd,flickrapi_key,flickrapi_secret,wteapi_key=getcredentials('credentials.ini')
    database=db_functions.initdatabase(pg_user,pg_passwd)
    roundup_images(database)
     
