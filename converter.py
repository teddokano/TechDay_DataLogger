#!/usr/bin/env python3

import	os
import	pandas as pd
import	openpyxl
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
		with open( access_log_folder + f, "rb" ) as file:
			logs.append( pickle.load( file ) )

	except:
		print( "fail" )
		pass

print( "logs are loaded" )

total_log	= pd.DataFrame()

for i in logs:	
	d	= { "time": i.time, "ip_addr": i.ip_addr }
	d.update( i.query )
	
	total_log	= pd.concat( [total_log, pd.DataFrame( d ) ] )
	
print( "done" )

total_log.to_excel('pandas_to_excel.xlsx', sheet_name='new_sheet_name')
