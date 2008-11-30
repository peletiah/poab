# coding=utf-8

import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy import types
from sqlalchemy import ForeignKey



def initdatabase(pg_user,pg_passwd):
    engine = sa.create_engine('postgres://' + pg_user + ':' + pg_passwd + '@localhost/poab')

    meta = sa.MetaData()

    ####### BLOG ########

    blog_table = sa.Table("log", meta,
        sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
        sa.Column("marker_id", types.Integer, ForeignKey('infomarkers.id')),
        sa.Column("country_id", types.Integer, ForeignKey('country.iso_nationalcode')),
        sa.Column("topic", types.UnicodeText),
        sa.Column("content", types.UnicodeText),
        sa.Column("createdate", types.TIMESTAMP(timezone=True)),
        )

    class blog(object):
        def __str(self):
            return self.title

        def __init__(self,marker_id,country_id,topic,content,createdate):
            self.marker_id = marker_id
            self.country_id = country_id
            self.topic = topic
            self.content = content
            self.createdate = createdate

        def __repr__(self):
            return "<blog('%s','%s','%s','%s','%s',)>" % (self.marker_id,self.country_id,self.topic,self.content,self.createdate)


    ####### COMMENT ########

    comment_table = sa.Table("comments", meta,
        sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
        sa.Column("log_id", types.Integer, ForeignKey('log.id')),
        sa.Column("alias", types.VARCHAR(128)),
        sa.Column("date", types.TIMESTAMP(timezone=True)),
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
        sa.Column("iso_nationalcode", types.Integer, primary_key=True),
        sa.Column("continent_id", types.Integer, ForeignKey('continent.id')),
        sa.Column("iso_countryname",types.VARCHAR(128))
        )

    class country(object):
        def __init__(self,iso_nationalcode,continent_id,iso_countryname):
            self.iso_nationalcode = iso_nationalcode
            self.continent_id = continent_id
            self.iso_countryname = iso_countryname

        def __repr__(self):
            return "<country_table('%s','%s','%s')>" % (self.iso_nationalcode,self.continent_id,self.iso_countryname)


        def __str(self):
            return self.title


    ####### PHOTOSET ########

    photoset_table = sa.Table("photosets", meta,
        sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
        sa.Column("flickrsetid", types.VARCHAR(256)),
        sa.Column("flickrprimary", types.VARCHAR(256)),
        sa.Column("flickrsecret", types.VARCHAR(256)),
        sa.Column("flickrserver", types.VARCHAR(256)),
        sa.Column("flickrfarm", types.VARCHAR(256)),
        sa.Column("flickrphotocount", types.Integer),
        sa.Column("flickrtitle", types.VARCHAR(256)),
        sa.Column("flickrdescription", types.UnicodeText),
        )

    class photosets(object):
        def __str(self):
            return self.title

        def __init__(self,flickrsetid,flickrprimary,flickrsecret,flickrserver,flickrfarm,flickrphotocount,flickrtitle,flickrdescription):
            self.flickrsetid = flickrsetid
            self.flickrprimary = flickrprimary
            self.flickrsecret = flickrsecret
            self.flickrserver = flickrserver
            self.flickrfarm = flickrfarm
            self.flickrphotocount = flickrphotocount
            self.flickrtitle = flickrtitle
            self.flickrdescription = flickrdescription

        def __repr__(self):
            return "<photosets('%s','%s','%s','%s','%s','%s','%s','%s')>" % (self.flickrsetid,self.flickrprimary,self.flickrsecret,self.flickrserver,self.flickrfarm,self.flickrphotocount,self.flickrtitle,self.flickrdescription)


    ####### IMAGEINFO ########

    imageinfo_table = sa.Table("imageinfo", meta,
        sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
        sa.Column("log_id", types.Integer, ForeignKey('log.id')),
        sa.Column("country_id", types.Integer, ForeignKey('country.iso_nationalcode')),
        sa.Column("infomarker_id", types.Integer, ForeignKey('infomarkers.id')),
        sa.Column("photoset_id", types.Integer, ForeignKey('photosets.id')),
        sa.Column("trackpoint_id", types.Integer, ForeignKey('track.id')),
        sa.Column("flickrfarm", types.VARCHAR(256)),
        sa.Column("flickrserver", types.VARCHAR(256)),
        sa.Column("flickrphotoid", types.VARCHAR(256)),
        sa.Column("flickrsecret", types.VARCHAR(256)),
        sa.Column("flickrdatetaken", types.TIMESTAMP(timezone=True)),
        sa.Column("original_name", types.VARCHAR(256)),
        )

    class imageinfo(object):
        def __str(self):
            return self.title

        def __init__(self,log_id,country_id,infomarker_id,photoset_id,trackpoint_id,flickrfarm,flickrserver,flickrphotoid,flickrsecret,flickrdatetaken,original_name):
            self.log_id = log_id
            self.country_id = country_id
            self.infomarker_id = infomarker_id
            self.photoset_id = photoset_id
            self.trackpoint_id = trackpoint_id
            self.flickrfarm = flickrfarm
            self.flickrserver = flickrserver
            self.flickrphotoid = flickrphotoid
            self.flickrsecret = flickrsecret
            self.flickrdatetaken = flickrdatetaken
            self.original_name = original_name

        def __repr__(self):
            return "<imageinfo('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (self.log_id,self.country_id,self.infomarker_id,self.photoset_id,self.trackpoint_id,self.flickrfarm,self.flickrserver,self.flickrphoto_id,self.flickrsecret,self.flickrdatetaken,self.original_name)


    ####### INFOMARKER ########

    infomarker_table = sa.Table("infomarkers", meta,
        sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
        sa.Column("trackpoint_id", types.Integer, ForeignKey('trackpoint.id')),
        )

    class infomarker(object):
        def __str(self):
            return self.title

        def __init__(self,trackpoint_id):
            self.trackpoint_id = trackpoint_id

        def __repr__(self):
            return "<infomarker('%s')>" % (self.trackpoint_id)


    ####### TRACK ########

    track_table = sa.Table("track", meta,
        sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
        sa.Column("date", types.TIMESTAMP(timezone=True)),
        sa.Column("distance", types.Numeric(8,6)),
        sa.Column("timespan", types.DateTime),
        )
    class track(object):
        def __str(self):
            return self.title

        def __init__(self,date,distance,timespan):
            self.date = date
            self.distance = distance
            self.timespan = timespan

        def __repr__(self):
            return "<track('%s','%s','%s')>" % (self.date,self.distance,self.timespan)


    ####### TRACKPOINT ########

    trackpoint_table = sa.Table("trackpoint", meta,
        sa.Column("id", types.Integer, primary_key=True, autoincrement=True),
        sa.Column("track_id", types.Integer, ForeignKey('track.id')),
        sa.Column("timezone_id", types.Integer, ForeignKey('timezone.id')),
        sa.Column("latitude", types.Numeric(7,7)),
        sa.Column("longitude", types.Numeric(7,7)),
        sa.Column("altitude", types.Integer),
        sa.Column("velocity", types.Integer),
        sa.Column("temperature", types.Integer),
        sa.Column("direction", types.Integer),
        sa.Column("pressure", types.Integer),
        sa.Column("timestamp", types.TIMESTAMP(timezone=True)),
        )

    class trackpoint(object):
        def __str(self):
            return self.title

        def __init__(self,track_id,timezone_id,latitude,longitude,altitude,velocity,temperature,direction,pressure,timestamp):
            self.track_id = track_id
            self.timezone_id = timezone_id
            self.latitude = latitude
            self.longitude = longitude
            self.altitude = altitude
            self.velocity = velocity
            self.temperature = temperature
            self.direction = direction
            self.pressure = pressure
            self.timestamp = timestamp

        def __repr__(self):
            return "<trackpoint('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')>" % (self.track_id,self.timezone_id,self.latitude,self.longitude,self.altitude,self.velocity,self.temperature,self.direction,self.pressure,self.timestamp)


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


    orm.mapper(blog, blog_table,
        order_by=[blog_table.c.id.desc()])

    orm.mapper(comments, comment_table,
        order_by=[comment_table.c.id.desc()])

    orm.mapper(continent, continent_table,
        order_by=[continent_table.c.id.desc()])

    orm.mapper(country, country_table,
        order_by=[country_table.c.iso_nationalcode.desc()])

    orm.mapper(photosets, photoset_table,
        order_by=[photoset_table.c.id.desc()])

    orm.mapper(imageinfo, imageinfo_table,
        order_by=[imageinfo_table.c.id.desc()])
 
    orm.mapper(infomarker, infomarker_table,
        order_by=[infomarker_table.c.id.desc()])

    orm.mapper(track, track_table,
        order_by=[track_table.c.id.desc()])

    orm.mapper(trackpoint, trackpoint_table,
        order_by=[trackpoint_table.c.id.desc()])

    orm.mapper(timezone, timezone_table,
        order_by=[timezone_table.c.id.desc()])


    Session=orm.sessionmaker(bind=engine)
    return Session,blog,comments,continent,country,photosets,imageinfo,infomarker,track,trackpoint,timezone

