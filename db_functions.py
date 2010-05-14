# coding=utf-8

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy import types
from sqlalchemy import ForeignKey
import datetime

def now():
    return datetime.datetime.now()


def initdatabase(pg_user,pg_passwd):
    engine = sa.create_engine('postgres://' + pg_user + ':' + pg_passwd + '@localhost/poab_dev')

    meta = sa.MetaData()

    ####### LOG ########

    log_table = sa.Table("log", meta,
        sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
        sa.Column("infomarker_id", types.Integer, ForeignKey('trackpoint.id')),
        sa.Column("topic", types.UnicodeText),
        sa.Column("content", types.UnicodeText),
        sa.Column("createdate", types.TIMESTAMP(timezone=False),default=now()),
        )

    class log(object):
        def __str(self):
            return self.title

        def __init__(self,infomarker_id,topic,content,createdate):
            self.infomarker_id = infomarker_id
            self.topic = topic
            self.content = content
            self.createdate = createdate

        def __repr__(self):
            return "<log('%s','%s','%s','%s',)>" % (self.infomarker_id,self.topic,self.content,self.createdate)


    ####### COMMENT ########

    comment_table = sa.Table("comments", meta,
        sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
        sa.Column("log_id", types.Integer, ForeignKey('log.id')),
        sa.Column("alias", types.VARCHAR(128)),
        sa.Column("date", types.TIMESTAMP(timezone=False)),
        sa.Column("email", types.VARCHAR(128)),
        sa.Column("region", types.UnicodeText),
        sa.Column("comment", types.UnicodeText),
        )

    class comments(object):
        def __str(self):
            return self.title

        def __init__(self,log_id,alias,date,email,region,comment):
            self.log_id = log_id
            self.alias = alias
            self.date = date
            self.email = email
            self.region = region
            self.comment = comment

        def __repr__(self):
            return "<comments('%s','%s','%s','%s','%s','%s')>" % (self.log_id,self.alias,self.date,self.email,self.region,self.comment)


    ####### CONTINENT ########

    continent_table = sa.Table("continent", meta,
        sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
        sa.Column("name",types.VARCHAR(128))
        )

    class continent(object):
        def __str(self):
            return self.title

        def __init__(self,name):
            self.name = name

        def __repr__(self):
            return "<continent('%s')>" % (self.name)


    ####### COUNTRY ########

    country_table = sa.Table("country", meta,
        sa.Column("iso_numcode", types.Integer, primary_key=True),
        sa.Column("continent_id", types.Integer, ForeignKey('continent.id')),
        sa.Column("iso_countryname",types.VARCHAR(128)),
        sa.Column("iso3_nationalcode",types.VARCHAR(3)),
        sa.Column("flickr_countryname",types.VARCHAR(128))
        )

    class country(object):
        def __init__(self,iso_numcode,continent_id,iso_countryname,iso3_nationalcode,flickr_countryname):
            self.iso_numcode = iso_numcode
            self.continent_id = continent_id
            self.iso_countryname = iso_countryname
            self.iso3_nationalcode = iso3_nationalcode
            self.flickr_countryname = flickr_countryname

        def __repr__(self):
            return "<country_table('%s','%s','%s','%s','%s')" % (self.iso_numcode,self.continent_id,self.iso_countryname,self.iso3_nationalcode,self.flickr_countryname)


        def __str(self):
            return self.title


    ####### PHOTOSET ########

    photoset_table = sa.Table("photosets", meta,
        sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
        sa.Column("flickrsetid", types.VARCHAR(256)),
        sa.Column("flickrowner", types.VARCHAR(256)),
        sa.Column("flickrprimary", types.VARCHAR(256)),
        sa.Column("flickrphotocount", types.Integer),
        sa.Column("flickrtitle", types.VARCHAR(256)),
        sa.Column("flickrdescription", types.UnicodeText),
        )

    class photosets(object):
        def __str(self):
            return self.title

        def __init__(self,flickrsetid,flickrowner,flickrprimary,flickrphotocount,flickrtitle,flickrdescription):
            self.flickrsetid = flickrsetid
            self.flickrowner = flickrowner
            self.flickrprimary = flickrprimary
            self.flickrphotocount = flickrphotocount
            self.flickrtitle = flickrtitle
            self.flickrdescription = flickrdescription

        def __repr__(self):
            return "<photosets('%s','%s','%s','%s','%s','%s')>" % (self.flickrsetid,self.flickrowner,self.flickrprimary,self.flickrphotocount,self.flickrtitle,self.flickrdescription)


    ####### IMAGEINFO ########

    imageinfo_table = sa.Table("imageinfo", meta,
        sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
        sa.Column("log_id", types.Integer, ForeignKey('log.id')),
        sa.Column("photoset_id", types.Integer, ForeignKey('photosets.id')),
        sa.Column("infomarker_id", types.Integer, ForeignKey('trackpoint.id')),
        sa.Column("trackpoint_id", types.Integer, ForeignKey('trackpoint.id')),
        sa.Column("flickrfarm", types.VARCHAR(256)),
        sa.Column("flickrserver", types.VARCHAR(256)),
        sa.Column("flickrphotoid", types.VARCHAR(256)),
        sa.Column("flickrsecret", types.VARCHAR(256)),
        sa.Column("flickrdatetaken", types.TIMESTAMP(timezone=False)),
        sa.Column("flickrtitle", types.VARCHAR(256)),
        sa.Column("flickrdescription", types.UnicodeText),
        sa.Column("photohash", types.VARCHAR(256)),
        sa.Column("photohash_990", types.VARCHAR(256)),
        sa.Column("imgname", types.VARCHAR(64)),
        sa.Column("aperture", types.VARCHAR(8)),
        sa.Column("shutter", types.VARCHAR(64)),
        sa.Column("focal_length", types.VARCHAR(64)),
        sa.Column("iso", types.VARCHAR(8)),
        sa.Column("online", types.Boolean, default=False),
        sa.Column("fullsize_online", types.Boolean, default=False),
        )

    class imageinfo(object):
        def __str(self):
            return self.title

        def __init__(self,log_id,photoset_id,infomarker_id,trackpoint_id,flickrfarm,flickrserver,flickrphotoid,flickrsecret,flickrdatetaken,flickrtitle,flickrdescription,photohash,photohash_990,imgname,aperture,shutter,focal_length,iso,online,fullsize_online):
            self.log_id = log_id
            self.photoset_id = photoset_id
            self.infomarker_id = infomarker_id
            self.trackpoint_id = trackpoint_id
            self.flickrfarm = flickrfarm
            self.flickrserver = flickrserver
            self.flickrphotoid = flickrphotoid
            self.flickrsecret = flickrsecret
            self.flickrdatetaken = flickrdatetaken
            self.flickrtitle = flickrtitle
            self.flickrdescription = flickrdescription
            self.photohash = photohash
            self.photohash_990 = photohash_990
            self.imgname = imgname
            self.aperture = aperture
            self.shutter = shutter
            self.focal_length = focal_length
            self.iso = iso
            self.online = online
            self.fullsize_online = fullsize_online

        def __repr__(self):
            return "<imageinfo('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (self.log_id,self.photoset_id,self.infomarker_id,self.trackpoint_id,self.flickrfarm,self.flickrserver,self.flickrphotoid,self.flickrsecret,self.flickrdatetaken,self.flickrtitle,self.flickrdescription,self.photohash,self.photohash_990,self.imgname,self.aperture,self.shutter,self.focal_length,self.iso,self.online,self.fullsize_online)


    ####### TRACK ########

    track_table = sa.Table("track", meta,
        sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
        sa.Column("date", types.TIMESTAMP(timezone=False)),
        sa.Column("trkptnum", types.Integer),
        sa.Column("distance", types.Numeric(11,4)),
        sa.Column("timespan", types.DateTime),
	     sa.Column("gencpoly_pts", types.UnicodeText),
	     sa.Column("gencpoly_levels", types.UnicodeText),
        sa.Column("color", types.CHAR(6), default='FF0000'),
        )
    class track(object):
        def __str(self):
            return self.title

        def __init__(self,date,trkptnum,distance,timespan,gencpoly_pts,gencpoly_levels,color):
            self.date = date
	    self.trkptnum = trkptnum
            self.distance = distance
            self.timespan = timespan
	    self.gencpoly_pts = gencpoly_pts
	    self.gencpoly_levels = gencpoly_levels
	    self.color = color

        def __repr__(self):
            return "<track('%s','%s','%s','%s','%s','%s')>" % (self.date,self.distance,self.timespan,self.gencpoly_pts,self.gencpoly_levels,self.color)


    ####### TRACKPOINT ########

    trackpoint_table = sa.Table("trackpoint", meta,
        sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
        sa.Column("track_id", types.Integer, ForeignKey('track.id')),
        sa.Column("timezone_id", types.Integer, ForeignKey('timezone.id')),
        sa.Column("country_id", types.Integer, ForeignKey('country.iso_numcode')),
        sa.Column("latitude", types.Numeric(9,7)),
        sa.Column("longitude", types.Numeric(10,7)),
        sa.Column("altitude", types.Integer),
        sa.Column("velocity", types.Integer),
        sa.Column("temperature", types.Integer),
        sa.Column("direction", types.Integer),
        sa.Column("pressure", types.Integer),
        sa.Column("timestamp", types.TIMESTAMP(timezone=False)),
        sa.Column("infomarker", types.Boolean, default=False),
        sa.Column("location", types.VARCHAR(256)),
        )

    class trackpoint(object):
        def __str(self):
            return self.title

        def __init__(self,track_id,timezone_id,country_id,latitude,longitude,altitude,velocity,temperature,direction,pressure,timestamp,infomarker,location):
            self.track_id = track_id
            self.timezone_id = timezone_id
            self.country_id = country_id
            self.latitude = latitude
            self.longitude = longitude
            self.altitude = altitude
            self.velocity = velocity
            self.temperature = temperature
            self.direction = direction
            self.pressure = pressure
            self.timestamp = timestamp
            self.infomarker = infomarker
            self.location = location

        def __repr__(self):
            return "<trackpoint('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (self.track_id,self.timezone_id,self.country_id,self.latitude,self.longitude,self.altitude,self.velocity,self.temperature,self.direction,self.pressure,self.timestamp, self.infomarker, self.location)


    ####### TIMEZONE ########

    timezone_table = sa.Table("timezone", meta,
        sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
        sa.Column("utcoffset", types.Interval),
        sa.Column("abbreviation", types.VARCHAR(256)),
        sa.Column("description", types.VARCHAR(256)),
        sa.Column("region", types.VARCHAR(256)),
        )

    class timezone(object):
        def __str(self):
           return self.title

        def __init__(self,utcoffset,abbreviation,description,region):
            self.utcoffset = utcoffset
            self.abbreviation = abbreviation
            self.description = description
            self.region = region


        def __repr__(self):
            return "<timezone('%s','%s','%s','%s')>" % (self.utcoffset,self.abbreviation,self.description,self.region)


    ####### IMAGE2TAG ########

    image2tag_table = sa.Table("image2tag", meta,
        sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
        sa.Column("imageinfo_id", types.Integer, ForeignKey('imageinfo.id')),
        sa.Column("phototag_id", types.Integer, ForeignKey('phototag.id')),
        )

    class image2tag(object):
        def __str(self):
           return self.title

        def __init__(self,imageinfo_id,phototag_id):
            self.imageinfo_id = imageinfo_id
            self.phototag_id = phototag_id


        def __repr__(self):
            return "<image2tag('%s','%s')>" % (self.imageinfo_id,self.phototag_id)


    ####### PHOTOTAG ########

    phototag_table = sa.Table("phototag", meta,
        sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
        sa.Column("tag", types.VARCHAR(256)),
        sa.Column("flickrtagid", types.VARCHAR(256)),
        )

    class phototag(object):
        def __str(self):
           return self.title

        def __init__(self,tag,flickrtagid):
            self.tag = tag
            self.flickrtagid = flickrtagid


        def __repr__(self):
            return "<phototag('%s','%s')>" % (self.tag,self.flickrtagid)






    orm.mapper(log, log_table,
        order_by=[log_table.c.id.desc()])

    orm.mapper(comments, comment_table,
        order_by=[comment_table.c.id.desc()])

    orm.mapper(continent, continent_table,
        order_by=[continent_table.c.id.desc()])

    orm.mapper(country, country_table,
        order_by=[country_table.c.iso_numcode.desc()])

    orm.mapper(photosets, photoset_table,
        order_by=[photoset_table.c.id.desc()])

    orm.mapper(imageinfo, imageinfo_table,
        order_by=[imageinfo_table.c.id.desc()])
 
    orm.mapper(track, track_table,
        order_by=[track_table.c.id.desc()])

    orm.mapper(trackpoint, trackpoint_table,
        order_by=[trackpoint_table.c.id.desc()])

    orm.mapper(timezone, timezone_table,
        order_by=[timezone_table.c.id.desc()])

    orm.mapper(image2tag, image2tag_table,
        order_by=[image2tag_table.c.id.desc()])

    orm.mapper(phototag, phototag_table,
        order_by=[phototag_table.c.id.desc()])



    Session=orm.sessionmaker(bind=engine)
    class database:
        db_session=Session
        db_log=log
        db_comments=comments
        db_continent=continent
        db_country=country
        db_photosets=photosets
        db_imageinfo=imageinfo
        db_track=track
        db_trackpoint=trackpoint
        db_timezone=timezone
        db_image2tag=image2tag
        db_phototag=phototag
#    return Session,log,comments,continent,country,photosets,imageinfo,track,trackpoint,timezone,image2tag,phototag
    return database


