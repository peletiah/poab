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
    svgdata='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.0//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
<svg height="250" width="370" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" onload='Init(evt)'>\n
<script type="text/ecmascript"><![CDATA[
      var SVGDocument = null;
      var SVGRoot = null;
      var SVGViewBox = null;
      var svgns = 'http://www.w3.org/2000/svg';
      var xlinkns = 'http://www.w3.org/1999/xlink';
      var toolTip = null;
      var TrueCoords = null;
      var tipBox = null;
      var tipText = null;
      var tipTitle = null;
      var tipDesc = null;
 
      var lastElement = null;
      var titleText = '';
      var titleDesc = '';
 
      function replaceLink(path)
        {
          parent.modFromSVG(path);
        }
 
      function Init(evt)
      {
         SVGDocument = evt.target.ownerDocument;
         SVGRoot = SVGDocument.documentElement;
         TrueCoords = SVGRoot.createSVGPoint();
 
         toolTip = SVGDocument.getElementById('ToolTip');
         tipBox = SVGDocument.getElementById('tipbox');
         tipText = SVGDocument.getElementById('tipText');
         tipTitle = SVGDocument.getElementById('tipTitle');
         tipDesc = SVGDocument.getElementById('tipDesc');
         //window.status = (TrueCoords);
 
         //create event for object
         SVGRoot.addEventListener('mousemove', ShowTooltip, false);
         SVGRoot.addEventListener('mouseout', HideTooltip, false);
      };
 
 
      function GetTrueCoords(evt)
      {
         // find the current zoom level and pan setting, and adjust the reported
         //    mouse position accordingly
         var newScale = SVGRoot.currentScale;
         var translation = SVGRoot.currentTranslate;
         TrueCoords.x = (evt.clientX - translation.x)/newScale;
         TrueCoords.y = (evt.clientY - translation.y)/newScale;
      };
 
 
      function HideTooltip( evt )
      {
         toolTip.setAttributeNS(null, 'visibility', 'hidden');
      };
 
 
      function ShowTooltip( evt )
      {
         GetTrueCoords( evt );
 
         var tipScale = 1/SVGRoot.currentScale;
         var textWidth = 0;
         var tspanWidth = 0;
         var boxHeight = 20;
 
         tipBox.setAttributeNS(null, 'transform', 'scale(' + tipScale + ',' + tipScale + ')' );
         tipText.setAttributeNS(null, 'transform', 'scale(' + tipScale + ',' + tipScale + ')' );
 
         var titleValue = '';
         var descValue = '';
         var targetElement = evt.target;
         if ( lastElement != targetElement )
         {
            var targetTitle = targetElement.getElementsByTagName('title').item(0);
            if ( targetTitle )
            {
               // if there is a 'title' element, use its contents for the tooltip title
               titleValue = targetTitle.firstChild.nodeValue;
            }
 
            var targetDesc = targetElement.getElementsByTagName('desc').item(0);
            if ( targetDesc )
            {
               // if there is a 'desc' element, use its contents for the tooltip desc
               descValue = targetDesc.firstChild.nodeValue;
 
               if ( '' == titleValue )
               {
                  // if there is no 'title' element, use the contents of the 'desc' element for the tooltip title instead
                  titleValue = descValue;
                  descValue = '';
               }
            }
 
            // if there is still no 'title' element, use the contents of the 'id' attribute for the tooltip title
            if ( '' == titleValue )
            {
               titleValue = targetElement.getAttributeNS(null, 'id');
            }
 
            // selectively assign the tooltip title and desc the proper values,
            //   and hide those which don't have text values
            //
            var titleDisplay = 'none';
            if ( '' != titleValue )
            {
               tipTitle.firstChild.nodeValue = titleValue;
               titleDisplay = 'inline';
            }
            tipTitle.setAttributeNS(null, 'display', titleDisplay );
 
 
            var descDisplay = 'none';
            if ( '' != descValue )
            {
               tipDesc.firstChild.nodeValue = descValue;
               descDisplay = 'inline';
            }
            tipDesc.setAttributeNS(null, 'display', descDisplay );
         }
 
         // if there are tooltip contents to be displayed, adjust the size and position of the box
         if ( '' != titleValue )
         {
            var xPos = TrueCoords.x + (10 * tipScale);
            var yPos = TrueCoords.y + (10 * tipScale);
 
            //return rectangle around text as SVGRect object
            var outline = tipText.getBBox();
            tipBox.setAttributeNS(null, 'width', Number(outline.width) + 10);
            tipBox.setAttributeNS(null, 'height', Number(outline.height) + 2);
 
            // update position
            toolTip.setAttributeNS(null, 'transform', 'translate(' + xPos + ',' + yPos + ')');
            toolTip.setAttributeNS(null, 'visibility', 'visible');
         }
      };
 
   ]]></script>
<script type="text/ecmascript">
    <![CDATA[
    var country;
    function updateCountryColor(country,color) {
                var changeAttr = "fill";
                var newstyle= color
                country.setAttributeNS(null,changeAttr,newstyle);
           }    
    function resetCountryColor(country,color) {
            var changeAttr = "fill";
            var newstyle= color
            country.setAttributeNS(null,changeAttr,newstyle);
           }
]]>
</script>
\n<g id="background">
<rect id="" width="370" height="250" fill="#222222"/>
</g>\n'''
    session=database.db_session()
    db_country=database.db_country
    db_trackpoint=database.db_trackpoint
    q = session.query(db_country).filter(or_(db_country.continent_id==1,db_country.continent_id==2,db_country.continent_id==3))
    #q = session.query(db_country).filter(db_country.iso_numcode==643)
    db_country_polygons=database.db_country_polygons
    for country in q.all():
        country_visited=False
        #print country.iso_countryname,country.iso_numcode
        q = session.query(db_trackpoint).filter(and_(db_trackpoint.country_id==country.iso_numcode,db_trackpoint.infomarker==True))
        if q.count() > 0:
            country_visited=True
            svgdata=svgdata+'''  <g id="%s" onmouseover="updateCountryColor(this,'#00BBF4')" onmouseout="resetCountryColor(this,'#008CB7')" onclick="replaceLink('%s')" style="cursor: pointer; stroke-miterlimit: 3; stroke: #000000; stroke-opacity: 1; stroke-width: 0.05; stroke-linejoin: bevel; stroke-linecap: square" fill="#008CB7">''' % (country.iso_numcode,country.iso_numcode)
        else:
            svgdata=svgdata+'''  <g id="'''+str(country.iso_numcode)+'''" style="stroke-miterlimit: 3; fill: #CFC2BB; stroke: #000000; stroke-opacity: 1; stroke-width: 0.05; stroke-linejoin: bevel; stroke-linecap: square">\n'''
        
        q = session.query(db_country_polygons).filter(and_(db_country_polygons.country_id==country.iso_numcode,db_country_polygons.active==True,db_country_polygons.solo==False))
        i=1
        #negative offset values to move max in x and y direction
        x_offset=580
        y_offset=110
        for polygon in q.all():
            polygon_new=''''''
            if country_visited==True or country_visited==False:
                pointlist=polygon.polygon.split(" ")
                for point in pointlist:
                    if len(point)>0:
                        x=point.split(",")[0]
                        x_int=int(x.split(".")[0])-x_offset
                        x_new=str(x_int)+'.'+x.split(".")[1]
                        y=point.split(",")[1]
                        y_int=int(y.split(".")[0])-y_offset
                        y_new=str(y_int)+'.'+y.split(".")[1]
                        polygon_new=polygon_new+'''%s,%s ''' % (x_new,y_new)
 
                svgdata=svgdata+'''    <polygon id="%s" points="%s" />\n''' % (country.flickr_countryname,polygon_new)
            else:
                svgdata=svgdata+'''    <polygon id="%s" points="%s" />\n''' % (i,polygon_new)
            i=i+1
        svgdata=svgdata+'''  </g>\n'''
    svgdata=svgdata+'''  <g id='ToolTip' opacity='0.6' visibility='hidden' pointer-events='none'>
      <rect id='tipbox' x='0' y='5' width='88' height='5' rx='2' ry='2' fill='#444444' stroke='black'/>
      <text id='tipText' x='5' y='20' font-family='Arial' font-size='12'>
         <tspan id='tipTitle' fill='white' x='5' font-weight='bold'><![CDATA[]]></tspan>
         <tspan id='tipDesc' x='5' dy='15' fill='blue'><![CDATA[]]></tspan>
      </text>
   </g>
</svg>'''
    basepath='/opt/pylons/poab/poab/public/static/'
    #basepath='/root/pylons/poab/poab/public/static/'
    countrysvg=open(basepath+'world.svg','w')
    countrysvg.write(svgdata)
    countrysvg.close()


if __name__ == "__main__":
    pg_user,pg_passwd,flickrapi_key,flickrapi_secret,wteapi_key=getcredentials('/root/poab/credentials.ini')
    database=db_functions.initdatabase(pg_user,pg_passwd)
    writesvg(database)
