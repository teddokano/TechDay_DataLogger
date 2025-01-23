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


html_source = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechDay Data Logger</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
        }
        header {
            background-color: #007BFF;
            color: white;
            padding: 1rem;
            text-align: center;
        }
        main {
            padding: 2rem;
        }
        section {
            background-color: white;
            margin-bottom: 1rem;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        h2 {
            color: #333;
        }
        form {
            display: flex;
            flex-direction: column;
        }
        label {
            margin-bottom: 0.5rem;
            color: #555;
        }
        input, select, button {
            padding: 0.5rem;
            margin-bottom: 1rem;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button {
            background-color: #007BFF;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        footer {
            background-color: #007BFF;
            color: white;
            padding: 1rem;
            text-align: center;
            position: fixed;
            width: 100%;
            bottom: 0;
        }

    </style>
</head>
<body>
    <header>
        <h4>The TechDay Data Logger</h4>
    </header>
    <main>
        <section id="selection-menu">
            <h2>Tag ID: ===TAG_ID===</h2>
        </section>
        <section id="selection-menu">
			ポップアップメニューを選択し，必要があればテキスト入力欄を埋めて「送信」してください. 
        </section>
        <section id="text-entry">





            <form id="data-form">
                <label for="demo">Select a demo:</label>
                <select id="options" name="demo">
                    ===DEMO_LIST===
                </select>

                <label for="tag">TAG:</label>
                <input id="tag" name="tag" type="number" value="===TAG_ID===" readonly />

                <label for="options">Choose an option:</label>
                <select id="options" name="options">
                    <option value="option1">Option 1</option>
                    <option value="option2">Option 2</option>
                    <option value="option3">Option 3</option>
                </select>
                <label for="data-input">Enter text data:</label>
                <input type="text" id="data-input" name="data-input" required>
                <button type="submit">送信</button>
            </form>
        </section>
        <section id="data-display">
			Something to add
        </section>
    </main>
    <footer>
        <p>2025 Tsukimidai Communication Syndicate - Crawl Design</p>
    </footer>

</body>
</html>
"""

PORT = 8000

class ExampleHandler( BaseHTTPRequestHandler ):
	def do_GET( self ):
	
		cookies = SimpleCookie( self.headers.get( "Cookie" ) )
		parsed	= urlparse( self.path )
		query	= parse_qs( parsed.query )

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

		self.send_response(200)
		self.send_header( "Set-Cookie", f"tag_id={tag_id};   path=/" )
		self.send_header( "Set-Cookie", f"demo_id={demo_id}; path=/" )
		'''
		C = SimpleCookie()
		C[ "tag_id"  ] = tag_id
		C[ "demo_id" ] = demo_id
		self.send_header( C )
		'''
		self.send_header( "Content-Type", "text/html" )
		self.end_headers()
		
		h	= html_source.replace( '===TAG_ID===', str( tag_id ) )
		h	= h.replace( '===DEMO_LIST===', demo_list( demo_id, 18 ) )
		self.wfile.write( h.encode("utf-8") )

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



with socketserver.TCPServer(("", PORT), ExampleHandler) as httpd:
	cookie_expire_seconds	= 3600 * 24 * 3
	C = SimpleCookie()
	C[ "tag_id"  ] = 9876
	C[ "demo_id" ] = "demo99"
	C[ "tag_id"  ][ "max-age" ] = cookie_expire_seconds
	C[ "demo_id" ][ "max-age" ] = cookie_expire_seconds
	print( C )
		
	print("serving at port", PORT)
	httpd.serve_forever()


	
