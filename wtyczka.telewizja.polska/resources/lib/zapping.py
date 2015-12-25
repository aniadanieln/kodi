#!/bin/python
import xbmcgui,xbmc,os,sys,re
import requests as requests
xbmcPlayer = xbmc.Player()
mode = sys.argv[1]
idx = mode.replace("url=", "").split('***')
#xbmc.executebuiltin('XBMC.Notification('+idx[1]+' , Aktualnie odtwarzana audycja ,20000,'+idx[2]+')')

url = idx[0]

def zapp(url,idx):

    if 'looknij.tv' in url:
        xbmc.executebuiltin('XBMC.Notification(Szukam transmisji ,'+idx[1]+',5000,'+idx[2]+')')
        urlpl = requests.get(url)
        pattern = '<div class="yendifplayer".*?src="([^"]+)".*?data-rtmp="([^"]+)"'
        rResult = parse(urlpl.text, pattern)
        xResult = rResult[1][0]
        url = xResult[1]+' playpath='+xResult[0]+' swfUrl=http://looknij.tv/wp-content/plugins/yendif-player/public/assets/libraries/player.swf?1438149198120 pageUrl=http://looknij.tv live=1'
    else:
        xbmc.executebuiltin('XBMC.Notification(Odtwarzanie ,'+idx[1]+',15000,'+idx[2]+')')
        url = requests.get('http://tvpstream.tvp.pl/sess/tvplayer.php?object_id=' + idx[0])
        url = find_between(url.text,"0:{src:'http://",".m3u8")
        url = "http://"+url+".m3u8"
    listitem = xbmcgui.ListItem( idx[1], iconImage=idx[2], thumbnailImage=idx[2])
    playlist = xbmc.PlayList( xbmc.PLAYLIST_VIDEO )
    playlist.clear()
    playlist.add( url, listitem )
    xbmcPlayer.play(playlist,None,False)
    sys.exit(0)

def find_between(s,first,last):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def parse(sHtmlContent, sPattern, iMinFoundValue = 1, ignoreCase = False):
        if ignoreCase:
            aMatches = re.compile(sPattern, re.DOTALL|re.I).findall(sHtmlContent)
        else:
            aMatches = re.compile(sPattern, re.DOTALL).findall(sHtmlContent)
        if (len(aMatches) >= iMinFoundValue):                
            return True, aMatches
        return False, aMatches

zapp(url,idx)