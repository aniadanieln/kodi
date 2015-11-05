# -*- coding: cp1254 -*-
# for more info please visit http://www.iptvxtra.net


import sys,xbmc,xbmcaddon

if 'extrafanart' in sys.argv[2]: sys.exit(0)

if 'runstream' in sys.argv[2]:
    url = sys.argv[2].replace('?runstream=','')
    px = xbmc.translatePath("special://home/addons/plugin.video.iptvxtra-polen/resources/lib/zapping.py")
    xbmc.executebuiltin('RunScript('+px+',url='+url+')')
    sys.exit(0)

import resources.lib.requests as requests
import re,os,xbmcplugin,xbmcgui

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')
Addon = xbmcaddon.Addon('plugin.video.iptvxtra-polen')
home = Addon.getAddonInfo('path')
icon = xbmc.translatePath( os.path.join( home, 'resources/lib/icon.png' ) )
eskaicon = xbmc.translatePath( os.path.join( home, 'resources/lib/eska.png' ) )
eskaricon = xbmc.translatePath( os.path.join( home, 'resources/lib/eskar.png' ) )
tvpicon = xbmc.translatePath( os.path.join( home, 'resources/lib/tvp.png' ) )
net = xbmc.translatePath( os.path.join( home, 'resources/lib/net.png') )
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )
xbmcPlayer = xbmc.Player()
playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
mode = sys.argv[2]

def main():

    if 'xcat1' in mode: tvp()
    elif 'xcat2' in mode: eska()
    elif 'xcat3' in mode: polen1()
    elif 'xcat4' in mode: polen2()
    else:
        addDir('TVP / TVN / Extras', 'plugin://plugin.video.iptvxtra-polen/?xcat3x', icon)
        addDir('TVP - informacje/regionalna', 'plugin://plugin.video.iptvxtra-polen/?xcat1x', tvpicon)
        addDir('Eska TV - Muzyka', 'plugin://plugin.video.iptvxtra-polen/?xcat2x', eskaicon)
        addDir('Test Channels', 'plugin://plugin.video.iptvxtra-polen/?xcat4x', icon)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        sys.exit(0)
    
def addLink(name,url,iconimage):
        ok=True
        if 'looknij.tv' in url: url = 'plugin://plugin.video.iptvxtra-polen/?runstream=' + url + '***' + name + '***' + iconimage	
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", iconimage )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,iconimage):
    print iconimage
    liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setProperty( "Fanart_Image", icon )
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=True)

def get_url():

    basicurl = 'http://tvpstream.tvp.pl/'
    plurl = requests.get(basicurl)
    pattern = '<div class="button.*?data-video_id="([^"]+)" title="([^"]+)">.*?<img src="([^"]+)".*?</div>'
    rResult = parse(plurl.text, pattern)
    return rResult[1]

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

def eska():
    addLink("Eska Best Music","rtmp://stream.smcloud.net/live2/best/best_480p live=1",eskaicon)
    addLink("Eska Party","rtmp://stream.smcloud.net/live2/eska_party/eska_party_360p live=1",eskaicon)
    addLink("Eska Party HD","rtmp://stream.smcloud.net/live2/eska_party/eska_party_720p live=1",eskaicon)
    addLink("Eska Rock","rtmp://stream.smcloud.net/live2/eska_rock/eska_rock_360p live=1",eskaicon)
    addLink("Eska Rock HD","rtmp://stream.smcloud.net/live2/eska_rock/eska_rock_720p live=1",eskaicon)
    addLink("Eska TV","rtmp://stream.smcloud.net/live2/eskatv/eskatv_360p live=1",eskaicon)
    addLink("Eska VOX TV","rtmp://stream.smcloud.net/live2/vox/vox_480p live=1",eskaicon)
    addLink("Eska WAWA TV","rtmp://stream.smcloud.net/live2/wawa/wawa_360p live=1",eskaicon)
    addLink("Eska WAWA TV HD","rtmp://stream.smcloud.net/live2/wawa/wawa_720p live=1",eskaicon)
    addLink("Polo TV","rtmp://stream.smcloud.net/live/polotv swfUrl=http://polotv.pl/thrdparty/flowplayer/flowplayer.rtmp-3.1.4.swf pageUrl=http://polotv.pl/player live=1",eskaicon)
    addLink("TV Disco","rtmp://edge4.popler.tv:1935/publishlive/tvdisco swfUrl=swfUrl=http://www.popler.tv/live/tvdisco live=1",eskaicon)

    addLink("Radio ESKA","http://s3.deb1.scdn.smcloud.net/t042-1.aac",eskaricon)
    addLink("Eska Rock","http://s3.deb1.scdn.smcloud.net/t041-1.aac",eskaricon)
    addLink("Eska Rock Polska","http://s3.deb1.scdn.smcloud.net/t008-1.mp3",eskaricon)
    addLink("Eska Party","http://s3.deb1.scdn.smcloud.net/t005-1.aac",eskaricon)
    addLink("Eska Summer City","http://s3.deb1.scdn.smcloud.net/t010-1.mp3",eskaricon)
    addLink("Eska Club","http://s3.deb1.scdn.smcloud.net/t004-1.mp3",eskaricon)
    addLink("Eska Tiesto","http://s3.deb1.scdn.smcloud.net/t023-1.mp3",eskaricon)
    addLink("Eska Goraca 20","http://s3.deb1.scdn.smcloud.net/t019-1.aac",eskaricon)
    addLink("Eska Goraca 100","http://s3.deb1.scdn.smcloud.net/t039-1.mp3",eskaricon)
    addLink("Eska Love","http://s3.deb1.scdn.smcloud.net/t038-1.mp3",eskaricon)
    addLink("Eska Young Stars","http://s3.deb1.scdn.smcloud.net/t025-1.mp3",eskaricon)
    addLink("Eska Hity Nie Tylko Na Czasie","http://s3.deb1.scdn.smcloud.net/t014-1.aac",eskaricon)
    addLink("Eska Global Lista","http://s3.deb1.scdn.smcloud.net/t016-1.mp3",eskaricon)
    addLink("Eska Dance","http://s3.deb1.scdn.smcloud.net/t012-1.mp3",eskaricon)
    addLink("Eska R'N'B","http://s3.deb1.scdn.smcloud.net/t003-1.mp3",eskaricon)
    addLink("Eska Ballads","http://s3.deb1.scdn.smcloud.net/t011-1.mp3",eskaricon)
    addLink("Eska Rap","http://s3.deb1.scdn.smcloud.net/t002-1.mp3",eskaricon)
    addLink("Eska Cinema","http://s3.deb1.scdn.smcloud.net/t024-1.mp3",eskaricon)
    addLink("Eska Armin Van Buuren","http://s3.deb1.scdn.smcloud.net/t032-1.mp3",eskaricon)
    addLink("Eska Nicky Romero","http://s3.deb1.scdn.smcloud.net/t022-1.mp3",eskaricon)
    addLink("Eska Ultra Music","http://s3.deb1.scdn.smcloud.net/t029-1.mp3",eskaricon)
    addLink("Eska Teksty FM","http://s3.deb1.scdn.smcloud.net/t026-1.mp3",eskaricon)
    addLink("Eska Justin Bieber","http://s3.deb1.scdn.smcloud.net/t099-1.mp3",eskaricon)
    addLink("Eska One Direction","http://s3.deb1.scdn.smcloud.net/t098-1.mp3",eskaricon)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    sys.exit(0)


def tvp():
    link = get_url()
    for i in link:
        url = 'plugin://plugin.video.iptvxtra-polen/?runstream=' + i[0] + '***' + i[1] + '***' + i[2]
        addLink(i[1],url,i[2])
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    sys.exit(0)

def polen1():
    addLink("TVP 1","http://looknij.tv/?port=tvp1",icon)
    addLink("TVP 2","http://looknij.tv/?port=tvp-2",icon)
    addLink("TVP Info","http://looknij.tv/?port=tvp-info",icon)
    addLink("TVP Seriale","http://looknij.tv/?port=tvp-seriale",icon)
    addLink("TVP Sport","http://looknij.tv/?port=tvp-sport",icon)
    addLink("TVP Historia","http://looknij.tv/?port=tvp-historia",icon)
    addLink("TTV","http://looknij.tv/?port=ttv",icon)
    addLink("TVN","http://looknij.tv/?port=tvn",icon)
    addLink("TVN 24","http://looknij.tv/?port=tvn-24",icon)
    addLink("TVN Turbo","http://looknij.tv/?port=tvn-turbo",icon)
    addLink("TVN Style","http://looknij.tv/?port=tvn-style",icon)
    addLink("N Sport","http://looknij.tv/?port=n-sport",icon)
    addLink("Eurosport","http://looknij.tv/?port=eurosport",icon)
    addLink("Eurosport 2","http://looknij.tv/?port=eurosport-2",icon)
    addLink("FOX Comedy","http://looknij.tv/?port=fox-comedy",icon)
    addLink("Disney Channel","http://looknij.tv/?port=disney-channel",icon)
    addLink("TLC","http://looknij.tv/?port=tlc",icon)
    addLink("AXN","http://looknij.tv/?port=axn",icon)
    addLink("AXN White","http://looknij.tv/?port=axn-white",icon)
    addLink("AXN Black","http://looknij.tv/?port=axn-black",icon)
    addLink("Comedy Central","http://looknij.tv/?port=comedy-central-2",icon)
    addLink("Comedy Central Family","http://looknij.tv/?port=comedy-central",icon)
    addLink("National Geographic","http://looknij.tv/?port=national-geographic",icon)
    addLink("Discovery","http://looknij.tv/?port=discovery",icon)
    addLink("Discovery Xtra","http://looknij.tv/?port=discovery-xtra",icon)
    addLink("Disney XD","http://looknij.tv/?port=disney-xd",icon)
    addLink("HBO","http://looknij.tv/?port=hbo",icon)
    addLink("HBO Comedy","http://looknij.tv/?port=hbo-comedy",icon)
    addLink("HBO 2","http://looknij.tv/?port=hbo-2",icon)
    addLink("Canal+","http://looknij.tv/?port=canal",icon)
    addLink("Toya TV","http://video.go.toya.net.pl:8080/live/KyhIZQZuY1Pb0AxwV_z-GQ/1438095204/01_toyahd_hls/index.m3u8",icon)

    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    sys.exit(0)

def polen2():
    addLink("TVP 1","rtmp://178.16.220.163/live/ playpath=jedynka1 swfUrl=http://p.jwpcdn.com/6/12/jwplayer.flash.swf pageUrl=http://tvzafree.pl/videopage/tvp-1/ live=1",icon)
    addLink("TVP 2 - nicht immer verfuegbar","rtmp://178.16.220.163/live/ playpath=tvvvpp22 swfUrl=http://p.jwpcdn.com/6/12/jwplayer.flash.swf pageUrl=http://tvzafree.pl/videopage/tvp-1/ live=1",icon)
    addLink("TVP Kultura","rtmp://178.16.220.163/live/ playpath=tkultura swfUrl=http://p.jwpcdn.com/6/12/jwplayer.flash.swf pageUrl=http://tvzafree.pl/videopage/tvn-turbo/ live=1",icon)
    addLink("TVP Rozrywka","rtmp://178.16.220.163/live/ playpath=trozrywka swfUrl=http://p.jwpcdn.com/6/12/jwplayer.flash.swf pageUrl=http://tvzafree.pl/videopage/tvn-turbo/ live=1",icon)
    addLink("TVN","rtmp://178.16.220.163/live/ playpath=t2vnaa swfUrl=http://p.jwpcdn.com/6/12/jwplayer.flash.swf pageUrl=http://tvzafree.pl/videopage/tvn/ live=1",icon)
    addLink("TVN Turbo","rtmp://178.16.220.163/live/ playpath=tvnturboaa swfUrl=http://p.jwpcdn.com/6/12/jwplayer.flash.swf pageUrl=http://tvzafree.pl/videopage/tvn-turbo/ live=1",icon)
    addLink("TVN 24","rtmp://178.16.220.163/live/ playpath=tvn24aa swfUrl=http://p.jwpcdn.com/6/12/jwplayer.flash.swf pageUrl=http://tvzafree.pl/videopage/tvn-24/ live=1",icon)
    addLink("Polsat 1","rtmp://178.16.220.163/live/ playpath=poolsat swfUrl=http://p.jwpcdn.com/6/12/jwplayer.flash.swf pageUrl=http://tvzafree.pl/videopage/polsat/ live=1",icon)
    addLink("Polsat Sport News","rtmp://178.16.220.163/live/ playpath=snpolsat swfUrl=http://p.jwpcdn.com/6/12/jwplayer.flash.swf pageUrl=http://tvzafree.pl/videopage/polsat/ live=1",icon)
    addLink("Canal+ - nicht immer verfuegbar","rtmp://178.16.220.163/live/ playpath=caaanaal1 swfUrl=http://p.jwpcdn.com/6/12/jwplayer.flash.swf pageUrl=http://tvzafree.pl/videopage/polsat/ live=1",icon)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    sys.exit(0)

def polen3():
    addLink("TVP 1","rtmp://94.242.228.182/yoy/_definst_ playpath=272 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("TVP 2","rtmp://94.242.228.182/yoy/_definst_ playpath=273 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("TVP Historia","rtmp://94.242.228.182/yoy/_definst_ playpath=274 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("TVP Info","rtmp://94.242.228.182/yoy/_definst_ playpath=279 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("TVP Kultura","rtmp://94.242.228.182/yoy/_definst_ playpath=276 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("TVP Sport","rtmp://94.242.228.182/yoy/_definst_ playpath=288 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("TVP ABC","rtmp://94.242.228.182/yoy/_definst_ playpath=314 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("TVP Seriale","rtmp://94.242.228.182/yoy/_definst_ playpath=287 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("TVP Polonia","rtmp://94.242.228.182/yoy/_definst_ playpath=278 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)

    addLink("TVP Rozrywka","rtmp://94.242.228.182/yoy/_definst_ playpath=281 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("Focus TV","rtmp://94.242.228.182/yoy/_definst_ playpath=181 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("teleTOON+","rtmp://94.242.228.182/yoy/_definst_ playpath=160 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("TV Puls","rtmp://94.242.228.182/yoy/_definst_ playpath=180 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("TV Puls 2","rtmp://94.242.228.182/yoy/_definst_ playpath=176 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("Stopklatka","rtmp://94.242.228.182/yoy/_definst_ playpath=182 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("TVN","rtmp://94.242.228.182/yoy/_definst_ playpath=315 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("TVN Turbo","rtmp://94.242.228.182/yoy/_definst_ playpath=345 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("TVN Style","rtmp://94.242.228.182/yoy/_definst_ playpath=346 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("TVN 24","rtmp://94.242.228.182/yoy/_definst_ playpath=347 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("TVN 7","rtmp://94.242.228.182/yoy/_definst_ playpath=177 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("TN 24","rtmp://94.242.228.182/yoy/_definst_ playpath=343 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("TN Met Act","rtmp://94.242.228.182/yoy/_definst_ playpath=344 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)

    addLink("TTV","rtmp://94.242.228.182/yoy/_definst_ playpath=316 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("TV 4","rtmp://94.242.228.182/yoy/_definst_ playpath=331 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("Polo tv","rtmp://94.242.228.182/yoy/_definst_ playpath=295 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("T6 Rozrywka","rtmp://94.242.228.182/yoy/_definst_ playpath=326 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("PSat","rtmp://94.242.228.182/yoy/_definst_ playpath=327 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("PSat Sportnews","rtmp://94.242.228.182/yoy/_definst_ playpath=332 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("TRWAM","rtmp://94.242.228.182/yoy/_definst_ playpath=298 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("Eurosport 2","rtmp://94.242.228.182/yoy/_definst_ playpath=321 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("Orange Sport","rtmp://94.242.228.182/yoy/_definst_ playpath=323 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("DOMO+","rtmp://94.242.228.182/yoy/_definst_ playpath=324 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("Mango 24","rtmp://94.242.228.182/yoy/_definst_ playpath=307 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)

    addLink("Discovery","rtmp://94.242.228.182/yoy/_definst_ playpath=236 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("Nat Geo Wild","rtmp://94.242.228.182/yoy/_definst_ playpath=325 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("MGM","rtmp://94.242.228.182/yoy/_definst_ playpath=237 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("Romance TV HD","rtmp://94.242.228.182/yoy/_definst_ playpath=239 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("Alekino","rtmp://94.242.228.182/yoy/_definst_ playpath=159 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("cnc Film 1","rtmp://94.242.228.182/yoy/_definst_ playpath=250 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("Kuchnia+","rtmp://94.242.228.182/yoy/_definst_ playpath=322 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    addLink("Planete+","rtmp://94.242.228.182/yoy/_definst_ playpath=217 swfUrl=http://yoy.tv/playerv2.swf  pageUrl=http://yoy.tv/channels/ live=1",icon)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    sys.exit(0)

main()




