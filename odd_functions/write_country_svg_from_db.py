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

def writesvg(database):
    
    session=database.db_session()
    db_country=database.db_country
    db_trackpoint=database.db_trackpoint
    q = session.query(db_country).filter(or_(db_country.continent_id==1,db_country.continent_id==2,db_country.continent_id==3))
    #q = session.query(db_country).filter(db_country.iso_numcode==643)
    db_country_polygons=database.db_country_polygons
    for country in q.all():
        svgdata='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.0//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
<svg height="250" width="370" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">\n
\n<g id="background">
<rect id="" width="370" height="250" fill="#222222"/>
</g>\n'''
        country_visited=False
        #print country.iso_countryname,country.iso_numcode
        q = session.query(db_trackpoint).filter(db_trackpoint.country_id==country.iso_numcode)
        svgdata=svgdata+'''  <g id="'''+str(country.iso_numcode)+'''" style="stroke-miterlimit: 3; fill: #F1F1F1; stroke: #000000; stroke-opacity: 1; stroke-width: 0.05; stroke-linejoin: bevel; stroke-linecap: square">\n'''
        q = session.query(db_country_polygons).filter(and_(db_country_polygons.country_id==country.iso_numcode,db_country_polygons.active==True, db_country_polygons.solo==True))
        i=1
        #negative offset values to move max in x and y direction
        x_offset=0
        y_offset=0
        x_min=1000
        y_min=1000
        x_max=0
        y_max=0
        x_svg=370
        y_svg=250
        scale=2.5
        for polygon in q.all():
            polygon_new=''''''
            pointlist=polygon.polygon.split(" ")
            for point in pointlist:
                if len(point)>0:
                    x=point.split(",")[0]
                    x_int=int(x.split(".")[0])
                    if x_int<x_min:
                        x_min=x_int
                    if x_int>x_max:
                        x_max=x_int
                    y=point.split(",")[1]
                    y_int=int(y.split(".")[0])
                    if y_int<y_min:
                        y_min=y_int
                    if y_int>y_max:
                        y_max=y_int
            x_max_min_diff=x_max-x_min
            x_c_middle=x_min+x_max_min_diff/2
            x_svg_middle=x_svg/2
            x_offset=x_svg_middle-x_c_middle 
            y_max_min_diff=y_max-y_min
            y_c_middle=y_min+y_max_min_diff/2
            y_svg_middle=y_svg/2
            y_offset=y_svg_middle-y_c_middle            
        
        for polygon in q.all():
            #x_offset=0
            #y_offset=0
            polygon_new=''''''
            pointlist=polygon.polygon.split(" ")
            for point in pointlist:
                if country.iso_numcode==710:
                    print x_max,y_max
                    print x_min,y_min
                    print y_offset
                    print x_offset
                    #y_offset=-30

                if len(point)>0:
                    x=point.split(",")[0]
                    x_int=int(x.split(".")[0])
                    x_int=(x_int+x_offset)
                    x_new=str(x_int)+'.'+x.split(".")[1]
                    y=point.split(",")[1]
                    y_int=int(y.split(".")[0])
                    y_int=(y_int+y_offset)
                    y_new=str(y_int)+'.'+y.split(".")[1]
                    polygon_new=polygon_new+'''%s,%s ''' % (x_new,y_new)
 
            svgdata=svgdata+'''    <polygon id="%s" points="%s" />\n''' % (country.flickr_countryname,polygon_new)
            i=i+1
        svgdata=svgdata+'''  </g>\n'''
        svgdata=svgdata+'''</svg>'''
        basepath='/root/pylons/poab/poab/public/static/countries/'
        countrysvg=open(basepath+str(country.iso_numcode)+'.svg','w')
        countrysvg.write(svgdata)
        countrysvg.close()
    #print x_min,y_min
    #print x_max,y_max


if __name__ == "__main__":
    pg_user,pg_passwd,flickrapi_key,flickrapi_secret,wteapi_key=getcredentials('/root/poab/credentials.ini')
    database=db_functions.initdatabase(pg_user,pg_passwd)
    writesvg(database)
