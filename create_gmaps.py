import ConfigParser
import time, datetime
from optparse import OptionParser
import db_functions #custom
from sqlalchemy import and_

config=ConfigParser.ConfigParser()
open('/root/scripts/credentials.ini')
config.read('/root/scripts/credentials.ini')
pg_user=config.get("postgresql","username")
pg_passwd=config.get("postgresql","password")

def getpolylines(date,delta):
    Session,db_log,db_comments,db_continent,db_country,db_photosets,db_imageinfo,db_track,db_trackpoint,db_timezone,db_image2tag,db_phototag=db_functions.initdatabase(pg_user,pg_passwd)
    session=Session()
    query_track=session.query(db_track).filter(and_(db_track.date > date, db_track.date < date+delta))
    for detail in query_track.all():
            gencpoly_pts=detail.gencpoly_pts
            gencpoly_levels=detail.gencpoly_levels
    return gencpoly_pts,gencpoly_levels


def writegmapsfile(gencpoly_pts,gencpoly_levels):
    js='''//<![CDATA[

   var map;
   function writegmarker(lng,lat,gallerylink) {
        var marker = new GMarker( new GLatLng(lng,lat) );
                GEvent.addListener(marker, 'click', function(){
                marker.openExtInfoWindow(
                  map,
                  "map_marker",
                  controllerlink(gallerylink),
                  {beakOffset: 3}
                );
              });
        map.addOverlay(marker);
   }

   function readjson() {
        $.getJSON("/json_vienna.js", function(json) {
                for (i=0;i<json.length;i++){
                        line=json[i];
                        writegmarker(line[0],line[1],line[2]);
//                      console.log(line);
                }


        });
   }
   function showGallery(gallerylink) {
        new Ajax.Request(gallerylink, {onSuccess: function(response) { document.getElementById('gallery').innerHTML = response.responseText; }});
        }


   function controllerlink(gallerylink) {
        return '<a href="javascript:showGallery(\\''+gallerylink+'\\')">gallery</a>';
   }
   function load() {
      if (GBrowserIsCompatible()) {
        map = new GMap2(document.getElementById("map"));
        map.setCenter(new GLatLng('47.1421920', '11.5538584'), 13);
        map.setMapType(G_PHYSICAL_MAP);
        map.addControl(new GScaleControl());
        map.addControl(new GLargeMapControl());
        var mapControl = new GHierarchicalMapTypeControl();
        map.addMapType(G_PHYSICAL_MAP);
        mapControl.addRelationship(G_SATELLITE_MAP, G_HYBRID_MAP, "Labels", false);
        map.addControl(mapControl);
        map.addControl(new GOverviewMapControl ());
        map.enableScrollWheelZoom();
        readjson();

var encodedPoints = "''' + gencpoly_pts + '''"
var encodedLevels = "''' + gencpoly_levels + '''"
var encodedPolyline = new GPolyline.fromEncoded({
                color: "#FF0000",
                weight: 5,
                points: encodedPoints,
                levels: encodedLevels,
                zoomFactor: 32,
                numLevels: 4
        });
        map.addOverlay(encodedPolyline);
      }
    }

    //]]>
'''
    gmapsfile=open('/opt/poab/poab/public/js/gmaps.js','w')
    gmapsfile.write(js)
    gmapsfile.close()

if __name__ == "__main__":
    parser = OptionParser()
    #parser.add_option("-h", "--help", action="help")
    parser.add_option("-d", action="append", dest="date",help="date of the track")
    (options, args) = parser.parse_args()
    searchdate=options.date[0]
    time_format = "%Y-%m-%d"
    mytime = time.strptime(searchdate,time_format)
    searchdate=datetime.datetime(*mytime[:6])
    delta = datetime.timedelta(days=1)
    gencpoly_pts,gencpoly_levels=getpolylines(searchdate,delta)
    writegmapsfile(gencpoly_pts,gencpoly_levels)    

