#this function fetches additional information for the LAST trackpoint of a track(Needed for the track mainly)

from sqlalchemy import and_, or_,desc,asc
import hashlib
import ConfigParser
import urllib
import os
import hashlib
import sys
sys.path.append('/root/poab')
from image_functions import sortedlistdir as sortedlistdir,tags2flickrndb as tags2flickrndb
from geo_functions import get_country as get_country,get_timezone as get_timezone
from fill_photos_db import resize_990 as resize_990
import talk2flickr
import db_functions
from getfromxml import parsexml as parsexml,getcredentials as getcredentials

if __name__ == "__main__":
    pg_user,pg_passwd,flickrapi_key,flickrapi_secret,wteapi_key=getcredentials('/root/poab/credentials.ini')
    database=db_functions.initdatabase(pg_user,pg_passwd)
    session=database.db_session()
    db_track=database.db_track
    db_trackpoint=database.db_trackpoint
    q=session.query(db_track)
    for track in q.all():
        q=session.query(db_trackpoint).filter(db_trackpoint.track_id==track.id).order_by(asc(db_trackpoint.timestamp))
        trackpoint=q.first()
        print trackpoint.id
        location=talk2flickr.findplace(trackpoint.latitude,trackpoint.longitude,8)
        if trackpoint.location==None:
            trackpoint.location=location
            session.commit()
        else:
            print trackpoint.location
            trackpoint.location=location
            session.commit()
