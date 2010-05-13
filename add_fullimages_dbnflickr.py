# checks for newly uploaded "big-size" images, adds to db and flickr and links to corresponding ids
# replaces 990px-images on flickr with full-size

import talk2flickr
import db_functions
from sqlalchemy import and_
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

#def checkimgindb(imagepath,image,database):
    

def roundup_imagepath(database):
    for path in os.listdir('/srv/trackdata/bydate/'):
        if os.path.isdir(path) == True:
            imagepath='/srv/trackdata/bydate/'+path+'/images/sorted/'
            print 'current directory is '+path
            filetypes=('.png','.jpg','.jpeg','.gif','.tif')
            if not os.path.isdir(imagepath+'tmp'):
                os.makedirs(imagepath+'tmp')
            for image in sortedlistdir(imagepath):
                if image.lower().endswith(filetypes):
                    imghash_full=hashlib.sha256(open(imagepath+image).read()).hexdigest()
                    imghash_resized=resize_990(imagepath,imagepath+'tmp/',image)
                    print image+' full: '+imghash_full
                    print image+' 990px: '+imghash_resized
                    #imageinfo=checkimgindb(imagepath,image,database)


if __name__ == "__main__":
    pg_user,pg_passwd,flickrapi_key,flickrapi_secret,wteapi_key=getcredentials('credentials.ini')
    database=db_functions.initdatabase(pg_user,pg_passwd)
    roundup_imagepath(database)
     
