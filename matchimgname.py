import hashlib
from sqlalchemy import and_
from sqlalchemy import update
import db_functions #custom
import os
import ConfigParser

config=ConfigParser.ConfigParser()
open('credentials.ini')
config.read('credentials.ini')
pg_user=config.get("postgresql","username")
pg_passwd=config.get("postgresql","password")

database=db_functions.initdatabase(pg_user,pg_passwd)

imagepath_full="/srv/trackdata/bydate/2009-12-12/images/best/"
imagepath_resized="/srv/trackdata/bydate/2009-12-12/images/best_990/"

def sortedlistdir(imagepath, cmpfunc=cmp):
    l = os.listdir(imagepath)
    l.sort(cmpfunc)
    return l

for image in sortedlistdir(imagepath_full):
    print 'imagename='+image
    photohash_full=hashlib.sha256(open(imagepath_full+image).read()).hexdigest()
    photohash_resized=hashlib.sha256(open(imagepath_resized+image).read()).hexdigest()
    session=database.db_session()
    db_imageinfo=database.db_imageinfo
    query_imageinfo=session.query(db_imageinfo).filter(db_imageinfo.photohash==photohash_full)
    for column in query_imageinfo.all():
        column.imgname=image
        column.photohash_990=photohash_resized
        session.commit()
    if query_imageinfo.count() == 1:
        print photohash_full + '=\n' + query_imageinfo.one().photohash
