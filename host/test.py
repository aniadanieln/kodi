# denmark television plugin written by IPTVxtra
# -*- coding: utf-8 -*-

# for more info please visit http://www.iptvxtra.net

import xbmcgui,xbmcplugin,sys 
plugin_handle = int(sys.argv[1])

def add_video_item(url, infolabels, img=''):
    listitem = xbmcgui.ListItem(infolabels['title'], iconImage=img, thumbnailImage=img)
    listitem.setInfo('video', infolabels)
    listitem.setProperty( "Fanart_Image", img )
    xbmcplugin.addDirectoryItem(plugin_handle, url, listitem, isFolder=False)



add_video_item('https://nrk1us-f.akamaihd.net/i/nrk1us_0@102847/master.m3u8|X-Forwarded-For=148.122.12.206',{ 'title': 'NRK 1 (NO)'},img='http://srv1.iptvxtra.net/xbmc/senderlogos_dk/nrk1.png')
add_video_item('https://nrk2us-f.akamaihd.net/i/nrk2us_0@107231/master.m3u8|X-Forwarded-For=148.122.12.206',{ 'title': 'NRK 2 (NO)'},img='http://srv1.iptvxtra.net/xbmc/senderlogos_dk/nrk2.png')
add_video_item('https://nrk3us-f.akamaihd.net/i/nrk3us_0@107233/master.m3u8|X-Forwarded-For=148.122.12.206',{ 'title': 'NRK 3 (NO)'},img='http://srv1.iptvxtra.net/xbmc/senderlogos_dk/nrk3.png')

xbmcplugin.endOfDirectory(plugin_handle)





















