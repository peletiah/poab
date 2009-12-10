import flickrapi
from lxml import etree
import ConfigParser
import sys

credentialfile='credentials.ini'
config=ConfigParser.ConfigParser()
open(credentialfile)
config.read('credentials.ini')
api_key=config.get("flickrcredentials","api_key")
api_secret=config.get("flickrcredentials","api_secret")


flickr = flickrapi.FlickrAPI(api_key, api_secret, format='etree')

flickr.web_login_url('delete')

