#!/usr/bin/env python3

import http.server
import socketserver
import urllib.request
import json
from urllib.parse import urlparse
from urllib.parse import parse_qs

html_source = """
<!DOCTYPE html>
<html lang="ja">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>TechDay Data Logger</title>

</head>
<body>
	<header>
		<h1>Welcome to TechDay Data Logger</h1>
	</header>
	<main>

		<section id="selection-menu">
			<h2>Tag ID</h2>
			<h2>===TAG_ID===</h2>

		</section>


		<section id="selection-menu">
			<h2>Selection Menu</h2>
		</section>


		<section id="text-entry">

			<form id="data-form">
				<label for="tag">TAG:</label>
				<input id="tag" name="tag" type="number" value="===TAG_ID===" readonly />

				<br/>
				<br/>

				<label for="options">Choose an option:</label>
				<select id="options" name="options">
					<option value="option1">Option 1</option>
					<option value="option2">Option 2</option>
					<option value="option3">Option 3</option>
				</select>

				<br/>
				<br/>

				<label for="data-input">Enter text data:</label>
				<input type="text" id="data-input" name="data-input" required><br />
				<button type="submit">送信</button>
			</form>
		</section>

		<section id="data-display">
		</section>

	</main>
	<footer>
		<p>2025 Tsukimidai Communication Syndicate - Crawl Design</p>
	</footer>
</body>
</html>
"""

PORT = 8000

class ExampleHandler( http.server.SimpleHTTPRequestHandler ):
	def do_GET( self ):
		parsed	= urlparse( self.path )
		query	= parse_qs( parsed.query )

		print( parsed )
		print( query )

		try:
			tag_id  = query[ "tag" ][0]
		except KeyError:
			tag_id  = 9999

		self.send_response(200)
		self.send_header("Content-Type", "text/html")
		self.end_headers()
		self.wfile.write( html_source.replace( '===TAG_ID===', str( tag_id ) ).encode("utf-8") )

def serve_rating_page( tag_number ):
	return "<http><title></title><body>{tag_number}</body></http>"

with socketserver.TCPServer(("", PORT), ExampleHandler) as httpd:
	print("serving at port", PORT)
	httpd.serve_forever()


	
