# ADB Wrapper

```
if __name__ == "__main__":
	adb = ADBWrapper( { "ip": "192.168.4.57" , "port": "5555" } )
	adb.take_screen_shot()
	adb.screen_shot.show()
	adb.open_uri( "https://www.youtube.com/watch?v=naOsvWxeYgo&list=PLcW8xNfZoh7fCLYJi0m3JXLs0LdcAsc0R&index=1" )
	adb.press_key_sequence( [ 22 , 22 , 22 , 22 ] )
	time.sleep( 10 )

	adb.press_keycode( "KEYCODE_MEDIA_PAUSE" )
	adb.press_keycode( "KEYCODE_MEDIA_FAST_FORWARD" )
	adb.press_keycode( "KEYCODE_MEDIA_PLAY" )
```