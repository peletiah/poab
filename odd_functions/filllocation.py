import sys
sys.path.append('/root/poab')
import talk2flickr
from optparse import OptionParser
import db_functions
from sqlalchemy import and_
import hashlib
import ConfigParser
import urllib
import os
import hashlib
import time

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

#if __name__ == "__main__":
#        pg_user,pg_passwd,flickrapi_key,flickrapi_secret,wteapi_key=getcredentials('/home/peletiah/poab/credentials.ini')
#        database=db_functions.initdatabase(pg_user,pg_passwd)
#        session=database.db_session()
#        db_imageinfo=database.db_imageinfo
#        infomarkerlist=list()
#        q=session.query(db_imageinfo).filter(db_imageinfo.infomarker_id!=None)
#        for line in q.all():
#            if line.infomarker_id in infomarkerlist:
#                pass
#            else:
#                infomarkerlist.append(line.infomarker_id)
#
#        db_log=database.db_log
#        q=session.query(db_log).filter(db_log.infomarker_id!=None)
#        for line in q.all():
#            print line.infomarker_id
#            if line.infomarker_id in infomarkerlist:
#                pass
#            else:
#                infomarkerlist.append(line.infomarker_id)
#
#    
pg_user,pg_passwd,flickrapi_key,flickrapi_secret,wteapi_key=getcredentials('/root/poab/credentials.ini')
database=db_functions.initdatabase(pg_user,pg_passwd)
session=database.db_session()

db_trackpoint=database.db_trackpoint
q=session.query(db_trackpoint).filter(db_trackpoint.location!=None)
for line in q.all():
    print line.id,line.timestamp
    print 'old:'+line.location
    location=talk2flickr.findplace(line.latitude,line.longitude,16)
    print 'new:'+location+'\n'
#    time.sleep(1)
    line.location=location
    session.commit()
