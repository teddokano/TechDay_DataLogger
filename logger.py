#!/usr/bin/env python3

import http.server
import socketserver
import urllib.request
import json
from urllib.parse import urlparse
from urllib.parse import parse_qs
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler
from http.cookies import SimpleCookie

import	os

PORT = 8000

page_template_path		= "page_template/main_page.html"
error404_template_path	= "page_template/404.html"
image_file_folder		= "img"
default_image			= "default.png"
verbose					= False

with open( page_template_path, "r" ) as f:
	html_source 	= f.read()					

with open( error404_template_path, "r" ) as f:
	html404_source 	= f.read()					

visitors	= {}

class Visitor:
	def __init__( self, id ):
		self.visitor_id	= id
		self.job_type	= { "" }
		self.product	= { "" }
		self.visit_demo	= {}

	def visit( self, demo_id, data ):
		self.visit_demo	= { demo_id, data }
		
class Demo:
	def __init__( self, demo_id ):
		self.demo_id	= demo_id
		self.chance		= 0
		self.interest	= 0
		self.options	= 0
		self.actions	= []
		self.memo		= ""

	def visit( self, demo_id, data ):
		self.visit_demo	= { demo_id, data }

class ExampleHandler( BaseHTTPRequestHandler ):
	def do_GET( self ):
	
		cookies = SimpleCookie( self.headers.get( "Cookie" ) )
		parsed	= urlparse( self.path )
		query	= parse_qs( parsed.query )

		if ( verbose ):
			print( f"parsed = {parsed}" )
			print( f"parsed.path = {parsed.path}" )
			print( f"query = {query}" )
		
		###
		### normal file handling
		###
		
		if "/.command" not in parsed.path:
			file_path	= parsed.path[ 1: ]
			
			if not os.path.isfile( file_path ):
				self.send_response( 404 )
				self.send_header( "Content-Type", "text/html" )
				self.end_headers()
				self.wfile.write( html404_source.encode("utf-8") )
			else:
				try:
					content_type = {ext_content[ os.path.splitext( parsed.path )[ 1 ][ 1: ] ]}
				except KeyError:
					content_type  = "text/html"

				with open( file_path, "rb" ) as f:
					data 	= f.read()					

				print( f"ext_content = {ext_content[ os.path.splitext( parsed.path )[ 1 ][ 1: ] ]}" )
		
				self.send_response(200)
				self.send_header( "Content-Type", content_type )
				self.end_headers()
			
				self.wfile.write( data )

		###
		### command handling
		###
		
		else:
			if "/.command_action" in parsed.path:
				try:
					tag_id	= cookies['tag_id'].value
					tag_id  = query[ "tag" ][0]
				except KeyError:
					tag_id  = 9999

				try:
					demo_id	= cookies['demo_id'].value
					demo_id  = query[ "demo" ][0]
				except KeyError:
					demo_id  = "demo10"

				cookies['tag_id' ]	= tag_id
				cookies['demo_id']	= demo_id

				cookie_expire_seconds	= 3600 * 24 * 3
				cookies[ "tag_id"  ][ "max-age" ] = cookie_expire_seconds
				cookies[ "demo_id" ][ "max-age" ] = cookie_expire_seconds

				self.send_response(200)
				self.send_header( "Set-Cookie", f"tag_id={tag_id};   path=/" )
				self.send_header( "Set-Cookie", f"demo_id={demo_id}; path=/" )

				self.send_header( "Content-Type", "text/html" )
				self.end_headers()
				
				h	= html_source.replace( '===TAG_ID===', str( tag_id ) )
				h	= h.replace( '===DEMO_LIST===', demo_list( demo_id, 18 ) )

				img_folder_path	= f"{image_file_folder}"

				image_file	= f"{img_folder_path}/{tag_id}.jpg"
				
				if not os.path.isfile( image_file ):
					image_file	= f"{img_folder_path}/{default_image}"
					
				h	= h.replace( '===IMAGE_FILE===', image_file )
				self.wfile.write( h.encode("utf-8") )
				
				
				if ( tag_id not in visitors.keys() ):
					print( "=== New visitor" )
					visitors[ tag_id ]	= Visitor( tag_id )
					
				print( visitors )

				print( f"json.dumps = {json.dumps( visitors[ tag_id ].visit_demo )}" )

				
			elif "/.command_vers" in parsed.path:
				tag_id	= query[ "tag"  ][0]
				demo_id	= query[ "demo" ][0]
		
				self.send_response(200)
				self.send_header( "Content-Type", "text/html" )
				self.end_headers()
				
				h	= json.dumps( visitors[ tag_id ][ demo_id ] )
				self.wfile.write( h.encode("utf-8") )
				print( " $$$$$$$$$$$$$$$$$$$$$$$$$$$$ vars" )
				print( f"{h}" )


def demo_list( selected, length ):
	str_list    = []
	
	for i in range( 1, length ):
		id	= f"demo{i}"
		if selected == id:
			sel	= "selected"
		else:
			sel	= ""
    		
		str_list   += [ f'<option value= "{id}" {sel}>Demo {i}</option>' ]

	return "\n".join( str_list )


def main():
	with socketserver.TCPServer(("", PORT), ExampleHandler) as httpd:		
		print("serving at port", PORT)
		httpd.serve_forever()


ext_content	= {	"css" : "text/css",
				"html": "text/html",
				"js"  : "text/javascript",
				"png" : "image/png",
				"jpg" : "image/jpg",
				"ico" : "image/ico",
				}	

if __name__ == "__main__":
	main()
