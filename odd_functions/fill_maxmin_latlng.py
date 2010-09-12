# -*- coding: utf-8 -*-
import sys
sys.path.append('/root/poab')
from lxml import etree
from xml.etree import ElementTree
import glineenc
from sqlalchemy import and_, or_
import ConfigParser
import db_functions
from unidecode import unidecode

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


def getmaxminbounds(database):
    session=database.db_session()
    db_track=database.db_track
    db_trackpoint=database.db_trackpoint
    q = session.query(db_track).filter(or_(db_track.maxlat==None,db_track.minlon==None,db_track.minlat==None,db_track.minlon==None))
    tracks = q.all()
    for track in tracks:
        q = session.query(db_trackpoint).filter(and_(db_trackpoint.track_id==track.id,db_trackpoint.infomarker==True))
        infomarker=q.one()
        maxlat=infomarker.latitude
        maxlon=infomarker.longitude
        minlat=infomarker.latitude
        minlon=infomarker.longitude
        q = session.query(db_trackpoint).filter(db_trackpoint.track_id==track.id)
        trackpoints=q.all()
        for trackpoint in trackpoints:
            if trackpoint.latitude>maxlat:
                maxlat=trackpoint.latitude
            if trackpoint.longitude>maxlon:
                maxlon=trackpoint.longitude
            if trackpoint.latitude<minlat:
                minlat=trackpoint.latitude
            if trackpoint.longitude<minlon:
                minlon=trackpoint.longitude
        print 'track_id: %s infomarker_id: %s maxlat: %s maxlon: %s minlat: %s minlon: %s' % (str(track.id),str(infomarker.id),str(maxlat),str(maxlon),str(minlat),str(minlon))
        track.maxlat=maxlat
        track.maxlon=maxlon
        track.minlat=minlat
        track.minlon=minlon
        session.commit()
            
    

if __name__ == "__main__":
    pg_user,pg_passwd,flickrapi_key,flickrapi_secret,wteapi_key=getcredentials('/root/poab/credentials.ini')
    database=db_functions.initdatabase(pg_user,pg_passwd)
    getmaxminbounds(database)
