#!/usr/bin/env python3
import subprocess
import time
import math
from PIL import Image
from pathlib import Path
import tempfile
import imagehash

from . import keycode_enum

# https://github.com/0187773933/ADBWrapper/blob/master/v1/wrapper/wrapper.go
class ADBWrapper:

	def __init__( self , options={} ):
		self.options = options
		self.connect()
		self.turn_on_screen()

	def sleep( self , milliseconds ):
		time.sleep( milliseconds )

	def exec( self , bash_command ):
		try:
			return subprocess.getoutput( bash_command )
		except Exception as e:
			print( e )
			return False

	def connect( self ):
		result = self.exec( f"adb connect {self.options['ip']}:{self.options['port']}" )
		print( result )

	def press_key( self , key_code ):
		result = self.exec( f"adb shell input keyevent {key_code}" )
		print( result )

	def press_key_sequence( self , key_sequence ):
		key_sequence = " ".join( [ str( x ) for x in key_sequence ] )
		result = self.exec( f"adb shell input keyevent {key_sequence}" )
		print( result )

	def press_keycode( self , key_code ):
		if keycode_enum.KEYCODES[ key_code ] == False:
			print( "keycode name not found in enum" )
			return False
		self.press_key( keycode_enum.KEYCODES[ key_code ] )

	# https://github.com/ceberous/ShzmTwitchBot/blob/master/main.js#L40=
	def tap( self , x , y ):
		result = self.exec( f"adb shell input tap {x} {y}" )
		print( result )

	def get_screen_power_state( self ):
		try:
			# result = self.exec( 'adb shell dumpsys input_method | grep -c "mScreenOn=true"' )
			result = self.exec( 'adb shell dumpsys power | grep mWakefulness=' )
			result = result.split( "=" )[ 1 ].strip()
			self.screen_power_state = result
		except Exception as e:
			print( e )
			self.screen_power_state = False

	def turn_on_screen( self ):
		self.get_screen_power_state()
		if self.screen_power_state != "Awake":
			self.press_key( 26 )
			self.get_screen_power_state()
		print( self.screen_power_state )

	def open_uri( self , uri ):
		result = self.exec( f"adb shell am start -a android.intent.action.VIEW -d {uri}" )
		print( result )

	def take_screen_shot( self ):
		try:
			with tempfile.TemporaryDirectory() as temp_dir:
				temp_dir_posix = Path( temp_dir )
				with tempfile.NamedTemporaryFile( suffix='.png' , prefix=temp_dir ) as tf:
					temp_file_path = temp_dir_posix.joinpath( tf.name )
					self.exec( f"adb exec-out screencap -p > {str( temp_file_path )}" )
					self.screen_shot = Image.open( str( temp_file_path ) )
		except Exception as e:
			print( e )
			return False

	# https://github.com/JohannesBuchner/imagehash
	def screen_difference_to_image( self , image_path ):
		try:
			with tempfile.TemporaryDirectory() as temp_dir:
				temp_dir_posix = Path( temp_dir )
				with tempfile.NamedTemporaryFile( suffix='.png' , prefix=temp_dir ) as tf:
					temp_file_path = temp_dir_posix.joinpath( tf.name )
					self.exec( f"adb exec-out screencap -p > {str( temp_file_path )}" )
					screen_shot = Image.open( str( temp_file_path ) )
					compared_image = Image.open( str( image_path ) )
					screen_shot_hash = imagehash.phash( screen_shot )
					compared_image_hash = imagehash.phash( compared_image )
					difference = ( screen_shot_hash - compared_image_hash )
					return difference
		except Exception as e:
			print( e )
			return False
