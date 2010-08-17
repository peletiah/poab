import feedparser
from time import strftime
import sys
sys.path.append('/root/poab')
import db_functions
from getfromxml import getcredentials as getcredentials
import re
from geo_functions import get_timezone as get_timezone, get_country as get_country
import datetime
import talk2flickr
from sqlalchemy import and_

pg_user,pg_passwd,flickrapi_key,flickrapi_secret,wteapi_key=getcredentials('/root/poab/credentials.ini')
database=db_functions.initdatabase(pg_user,pg_passwd)

feed_url='http://twitter.com/statuses/user_timeline/19782485.rss'
tweets = feedparser.parse(feed_url)
tweet_list=list()
session=database.db_session()
db_log=database.db_log
db_trackpoint=database.db_trackpoint
for tweet in tweets['entries']:
    print strftime("%a, %d %b %Y %H:%M:%S +0000", tweet.updated_parsed)
    date=strftime("%Y-%m-%d %H:%M:%S", tweet.updated_parsed)
    content=tweet['description']
    guid=tweet['guid']
    q = session.query(db_log).filter(db_log.content==content)
    if q.count()>0:
        print 'tweet already in db: '+date,content
    else:
        p=re.compile("(?P<lat>-{0,1}\d{1,5}),(?P<lon>-{0,1}\d{1,6})")
        if p.search(content):
            p_lat=p.search(content).group("lat")
            p_lon=p.search(content).group("lon")
            #we split the regex-match at the last two digits and insert a colon
            lat=p_lat[:-3]+"."+p_lat[-3:]
            lon=p_lon[:-3]+"."+p_lon[-3:]
            country=get_country(lat,lon,database)
            location=talk2flickr.findplace(lat,lon,11)
            print lat,lon,country.iso_numcode,location
            q = session.query(db_trackpoint).filter(and_(db_trackpoint.latitude==lat,db_trackpoint.longitude==lon,db_trackpoint.timestamp==date))
            if q.count()>0:
                print 'Trackpoint already exists: '+str(q.one().id)
            else:
                tz_detail=get_timezone(database,lat,lon,datetime.datetime.strptime(date,'%Y-%m-%d %H:%M:%S'),wteapi_key)
                session.add(db_trackpoint(None,tz_detail.id,country.iso_numcode,lat,lon,None,None,None,None,None,date,True,location))
                session.commit()
            if q.count() == 1:
                trackpoint=q.one()
                content=content.replace('derreisende: ','')
                content=content.replace(p_lat+','+p_lon,'<a rel="map_colorbox" href="/track/simple/'+str(trackpoint.id)+'" target="_blank">'+lat+', '+lon+'</a>')
                q = session.query(db_log).filter(db_log.content==content)
                if q.count()>0:
                    print 'tweet already in db: '+date,content
                else:
                    session.add(db_log(trackpoint.id,guid,content,date))
                    session.commit()
            else:
                print str(q.count())+' entries found for '+str(lat)+','+str(lon)+','+str(date)
        else:
            #session.add(db_log(114791,title,content.replace('derreisende: ',''),date))
            #session.commit()
            print 'non geotagged entries not written to db'
