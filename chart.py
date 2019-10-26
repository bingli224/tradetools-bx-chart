
## By BingLi224
##
## BTC/THB Chart
##
## Requested public data from bx.in.th,
## save the cache to local json file,
## show in the chart with EMAs and volume.
##

import urllib.request
import datetime
from datetime import date
import json
from operator import itemgetter

url_daily = 'https://bx.in.th/api/tradehistory/?pairing=1&date={:s}'

days = 600

def get_candlestick ( day ) :
	data = json.loads ( urllib.request.urlopen (
		urllib.request.Request (
			url_daily.format ( day ),
			headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36' }
		)
	).read ( ) )

	if 'success' in data :
		return data [ 'data' ]
	else :
		return None

def update_candlestick ( ) :
	print ( '.' )
	if candlesticks [ -1 ] [ 'date' ] == datetime.date.today ( ) :
		## get current candlestick
		data = get_candlestick ( day )
		if data is not None :
			## update to the candlestick list
			candlesticks.remove ( len ( candlesticks ) )
			candlesticks.append ( data )

			## update the UI chart
			draw_chart ( candlesticks [ len ( candlesticks ) - n_candlesticks + 1 : len ( candlesticks ) ] )

	if root is not None :
		root.after ( 5000, lambda : update_candlestick ( ) )

def draw_chart ( candlesticks ) :
	## draw the chart

	height = int ( c.cget( 'height' ) )

	n_candlesticks = len ( candlesticks )

	## get highest and lowest
	low = min ( candlesticks, key=itemgetter ('low') ) [ 'low' ]
	high = max ( candlesticks, key=itemgetter ('high') ) [ 'high' ]

	max_vol = max ( candlesticks, key=itemgetter ('volume') ) ['volume']

	print ( "################################################################################" )
	print ( "low={:f}\thigh={:f}".format ( low, high ) )

	#for idx in range ( len ( candlesticks ) - 1 ) :
	for idx in range ( n_candlesticks ) :
		## for each candlesticks..

		"""
		print (
				'{:f}\t{:f}\t{:f}\t{:f}'.format (
				candlesticks [ idx ] [ 'low' ],
				( candlesticks [ idx ] [ 'low' ] - low ) / ( high - low ),
				( candlesticks [ idx ] [ 'low' ] - low ) / ( high - low ) * height,
				( -candlesticks [ idx ] [ 'low' ] + high ) / ( high - low ) * height,
				#( candlesticks [ idx ] [ 'high' ] - low ) / ( high - low ) * 500,
			)
		)
		"""

		## vol
		c.create_line (
			idx * w_candlestick,
			height - ( ( max_vol - candlesticks [ idx ] [ 'volume' ] ) / max_vol ) * height * .2,
			idx * w_candlestick,
			height,
			tags = ( 'vol' ),
			fill='#ffffff',
			width=3
		)

		## candlestick color
		clr = '#33cc33'
		if candlesticks [ idx ] [ 'open' ] > candlesticks [ idx ] [ 'close' ] :
			clr = '#cc3333'

		## EMAs
		if idx > 0 :
			c.create_line (
				( idx - 1 ) * w_candlestick,
				( .10 + ( -candlesticks [ idx-1 ] [ 'EMA5' ] + high ) / ( high - low ) * .60 ) * height,
				idx * w_candlestick,
				( .10 + ( -candlesticks [ idx ] [ 'EMA5' ] + high ) / ( high - low ) * .60 ) * height,
				tags=( 'ema', 'ema5' ),
				fill='#cc00cc',
				width=1,
				smooth=1
			)
			c.create_line (
				( idx - 1 ) * w_candlestick,
				( .10 + ( -candlesticks [ idx-1 ] [ 'EMA10' ] + high ) / ( high - low ) * .60 ) * height,
				idx * w_candlestick,
				( .10 + ( -candlesticks [ idx ] [ 'EMA10' ] + high ) / ( high - low ) * .60 ) * height,
				tags=( 'ema', 'ema10' ),
				fill='#aa00aa',
				width=1,
				smooth=1
			)
			c.create_line (
				( idx - 1 ) * w_candlestick,
				( .10 + ( -candlesticks [ idx-1 ] [ 'EMA25' ] + high ) / ( high - low ) * .60 ) * height,
				idx * w_candlestick,
				( .10 + ( -candlesticks [ idx ] [ 'EMA25' ] + high ) / ( high - low ) * .60 ) * height,
				tags=( 'ema', 'ema25' ),
				fill='#880088',
				width=1,
				smooth=1
			)
			c.create_line (
				( idx - 1 ) * w_candlestick,
				( .10 + ( -candlesticks [ idx-1 ] [ 'EMA75' ] + high ) / ( high - low ) * .60 ) * height,
				idx * w_candlestick,
				( .10 + ( -candlesticks [ idx ] [ 'EMA75' ] + high ) / ( high - low ) * .60 ) * height,
				tags=( 'ema', 'ema75' ),
				fill='#660066',
				width=2,
				smooth=1
			)
			c.create_line (
				( idx - 1 ) * w_candlestick,
				( .10 + ( -candlesticks [ idx-1 ] [ 'EMA200' ] + high ) / ( high - low ) * .60 ) * height,
				idx * w_candlestick,
				( .10 + ( -candlesticks [ idx ] [ 'EMA200' ] + high ) / ( high - low ) * .60 ) * height,
				tags=( 'ema', 'ema200' ),
				fill='#330033',
				width=2,
				smooth=1
			)

		## shadow
		c.create_line (
			idx * w_candlestick,
			( .10 + ( -candlesticks [ idx ] [ 'low' ] + high ) / ( high - low ) * .60 ) * height,
			idx * w_candlestick,
			( .10 + ( -candlesticks [ idx ] [ 'high' ] + high ) / ( high - low ) * .60 ) * height,
			tags='candlestick',
			fill=clr,
			width=1
		)
		
		## body
		c.create_line (
			#idx * w_candlestick - w_candlestick / 2,
			idx * w_candlestick,
			( .10 + ( -candlesticks [ idx ] [ 'open' ] + high ) / ( high - low ) * .60 ) * height,
			#idx * w_candlestick - w_candlestick / 2,
			idx * w_candlestick,
			( .10 + ( -candlesticks [ idx ] [ 'close' ] + high ) / ( high - low ) * .60 ) * height,
			tags='candlestick',
			fill=clr,
			width=3
		)

def line_start ( event ) :
	global x_last, y_last

	## remember first point
	x_last = c.canvasx ( event.x )
	y_last = c.canvasy ( event.y )
	
def line_prev ( event ) :
	global x_last, y_last
	if x_last is None :
		x_last = c.canvasx ( event.x )
	if y_last is None :
		y_last = c.canvasy ( event.y )

	c.delete ( 'line_prev' )

	## calc line
	x = c.canvasx ( event.x )
	y = c.canvasx ( event.y )
	if x != x_last :
		slope = ( y - y_last ) / ( x - x_last )
		intercept = y - slope * x

		w = int ( c.cget( 'width' ) )

		## recreate preview line
		c.create_line (
			0, intercept,
			w, intercept + slope * w,
			tags='line_prev',
			fill='#99ccee'
		)

def line_stop ( event ) :
	global x_last, y_last
	if x_last is None :
		x_last = c.canvasx ( event.x )
	if y_last is None :
		y_last = c.canvasy ( event.y )

	## remove preview line
	c.delete ( 'line_prev' )

	## calc line
	x = c.canvasx ( event.x )
	y = c.canvasx ( event.y )
	if x != x_last :
		slope = ( y - y_last ) / ( x - x_last )
		intercept = y - slope * x

		w = int ( c.cget( 'width' ) )

		## recreate preview line
		c.create_line (
			0, intercept,
			w, intercept + slope * w,
			tags='line',
			fill='#99ccee'
		)

	x_last = y_last = None

def line_vertical ( event ) :
	x = c.canvasx ( event.x )

	c.delete ( 'line_vert' )

	c.create_line (
		x, 0,
		x, height,
		tags='line_vert',
		fill='#999999'
	)

def line_delete ( event ) :
	## delete clicked line
	x = c.canvasx ( event.x )
	y = c.canvasx ( event.y )
	for id in c.find_closest ( x, y, halo=2 ) :
		if 'line' in c.gettags ( id ) :
			c.delete ( id )

################################################################################

candlesticks = []

## load the saved data
with open ( 'btc_thb.json', 'r' ) as fl :
	candlesticks.extend ( json.load ( fl ) )

b_updated = None

## today
tday = datetime.date.today ( ).toordinal ( )

#dict_candlesticks = sorted ( candlesticks, key=itemgetter ( 'date' ) )
dict_candlesticks = {}
#for d in sorted ( candlesticks, key=itemgetter ( 'date' ) ) :
for d in candlesticks :
	dict_candlesticks [ d [ 'date' ] ] = d

for day in range ( days, 0, -1 ) :

	day = date.fromordinal ( tday - day ).strftime ( '%d-%m-%Y' )

	data = None

	## check if already known
	#for d in candlesticks :
	#	print ( d [ 'date' ] + ' vs ' + day )
	#	if d [ 'date' ] == day :
	#		## found
	#		data = d
	#		break
	if day in dict_candlesticks :
		data = dict_candlesticks [ day ]

	## if no requested data, request from web server
	if data is None or day == datetime.date.today ( ) :
		## get daily close
		#print ( url_daily.format ( str ( date.fromordinal ( d - day ).strftime ( '%d-%m-%Y' ) ) ) )
		#data = json.loads ( urllib.request.urlopen (
		#	urllib.request.Request (
		#		url_daily.format ( day ),
		#		headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36' }
		#	)
		#).read ( ) )

		data = get_candlestick ( day )

		b_updated = 1
		print ( '+' )

		#if 'success' in data :
		if data is not None :
			## remember the date
			data [ 'date' ] = day

			## convert str data to float
			data [ 'close' ] = float ( data [ 'close' ] )
			data [ 'low' ] = float ( data [ 'low' ] )
			data [ 'high' ] = float ( data [ 'high' ] )
			data [ 'open' ] = float ( data [ 'open' ] )
			data [ 'avg' ] = float ( data [ 'avg' ] )
			data [ 'volume' ] = float ( data [ 'volume' ] )

			## remember the new data
			candlesticks.append ( data )

	## if got data, check EMAs
	if data is not None and 'close' in data :
		## check EMAs

		print ( data [ 'close' ] )

		if 'EMA5' not in data :
			b_updated = 1

			## calculate EMAs
			if len ( candlesticks ) < 2 :
				## first data
				data [ 'EMA5' ] = float ( data [ 'close' ] )
				data [ 'EMA10' ] = float ( data [ 'close' ] )
				data [ 'EMA25' ] = float ( data [ 'close' ] )
				data [ 'EMA75' ] = float ( data [ 'close' ] )
				data [ 'EMA200' ] = float ( data [ 'close' ] )
			else :
				yesterday = candlesticks [ -2 ]
				data [ 'EMA5' ] = float ( data [ 'close' ] ) * ( 2 / 6 ) + ( yesterday [ 'EMA5' ] * ( 1 - 2 / 6 ) )
				data [ 'EMA10' ] = float ( data [ 'close' ] ) * ( 2 / 11 ) + ( yesterday [ 'EMA10' ] * ( 1 - 2 / 11 ) )
				data [ 'EMA25' ] = float ( data [ 'close' ] ) * ( 2 / 26 ) + ( yesterday [ 'EMA25' ] * ( 1 - 2 / 26 ) )
				data [ 'EMA75' ] = float ( data [ 'close' ] ) * ( 2 / 76 ) + ( yesterday [ 'EMA75' ] * ( 1 - 2 / 76 ) )
				data [ 'EMA200' ] = float ( data [ 'close' ] ) * ( 2 / 201 ) + ( yesterday [ 'EMA200' ] * ( 1 - 2 / 201 ) )

	## sort the data by date
	#candlesticks = sorted ( candlesticks, key=itemgetter ( 'date' )

#fl = open ( 'btc_thb.json', 'w' )
if b_updated :
	## save the updated data
	with open ( 'btc_thb.json', 'w' ) as fl :
		json.dump ( candlesticks, fl )

################################################################################

import tkinter as tk
from tkinter import *
#from tkinter import ttk

root = Tk ( )

n_candlesticks = 150
w_candlestick = 5
width = n_candlesticks * ( w_candlestick )
height = 500
pair_id = 1

c = tk.Canvas (
	bg = '#000000',
	width = width,
	height = height
)

x_last = None
y_last = None


c.pack ( side='top', fill='both', expand=1 )

c.bind ( '<Shift-B1-ButtonPress>', line_start )
c.bind ( '<Shift-B1-Motion>', line_prev )
c.bind ( '<Shift-B1-ButtonRelease>', line_stop )
c.bind ( '<Control-Shift-1>', line_delete )
c.bind ( '<1>', line_vertical )

root.title ( "bx.in.th" )

draw_chart ( candlesticks [ len ( candlesticks ) - n_candlesticks + 1 : len ( candlesticks ) ] )

root.after ( 5000, lambda : update_candlestick ( ) )

root.mainloop ( )
