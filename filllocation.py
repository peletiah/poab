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

if __name__ == "__main__":
        pg_user,pg_passwd,flickrapi_key,flickrapi_secret,wteapi_key=getcredentials('/home/peletiah/poab/credentials.ini')
        Session,db_log,db_comments,db_continent,db_country,db_photosets,db_imageinfo,db_track,db_trackpoint,db_timezone,db_image2tag,db_phototag=db_functions.initdatabase(pg_user,pg_passwd)
        session=Session()
        infomarkerlist=list()
        q=session.query(db_imageinfo).filter(db_imageinfo.infomarker_id!=None)
        for line in q.all():
            if line.infomarker_id in infomarkerlist:
                pass
            else:
                infomarkerlist.append(line.infomarker_id)

        q=session.query(db_log).filter(db_log.infomarker_id!=None)
        for line in q.all():
            print line.infomarker_id
            if line.infomarker_id in infomarkerlist:
                pass
            else:
                infomarkerlist.append(line.infomarker_id)

    
        for infomarkerid in infomarkerlist:
            q=session.query(db_trackpoint).filter(db_trackpoint.id==infomarkerid)
            for line in q.all():
                location=talk2flickr.findplace(line.latitude,line.longitude,8)
                line.location=location
                session.commit()
