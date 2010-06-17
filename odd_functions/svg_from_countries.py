import sys
sys.path.append('/root/poab')
from lxml import etree
from xml.etree import ElementTree
import glineenc
from sqlalchemy import and_, or_
import ConfigParser
import db_functions
import os

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

def parsesvg(database,svgfile,svgpath):
    session=database.db_session()
    db_country=database.db_country
    db_country_polygons=database.db_country_polygons
    print svgpath,svgfile
    if svgfile.lower().endswith('.svg'):
        try:
            tree = etree.fromstring(file(svgpath+svgfile, "r").read())
            query_points='//@points'
            query_ids='//@id'
            i=0
            pointlist=tree.xpath(query_points)
            isocode=int(tree.xpath('//@id')[1].split('-')[1])
            i=0
            print isocode
            try:
                q = session.query(db_country).filter(db_country.iso_numcode==isocode)
                cindb=q.one()
                print cindb.iso_countryname
                for points in pointlist:
                    points=str(points)
                    i=i+1
                    q = session.query(db_country_polygons).filter(and_(db_country_polygons.country_id==isocode,db_country_polygons.polygon==points,db_country_polygons.solo==True))
                    print q.count()
                    if q.count()>1:
                        country_polygon=q.one()
                        print country_polygon.id,country_shape.iso_numcode
                    else:
                        print isocode
                        session.add(db_country_polygons(isocode,points,True,True))
                        session.commit()
            except:
                print 'Error:'+str(isocode)
                print 'Country not found in db:'+str(isocode)
        except:
                print 'Error:'+str(svgfile)
                print 'No data in file:'+str(svgfile)
        

if __name__ == "__main__":
    pg_user,pg_passwd,flickrapi_key,flickrapi_secret,wteapi_key=getcredentials('/root/poab/credentials.ini')
    database=db_functions.initdatabase(pg_user,pg_passwd)
    svgpath='/root/poab/odd_functions/countries/'
    for svgfile in os.listdir(svgpath):
        print svgfile
        parsesvg(database,svgfile,svgpath)
