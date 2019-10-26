
## By BingLi224
##
## BTC/THB Chart
##
## Requested public data from bx.in.th,
## save the cache to local json file,
## show in the chart with EMAs and volume.
##
##
################################################################################
## References:
##		canvas resize
##	https://stackoverflow.com/questions/22835289/how-to-get-tkinter-canvas-to-dynamically-resize-to-window-width
##

import urllib.request
import datetime
from datetime import date
import json
from operator import itemgetter

url_daily = 'https://bx.in.th/api/tradehistory/?pairing=1&date={:s}'

tday = datetime.date.today ( ).toordinal ( )

days = 600

#print ( url_daily.format ( str ( date.fromordinal ( d ).strftime ( '%d-%m-%Y' ) ) ) )
candlesticks = []

## load the saved data
with open ( 'btc_thb.json', 'r' ) as fl :
	candlesticks.extend ( json.load ( fl ) )

b_updated = None

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
		data = json.loads ( urllib.request.urlopen (
			urllib.request.Request (
				url_daily.format ( day ),
				headers = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36' }
			)
		).read ( ) )

		b_updated = 1
		print ( '+' )

		if 'success' in data :
			data = data [ 'data' ]

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

n_candlesticks = IntVar ( )
n_candlesticks.set ( 400 )

w_candlestick = 5
w_last = n_candlesticks.get ( ) * ( w_candlestick )
h_last = 800
pair_id = 1

frm = tk.Frame ( )
frm.pack ( )
tk.Label ( frm, text = 'Pair #' ).pack ( side = 'left' )
tk.Entry ( frm, textvariable = pair_id ).pack ( side = 'left' )
tk.Label ( frm, text = 'No. Candlesticks' ).pack ( side = 'left' )
tk.Entry ( frm, textvariable = n_candlesticks ).pack ( side = 'left' )
tk.Button ( frm, text = 'Update', command = lambda :
	#print ( n_candlesticks.get ( ) )
	draw_chart ( candlesticks, offset = -n_candlesticks.get ( ) )
	).pack ( side = 'right' )

c = tk.Canvas (
	bg = '#000000',
	width = w_last,
	height = h_last
)

x_last = None
y_last = None

def draw_chart ( candlesticks, n_candlesticks = 0, offset = -200, e = None ) :
	## reset the chart
	c.delete ( 'all' )

	#global w_last, h_last

	w_last = int ( c.cget( 'width' ) )
	h_last = int ( c.cget( 'height' ) )

	#print ( 'bef {:d} vs {:d}\t{:d} vs {:d}'.format ( w_last, root.winfo_width ( ), h_last, root.winfo_height ( ) ) )
	#if e is not None :
	#	print ( '{:d} vs {:d} vs {:d}\t{:d} vs {:d} vs {:d}'.format ( w_last, e.width, root.winfo_width ( ), h_last, e.height, root.winfo_height ( ) ) )
	#	print ( '{:d} - {:d} = {:d}'.format ( int ( e.width ), w_last, int ( e.width ) - w_last ) )
	#	print ( '{:d} - {:d} = {:d}'.format ( int ( e.height ), h_last, int ( e.height ) - h_last ) )
	#	if int ( e.width ) != w_last or int ( e.height ) != h_last :
	#		print ( '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n' )
	#print ( "bef\tlen={:d}\toffset={:d}\tn={:d}".format ( len ( candlesticks ), offset, n_candlesticks ) )

	if offset < 0 :
		offset = len ( candlesticks ) + offset

	if n_candlesticks == 0 :
		n_candlesticks = len ( candlesticks ) - offset
	
	## get the visible data list
	candlesticks = candlesticks [ offset : offset + n_candlesticks ]

	#print ( "aft\tlen={:d}\toffset={:d}\tn={:d}".format ( len ( candlesticks ), offset, n_candlesticks ) )

	if n_candlesticks <= 0 :
		return

	#print ( len ( candlesticks ), offset, n_candlesticks )

	## calc the scale
	w_candlestick = w_last / ( n_candlesticks + 1 )
	if w_candlestick < 1 :
		w_candlestick = 1

	## get highest and lowest price
	low = min ( candlesticks, key=itemgetter ('low') ) [ 'low' ]
	high = max ( candlesticks, key=itemgetter ('high') ) [ 'high' ]

	## get highest vol
	max_vol = max ( candlesticks, key=itemgetter ('volume') ) ['volume']

	#print ( "################################################################################" )
	##print ( "low={:f}\thigh={:f}".format ( low, high ) )

	## draw the chart

	rsi_gain = 0
	rsi_loss = 0
	rsi_last = None
	rsi_period = 14

	for idx in range ( n_candlesticks ) :
		## for each candlesticks..

		#print ( str ( idx ) + ' ', end = '' )

		"""
		print (
				'{:f}\t{:f}\t{:f}\t{:f}'.format (
				candlesticks [ idx ] [ 'low' ],
				( candlesticks [ idx ] [ 'low' ] - low ) / ( high - low ),
				( candlesticks [ idx ] [ 'low' ] - low ) / ( high - low ) * h_last,
				( -candlesticks [ idx ] [ 'low' ] + high ) / ( high - low ) * h_last,
				#( candlesticks [ idx ] [ 'high' ] - low ) / ( high - low ) * 500,
			)
		)
		"""

		## vol
		c.create_line (
			idx * w_candlestick,
			h_last - ( ( max_vol - candlesticks [ idx ] [ 'volume' ] ) / max_vol ) * h_last * .2,
			idx * w_candlestick,
			h_last,
			tags = ( 'vol' ),
			fill='#ffffff',
			width=3
		)

		## RSI
		if idx < rsi_period and idx > 0 :
			if candlesticks [ idx ] [ 'close' ] > candlesticks [ idx - 1 ] [ 'close' ] :
				rsi_gain += ( candlesticks [ idx ] [ 'close' ] - candlesticks [ idx - 1 ] [ 'close' ] ) / rsi_period
			elif candlesticks [ idx ] [ 'close' ] < candlesticks [ idx - 1 ] [ 'close' ] :
				rsi_loss += ( candlesticks [ idx - 1 ] [ 'close' ] - candlesticks [ idx ] [ 'close' ] ) / rsi_period
		else :
			rsi_gain = ( rsi_gain * ( rsi_period - 1 ) + abs ( candlesticks [ idx - 1 ] [ 'close' ] - candlesticks [ idx ] [ 'close' ] ) ) / rsi_period
			rsi_loss = ( rsi_loss * ( rsi_period - 1 ) + abs ( candlesticks [ idx - 1 ] [ 'close' ] - candlesticks [ idx ] [ 'close' ] ) ) / rsi_period

			if rsi_loss <= 0 :
				rsi_new = 0
			else :
				rsi_new = 1 - 1 / ( rsi_gain / rsi_loss + 1 )

			if rsi_last is not None :
				c.create_line (
					( idx - 1 ) * w_candlestick,
					h_last * .8 - rsi_last * h_last * .2,
					idx * w_candlestick,
					h_last * .8 - rsi_new * h_last * .2,
					#h_last * .8 - ( 1 - 1 / ( 1 + rsi_gain / rsi_loss ) ) * h_last * .2,
					tags = ( 'rsi' ),
					fill='#0000cc',
					width=1
				)

			## remember recent RSI
			rsi_last = rsi_new
			print ( f'rsi={rsi_last}' )

		## candlestick color
		clr = '#33cc33'
		if candlesticks [ idx ] [ 'open' ] > candlesticks [ idx ] [ 'close' ] :
			clr = '#cc3333'

		## EMAs
		if idx > 0 :
			c.create_line (
				( idx - 1 ) * w_candlestick,
				( .10 + ( -candlesticks [ idx-1 ] [ 'EMA5' ] + high ) / ( high - low ) * .60 ) * h_last,
				idx * w_candlestick,
				( .10 + ( -candlesticks [ idx ] [ 'EMA5' ] + high ) / ( high - low ) * .60 ) * h_last,
				tags=( 'ema', 'ema5' ),
				fill='#cc00cc',
				width=1,
				smooth=1
			)
			c.create_line (
				( idx - 1 ) * w_candlestick,
				( .10 + ( -candlesticks [ idx-1 ] [ 'EMA10' ] + high ) / ( high - low ) * .60 ) * h_last,
				idx * w_candlestick,
				( .10 + ( -candlesticks [ idx ] [ 'EMA10' ] + high ) / ( high - low ) * .60 ) * h_last,
				tags=( 'ema', 'ema10' ),
				fill='#aa00aa',
				width=1,
				smooth=1
			)
			c.create_line (
				( idx - 1 ) * w_candlestick,
				( .10 + ( -candlesticks [ idx-1 ] [ 'EMA25' ] + high ) / ( high - low ) * .60 ) * h_last,
				idx * w_candlestick,
				( .10 + ( -candlesticks [ idx ] [ 'EMA25' ] + high ) / ( high - low ) * .60 ) * h_last,
				tags=( 'ema', 'ema25' ),
				fill='#880088',
				width=1,
				smooth=1
			)
			c.create_line (
				( idx - 1 ) * w_candlestick,
				( .10 + ( -candlesticks [ idx-1 ] [ 'EMA75' ] + high ) / ( high - low ) * .60 ) * h_last,
				idx * w_candlestick,
				( .10 + ( -candlesticks [ idx ] [ 'EMA75' ] + high ) / ( high - low ) * .60 ) * h_last,
				tags=( 'ema', 'ema75' ),
				fill='#660066',
				width=2,
				smooth=1
			)
			c.create_line (
				( idx - 1 ) * w_candlestick,
				( .10 + ( -candlesticks [ idx-1 ] [ 'EMA200' ] + high ) / ( high - low ) * .60 ) * h_last,
				idx * w_candlestick,
				( .10 + ( -candlesticks [ idx ] [ 'EMA200' ] + high ) / ( high - low ) * .60 ) * h_last,
				tags=( 'ema', 'ema200' ),
				fill='#330033',
				width=2,
				smooth=1
			)

		## shadow
		c.create_line (
			idx * w_candlestick,
			( .10 + ( -candlesticks [ idx ] [ 'low' ] + high ) / ( high - low ) * .60 ) * h_last,
			idx * w_candlestick,
			( .10 + ( -candlesticks [ idx ] [ 'high' ] + high ) / ( high - low ) * .60 ) * h_last,
			tags='candlestick',
			fill=clr,
			width=1
		)
		
		## body
		c.create_line (
			#idx * w_candlestick - w_candlestick / 2,
			idx * w_candlestick,
			( .10 + ( -candlesticks [ idx ] [ 'open' ] + high ) / ( high - low ) * .60 ) * h_last,
			#idx * w_candlestick - w_candlestick / 2,
			idx * w_candlestick,
			( .10 + ( -candlesticks [ idx ] [ 'close' ] + high ) / ( high - low ) * .60 ) * h_last,
			tags='candlestick',
			fill=clr,
			width=3
		)

	#print ( 'after {:d} vs {:d}\t{:d} vs {:d}'.format ( w_last, root.winfo_width ( ), h_last, root.winfo_height ( ) ) )
	#if e is not None :
	#	print ( '{:d} vs {:d} vs {:d}\t{:d} vs {:d} vs {:d}'.format ( w_last, e.width, root.winfo_width ( ), h_last, e.height, root.winfo_height ( ) ) )
	#	print ( '{:d} - {:d} = {:d}'.format ( int ( e.width ), w_last, int ( e.width ) - w_last ) )
	#	print ( '{:d} - {:d} = {:d}'.format ( int ( e.height ), h_last, int ( e.height ) - h_last ) )
	#	if ( int ( e.width ) != w_last ) or ( int ( e.height ) != h_last ) :
	#		print ( '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n' )

def on_configure ( event ) :
	global w_last, h_last

	print ( 'bef {:d} vs {:d} vs {:d}\t{:d} vs {:d} vs {:d}'.format ( w_last, event.width, root.winfo_width ( ), h_last, event.height, root.winfo_height ( ) ) )
	print ( '{:d} - {:d} = {:d}'.format ( int ( event.width ), w_last, int ( event.width ) - w_last ) )
	print ( '{:d} - {:d} = {:d}'.format ( int ( event.height ), h_last, int ( event.height ) - h_last ) )
	if int ( event.width ) != w_last or int ( event.height ) != h_last :
		print ( '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n' )

	if w_last is None or h_last is None or int ( event.width ) != w_last or int ( event.height ) != h_last :
		#draw_chart ( candlesticks, offset = -n_candlesticks.get ( ) )
		#c.config ( width = event.width, height = event.height )
		c.scale ( 'all', 0, 0,
				#float ( event.width ) / float ( c.cget ( 'width' ) ), float ( event.height ) / float ( c.cget ( 'height' ) )
				float ( event.width ) / w_last,
				float ( event.height ) / h_last
			)
	
	## remember the event size for prevent redundant draw
	w_last = int ( event.width )
	h_last = int ( event.height )

	print ( 'aft {:d} vs {:d} vs {:d}\t{:d} vs {:d} vs {:d}'.format ( w_last, event.width, root.winfo_width ( ), h_last, event.height, root.winfo_height ( ) ) )
	print ( '{:d} - {:d} = {:d}'.format ( int ( event.width ), w_last, int ( event.width ) - w_last ) )
	print ( '{:d} - {:d} = {:d}'.format ( int ( event.height ), h_last, int ( event.height ) - h_last ) )
	if int ( event.width ) != w_last or int ( event.height ) != h_last :
		print ( '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n' )

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
		x, h_last,
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

c.pack ( side='top', fill='both', expand=1 )

c.bind ( '<Shift-B1-ButtonPress>', line_start )
c.bind ( '<Shift-B1-Motion>', line_prev )
c.bind ( '<Shift-B1-ButtonRelease>', line_stop )
c.bind ( '<Control-Shift-1>', line_delete )
c.bind ( '<1>', line_vertical )
c.bind ( '<Configure>', lambda e : 
	print ( 'cv bind\t{:d} vs {:d}', e.width, c.cget ( 'width' ) )
	)
c.bind ( '<Configure>', on_configure )

root.title ( "bx.in.th" )
#root.bind ( '<Configure>', on_configure )
#root.bind ( '<Configure>', lambda e : 
	#print ( n_candlesticks.get ( ) )
	#print ( self.width )
	#print ( '{:d} vs {:d} vs {:d}\t{:d} vs {:d} vs {:d}'.format ( w_last, e.width, root.winfo_width ( ), h_last, e.height, root.winfo_height ( ) ) )
	#print ( type ( e.width ) )
	#draw_chart ( candlesticks, offset = -n_candlesticks.get ( ) ) if ( ( e.width - w_last != 0 ) or ( e.height - h_last != 0 ) ) else None
#	draw_chart ( candlesticks, offset = -n_candlesticks.get ( ), e = e ) if int ( e.width ) != w_last or int ( e.height ) != h_last else None
#	)

#draw_chart ( candlesticks [ len ( candlesticks ) - n_candlesticks.get ( ) + 1 : len ( candlesticks ) ] )
#draw_chart ( candlesticks, offset = -n_candlesticks.get ( ) )
root.mainloop ( )
