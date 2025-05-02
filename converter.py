#!/usr/bin/env python3

import	os
import	pickle

access_log_folder	= "access_log/"

class Access:
    def __init__( self, query, time, ip_addr ):
        self.query		= query
        self.time		= time
        self.ip_addr	= ip_addr

files		= os.listdir( access_log_folder )
log_files	= [ f for f in files if f.endswith( ".log" ) == True ]

logs		= []

for f in log_files:
	try:
		print( f"opening file: {access_log_folder + f}", end = "" )
		with open( access_log_folder + f, "rb" ) as file:
			logs.append( pickle.load( file ) )
			print( "loaded" )

	except:
		print( "fail" )
		pass

print( "logs are loaded" )

for i in logs:
    print( i.time, end = " " )
    print( i.ip_addr, end = " " )
    print( i.query )

print( "done" )
