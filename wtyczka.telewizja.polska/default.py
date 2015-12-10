# -*- coding: cp1250 -*-
#from __future__ import unicode_literals
 
import sys,xbmc,xbmcaddon
import resources.lib.requests as requests
import re,os,xbmcplugin,xbmcgui

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')

Addon = xbmcaddon.Addon('wtyczka.telewizja.polska')
home = Addon.getAddonInfo('path')

sys.path.append( xbmc.translatePath("special://home/addons/wtyczka.telewizja.polska/resources/lib") )
sys.path.append( xbmc.translatePath("special://home/addons/wtyczka.telewizja.polska/obrazy") )

if 'extrafanart' in sys.argv[2]: sys.exit(0)

if 'runstream' in sys.argv[2]:
    url = sys.argv[2].replace('?runstream=','')
    px = xbmc.translatePath("special://home/addons/wtyczka.telewizja.polska/resources/lib/zapping.py")
    xbmc.executebuiltin('RunScript('+px+',url='+url+')')
    sys.exit(0)

obrazy = xbmc.translatePath( os.path.join( home, 'obrazy' ) )
iconimage = xbmc.translatePath( os.path.join( home, 'obrazy/DefaultVideo.png' ) )
icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
icontv = xbmc.translatePath( os.path.join( home, 'obrazy/telewizja.png' ) )
icontest = xbmc.translatePath( os.path.join( home, 'obrazy/test.png' ) )
iconeska = xbmc.translatePath( os.path.join( home, 'obrazy/eskatv.png' ) )
eskaicon = xbmc.translatePath( os.path.join( home, 'resources/lib/eska.png' ) )
eskaricon = xbmc.translatePath( os.path.join( home, 'resources/lib/eskar.png' ) )
tvpicon = xbmc.translatePath( os.path.join( home, 'resources/lib/tvp.png' ) )
net = xbmc.translatePath( os.path.join( home, 'resources/lib/net.png') )
######## IKONY KANAŁÓW TV ############################################################
tvn24 = xbmc.translatePath( os.path.join( obrazy, 'tvn24.png' ) )

tvpregionalna = xbmc.translatePath( os.path.join( obrazy, 'TvpRegionalna.png' ) ) 
fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )

xbmcPlayer = xbmc.Player()
playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
mode = sys.argv[2]


#xbmc.executebuiltin('XBMC.Notification('+idx[1]+' , Aktualnie odtwarzana audycja ,20000,'+idx[2]+')')


def main():

    if 'xcat1' in mode: tvp()
    elif 'xcat2' in mode: eska()
    elif 'xcat3' in mode: looknij()
    elif 'xcat4' in mode: telewizja()
    elif 'xcat5' in mode: filmboxlive()
    elif 'xcat6' in mode: lokalna()
    else:
        addDir('[COLOR gold][B] Telewizja [/B][/COLOR]', 'plugin://wtyczka.telewizja.polska/?xcat4x', icontv)
        addDir(' FilmBox Live ', 'plugin://wtyczka.telewizja.polska/?xcat5x', xbmc.translatePath( os.path.join( obrazy, 'filmboxlive.png' ) ) )
        addDir(' Looknij TV ', 'plugin://wtyczka.telewizja.polska/?xcat3', xbmc.translatePath( os.path.join( obrazy, 'looknijtv.png' ) ) )
        addDir(' Eska GO ', 'plugin://wtyczka.telewizja.polska/?xcat2x', xbmc.translatePath( os.path.join( obrazy, 'eskago.png' ) ) )
        addDir('TVP Stream', 'plugin://wtyczka.telewizja.polska/?xcat1x', xbmc.translatePath( os.path.join( obrazy, 'tvpstream.png' ) ) )
        addDir('TV Lokalna', 'plugin://wtyczka.telewizja.polska/?xcat6x', xbmc.translatePath( os.path.join( obrazy, 'tvlokalna.png' ) ) )

        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        sys.exit(0)
    
def addLink(name,url,iconimage):
        ok=True
        if 'looknij.tv' in url: url = 'plugin://wtyczka.telewizja.polska/?runstream=' + url + '***' + name + '***' + iconimage	
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
#fanart        liz.setProperty( "Fanart_Image", iconimage )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,iconimage):
    print iconimage
    liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setProperty( "Fanart_Image", iconimage )
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

#####################################################################################################

def tvp():
    link = get_url()
    for i in link:
        url = 'plugin://wtyczka.telewizja.polska/?runstream=' + i[0] + '***' + i[1] + '***' + i[2]
        addLink(i[1],url,i[2])
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    sys.exit(0)

########################################################################################################

def looknij():
    addLink("Eleven -looknij", "rtmp://144.76.154.14/live/eleven live=true timeout=15", icon) 
    addLink("Eleven Sport -looknij", "rtmp://144.76.154.14/live/elevensport live=true timeout=15", icon) 
    addLink("HBO -looknij", "rtmp://149.202.74.234/live/hbohd live=true timeout=15", icon) 
    addLink("HBO 2", "rtmp://149.202.74.234/live/hbo2 live=true timeout=15", icon) 
    addLink("HBO Comedy -looknij", "rtmp://149.202.74.234/live/hbocom live=true timeout=15", icon) 
    addLink("Canal+ -looknij", "rtmp://149.202.74.234/live/canalhd live=true timeout=15", icon) 
    addLink("Canal+ Sport -looknij", "rtmp://149.202.74.234/live/canalsport live=true timeout=15", icon) 
    addLink("Cinemax -looknij", "rtmp://149.202.68.200/live/cinemaxhd live=true timeout=15", icon) 
    addLink("Discovery -looknij", "rtmp://149.202.74.234/live/discoveryhd live=true timeout=15", icon) 
    addLink("Domo+ -looknij", "rtmp://149.202.74.234/live/domo live=true timeout=15", icon)  
    addLink("Eurosport -looknij", "rtmp://85.10.208.218/live/eurosport live=true timeout=15", icon) 
    addLink("Eurosport 2 -looknij", "rtmp://149.202.68.200/live/eurosport2hd live=true timeout=15", icon) 
    addLink("FOX Comedy -looknij", "rtmp://149.202.68.200/live/foxcom live=true timeout=15", icon) 
    addLink("nSport+ -looknij", "rtmp://85.10.208.218/live/n2sport live=true timeout=15", icon)
    addLink("National Geographic -looknij", "rtmp://144.76.154.14/live/nageo live=true timeout=15", icon) 
    addLink("Orange Sport -looknij", "rtmp://144.76.154.14/live/orangesport live=true timeout=15", icon) 
    addLink("TVN -looknij", "rtmp://85.10.208.218/live/tvn live=true timeout=15", icon) 
    addLink("TVN 24 -looknij", "rtmp://85.10.208.218/live/tvn24 live=true timeout=15", icon) 
    addLink("TVN Style -looknij", "rtmp://85.10.208.218/live/tvnstyle live=true timeout=15", icon) 
    addLink("TVN Turbo -looknij", "rtmp://85.10.208.218/live/tvnturbo live=true timeout=15", icon) 
    addLink("TVP 1 -looknij", "rtmp://85.10.208.218/live/jedynka1 live=true timeout=15", icon) 
    addLink("TVP 2 -looknij", "rtmp://149.202.74.239/live/Tvp2 live=true timeout=15", icon) 
    addLink("TVP Sport -looknij", "rtmp://85.10.208.218/live/tvpsport live=true timeout=15", icon)
    addLink("TVP Seriale -looknij", "rtmp://144.76.154.14/live/tvpseriale live=true timeout=15", icon)
    addLink("TTV -looknij", "rtmp://149.202.74.234/live/ttv live=true timeout=15", icon) 
    addLink("                         ",'none','none')
    
    addLink("TVP 1","http://looknij.tv/?port=Tvp-1",icon)
    addLink("TVP 2","http://looknij.tv/?port=Tvp-2",icon)
    addLink("TVP Info","http://looknij.tv/?port=tvp-info",icon)
    addLink("TVP Seriale","http://looknij.tv/?port=tvpseriale",icon)
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

############################################################################################################

def eska():
# tv
    addLink("[LIGHT][COLOR ff2e2e1e][I]—————< TV >———————————————————————————[/I][/COLOR][/LIGHT]",'none','none')
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
# radio
    addLink("[LIGHT][COLOR ff2e2e1e][I]————< RADIO >——————————————————————————[/I][/COLOR][/LIGHT]",'none','none')
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

#############################################################################################################

def filmboxlive():

    addLink("FilmBox                    ", "http://spi-live.ercdn.net/spi/smil:filmboxbasicsd_pl_0.smil/chunklist_b800000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", icontest) 
    addLink("FilmBox Premium HD         ", "http://spi-live.ercdn.net/spi/smil:filmboxextrasd_pl_0.smil/chunklist_b800000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", icontest) 
    addLink("[LIGHT]FilmBox Premium HD  [/LIGHT]", "http://inea.live.e238-po.insyscd.net/filmboxextra.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", icontest)
    addLink("[LIGHT]FilmBox Extra HD    [/LIGHT]", "http://inea.live.e238-po.insyscd.net/filmboxhd.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", icontest) 
    addLink("FilmBox Extra HD           ", "http://spi-live.ercdn.net/spi/smil:filmboxhd_pl_0.smil/chunklist_b1800000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", icontest) 
    addLink("FilmBox Action HD          ", "http://inea.live.e238-po.insyscd.net/filmboxaction.smil/chunklist_.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", icontest)
    addLink("FightBox HD                ", "http://spi-live.ercdn.net/spi/smil:fightboxhd_1.smil/chunklist_b1800000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", icontest) 
    addLink("Kino Polska                ", "http://spi-live.ercdn.net/spi/smil:kinopolskahd_international_0.smil/chunklist_b1200000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", icontest) 
    addLink("[LIGHT]Kino Polska[/LIGHT] ", "http://inea.live.e238-po.insyscd.net/kinopolska.smil/chunklist_.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", icontest) 
    addLink("Kino Polska Muzyka         ", "http://spi-live.ercdn.net/spi/smil:kinopolskamuzikasd_international_0.smil/chunklist_b800000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", icontest) 
    addLink("ArtHouse HD [COLOR ff2e2e1e][I](napisy)[/I][/COLOR]    ", "http://spi-live.ercdn.net/spi/smil:fbarthousesd_pl_0.smil/chunklist_b800000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", icontest) 
    addLink("DocuBox HD                 ", "http://spi-live.ercdn.net/spi/smil:docuboxhd_0.smil/chunklist_b1600000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", icontest) 
    addLink("FasionBox HD               ", "http://spi-live.ercdn.net/spi/smil:fashionboxhd_0.smil/chunklist_b1600000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", icontest) 
    addLink("360TuneBox HD              ", "http://spi-live.ercdn.net/spi/smil:360tuneboxhd_0.smil/chunklist_b1600000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", icontest) 
    addLink("Fast'n'Fun HD              ", "http://spi-live.ercdn.net/spi/smil:fastnfunhd_0.smil/chunklist_b1200000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", icontest) 
    addLink("Madscreen                  ", "http://spi-live.ercdn.net/spi/smil:madscreen_0.smil/chunklist_b1800000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", icontest) 

    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    sys.exit(0)

##############################################################################################################
def lokalna():

    addLink("TV Kujawy          ", "rtmp://stream.tvkujawy.pl/live/broadcast live=true", icontest) 
    addLink("Stella             ", "rtmp://live-tvk.tvkstella.pl/flvplayback playpath=StellaLive swfUrl=http://www.tvkstella.pl/flowplayer-3.2.7.swf pageUrl=http://www.tvkstella.pl/live_tv live=true swfVfy=true live=true", icontest) 
    addLink("WTK                ", "http://wtk.live-ext.e96-jw.insyscd.net/wtk.smil/playlist.m3u8 live=true", icontest) 
    addLink("CW24TV             ", "rtmp://cdn4.stream360.pl:1935/CW24/transmisja_live live=true", icontest) 
    addLink("Pomerania          ", "rtmp://153.19.248.4:1935/publishlive/pomeraniatv", icontest) 
    addLink("Lech TV            ", "http://wtk.live-ext.e96-jw.insyscd.net/lechtv.smil/playlist.m3u8 live=true", icontest) 
    addLink("Pomorska TV        ", "rtmp://stream.trefl.com/livepkgr/ playpath=livestream_2 swfUrl=http://pomorska.tv/player/jwplayer.flash.swf pageUrl=http://pomorska.tv/livestream live=true swfVfy=true live=true", icontest) 
    addLink("Tawizja            ", "rtmp://w-stream2.4vod.tv:1935/lduitv/ playpath=lduitv.stream swfUrl=http://www.tawizja.pl/video/lduflash.swf pageUrl=http://www.tawizja.pl/video/program-emisja-na-zywo.htm live=true swfVfy=true live=true", icontest) 
    addLink("TVP Warszawa       ", "http://195.245.213.230/live/warszawa2.isml/warszawa2.m3u8 live=true", iconimage) 
    addLink("TVP Białystok      ", "http://195.245.213.230/live/bialystok.isml/bialystok.m3u8 live=true", tvpregionalna) 
    addLink("TVP Bydgoszcz      ", "http://195.245.213.230/live/bydgoszcz.isml/bydgoszcz.m3u8 live=true", tvpregionalna) 
    addLink("TVP Gdańsk         ", "http://195.245.213.230/live/gdansk.isml/gdansk.m3u8 live=true", tvpregionalna) 
    addLink("TVP Gorzów Wlkp.   ", "http://195.245.213.230/live/gorzow.isml/gorzow.m3u8 live=true", tvpregionalna) 
    addLink("TVP Katowice       ", "http://195.245.213.230/live/katowice.isml/katowice.m3u8 live=true", tvpregionalna) 
    addLink("TVP Kielce         ", "http://195.245.213.230/live/kielce.isml/kielce.m3u8 live=true", tvpregionalna) 
    addLink("TVP Kraków         ", "http://195.245.213.230/live/krakow.isml/krakow.m3u8 live=true", tvpregionalna) 
    addLink("TVP Lublin         ", "http://195.245.213.230/live/lublin.isml/lublin.m3u8 live=true", tvpregionalna) 
    addLink("TVP Łódź           ", "http://195.245.213.230/live/lodz.isml/lodz.m3u8 live=true", tvpregionalna) 
    addLink("TVP Olsztyn        ", "http://195.245.213.230/live/olsztyn.isml/olsztyn.m3u8 live=true", tvpregionalna) 
    addLink("TVP Opole          ", "http://195.245.213.230/live/opole.isml/opole.m3u8 live=true", tvpregionalna) 
    addLink("TVP Poznań         ", "http://195.245.213.230/live/poznan.isml/poznan.m3u8 live=true", tvpregionalna) 
    addLink("TVP Rzeszów        ", "http://195.245.213.230/live/rzeszow.isml/rzeszow.m3u8 live=true", tvpregionalna) 
    addLink("TVP Szczecin       ", "http://195.245.213.230/live/szczecin.isml/szczecin.m3u8 live=true", tvpregionalna) 
    addLink("TVP Wrocław        ", "http://195.245.213.230/live/wroclaw.isml/wroclaw.m3u8 live=true", tvpregionalna) 


    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    sys.exit(0)
########################################################################################################
def zagraniczne():
    addLink("abc News [USA]", "http://abclive.abcnews.com/i/abc_live4@136330/index_1200_av-b.m3u8?=key live=true", icon) 
    addLink("CBS News [USA] [I]FullHD[/I]", "http://cbsnewshd-lh.akamaihd.net/i/CBSNDC_4@199302/index_4000_av-b.m3u8?sd=10&rebase=on live=true", icon) 
    addLink("Global [CAN]", "https://glblvestu-f.akamaihd.net/i/glblvestu_1@78149/master.m3u8?__b__=900&hdnea=ip=99.18.68.202~st=1434303944~exp=1434304544~acl=/i/*~id=3f0edb02-c4e5-4596-8950-4331b8ce1baf~hmac=4acbecb511f7c3beaf085123ab9097c7a6acbd5d857fd4cefbfdfb733b666f57 live=true", icon) 
    addLink("Weather Nation [USA]", "http://cdnapi.kaltura.com/p/931702/sp/93170200/playManifest/entryId/1_oorxcge2/format/applehttp/protocol/http/uiConfId/28428751/a.m3u8?key= live=true", icon) 
    addLink("ARD [GR]", "http://daserste_live-lh.akamaihd.net/i/daserste_de@91204/master.m3u8?=key live=true", icon) 
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    sys.exit(0)

########################################################################################################
def telewizja():

#    addLink("[COLOR lime][B]TEST1[/B][/COLOR]", "http://inea.live.e238-po.insyscd.net/tvnhd.smil/chunklist_.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", icontest) 
#    addLink("[COLOR aqua][B]TEST2[/B][/COLOR]", "http://inea.live.e238-po.insyscd.net/natgeowild.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", icontest) 


#C
    addLink("Canal+", "rtmp://195.154.217.247:80/liverepeater playpath=143112 swfUrl=http://cdn.deltatv.pw/players.swf live=1 token=Fo5_n0w?U.rA6l3-70w47ch flashver=WIN\2019,0,0,245 timeout=15 swfVfy=1 pageUrl=http://deltatv.pw/stream.php?id=143112&width=640&height=480", icontest) 
    addLink("Canal+ [COLOR ff000055]stream 2[/COLOR]", "rtmp://195.154.180.99:80/liverepeater playpath=143112 swfUrl=http://cdn.deltatv.pw/players.swf live=1 token=Fo5_n0w?U.rA6l3-70w47ch flashver=WIN\2019,0,0,245 timeout=13 swfVfy=1 pageUrl=http://deltatv.pw/stream.php?id=143112&width=640&height=480", icon) 
   # addLink("Canal+ Sport", "rtmpe://live.tutelehd.com/redirect?token=z0dbaEeh0Io1dieFJr6VSAExpired=1449700403 playpath=sfvbdfibherhwib swfUrl=http://tutelehd.com/player.swf swfVfy=1 flashver=WIN\2019,0,0,245 live=true token=0fea41113b03061a pageUrl=http://tutelehd.com/embed/embed.php?channel=sfvbdfibherhwib", icon) 
  #  addLink("Canal+ Sport [COLOR ff000055]stream 2[/COLOR]", "rtmpe://stream.byetv.org/redirect?token=7Gr71iZRQkJd2IX7zECNLgExpired=1449699794 playpath=bya53uos9 swfUrl=http://www.byetv.org/player.swf flashver=WIN\2019,0,0,245 token=0fea41113b03061a live=1 timeout=25 swfVfy=1 pageUrl=http://www.byetv.org/embed.php?a=1320&id=&width=700&height=400&autostart=true&strech=", icon) 

#D
    addLink("Discovery ID [I]HD[/I]", "http://inea.live.e238-po.insyscd.net/id.smil/chunklist_.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", icontest) 
    addLink("Discovery Life [I]HD[/I]", "http://inea.live.e238-po.insyscd.net/animalplanet.smil/chunklist_.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", icontest) 
    addLink("Discovery Science [I]HD[/I]", "http://inea.live.e238-po.insyscd.net/discoveryscience.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", icontest) 
    addLink("Discovery Turbo Xtra [I]HD[/I]", "http://inea.live.e238-po.insyscd.net/dtx.smil/chunklist_.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", icontest) 

#E
    addLink("EDU sat", "rtmp://178.73.10.66:1935/live playpath=mpegts.stream swfUrl= pageUrl= live=true swfVfy=true live=true", icontest) 
    addLink("Eleven", "rtmp://144.76.154.14/live playpath=eleven swfUrl= pageUrl= live=true swfVfy=true live=true", icontest) 
 #   addLink("Eleven Sport", "rtmp://live.abcast.net/redirect?token=q8Yg185XxhEvM7v1-5WVeAExpired=1449701720 playpath=ver4d122f38f81526f6dc040e swfUrl=http://abcast.net/juva.swf live=1 timeout=15 swfVfy=1 pageUrl=http://abcast.net/embed.php?file=fglknfbofdnob", icon) 
    addLink("Eska TV ", "rtmp://stream.smcloud.net/live2/eskatv/eskatv_480p live=true swfVfy=true pageUrl=", icontest) 

#F
    addLink("Fokus", "rtmp://stream.smcloud.net/live/fokustv live=true swfVfy=true pageUrl=", icontest) 

#H
  #  addLink("HBO [COLOR ff000055][I](org)[/I][/COLOR]", "rtmp://50.7.28.146/app playpath=17194?MTQ0OTY5NzQ0Mzs2MzZhZTQ0NWVkNjQwYWViMmYyYmI5ZWZlMmQ1MDM0Ng== swfVfy=1 timeout=10 swfUrl=http://cdn.shidurlive.com/player.swf live=true pageUrl=http://www.shidurlive.com/embed/sdaffsdafsdf", icon) 
  #  addLink("HBO Comedy [COLOR ff000055][I](org)[/I][/COLOR]", "rtmp://50.7.28.194/app playpath=17249?MTQ0OTY5NzQ4NTsxMzZlOGE5NTMwNDVkMTJjZTZjNzIxZGQ1YTFjZGUyOQ== swfVfy=1 timeout=10 swfUrl=http://cdn.shidurlive.com/player.swf live=true pageUrl=http://www.shidurlive.com/embed/hjghjhjgjgfhj", icon) 

#K
    addLink("Kino Polska [I]HD[/I]", "http://inea.live.e238-po.insyscd.net/kinopolska.smil/chunklist_.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", icontest) 

#M
    addLink("Mango24", "rtmp://stream.mango.pl/rtplive playpath=live/1 swfUrl=http://tv.mango.pl/player.swf pageUrl=http://tv.mango.pl/ live=true swfVfy=true live=true", icontest) 

#N
    addLink("National Geographic", "rtmp://144.76.154.14/live playpath=nageo swfUrl= live=1 pageUrl= live=true", icontest) 
    addLink("NatGeo Wild [I]HD[/I]", "http://inea.live.e238-po.insyscd.net/natgeowildhd.smil/chunklist_.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", icontest) 

#O
    addLink("Opoka.tv", "rtmp://153.19.248.2:1935/publishlive?play=123452 playpath=Opokatv swfUrl=http://images.popler.tv/player/flowplayer.commercial.swf pageUrl=http://www.popler.tv/Opokatv live=true swfVfy=true live=true", icontest) 

#P
    addLink("Polsat", "rtmpe://stream.byetv.org/redirect?token=kPJMz70JgwmVy4UBfFPr8gExpired=1449553664 playpath=bya53rk7b swfUrl=http://www.byetv.org/player.swf flashver=WIN\2019,0,0,245 token=0fea41113b03061a live=1 timeout=25 swfVfy=1 pageUrl=http://www.byetv.org/embed.php?a=1307&id=&width=700&height=400&autostart=true&strech=", icontest) 
    addLink("Polsat Sport News", "http://n-2-4.dcs.redcdn.pl/hls/o2/ATM-Lab/borys/MotoGP/live.livx/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", icontest) 

#R
    addLink("RBL.tv", "rtmp://153.19.248.4:1935/publishlive/rebeltv", icontest) 
    addLink("Republika", "http://stream4.videostar.pl/999_tvrtest/smil:4321abr.ism/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", icontest) 
    addLink("Republika [COLOR ff000055]stream 2[/COLOR]", "http://stream6.videostar.pl/999_tvrtest/smil:4321high.ism/playlist.m3u8?key= live=true", icontest) 

#S
    addLink("Stars.tv", "http://starstv.live.e55-po.insyscd.net/starstvhd.smil/chunklist_.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", icontest) 
    addLink("SuperStacja [I]HD[/I]", "http://inea.live.e238-po.insyscd.net/superstacja.smil/chunklist_.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", icontest) 

#T
  #  addLink("TLC", "rtmp://live.openlive.org/redirect?token=MEVPv6OrUONU7Tr1BD83FwExpired=1449701425 playpath=ver7c9b621d487065df2f2fd8 swfUrl=http://www.openlive.org/player.swf live=1 timeout=15 swfVfy=1 pageUrl=http://openlive.org/embed.php?file=fghghdfghgfhfj&width=640&height=380", icon) 
    addLink("Trwam", "http://trwamtv.live.e96-jw.insyscd.net/trwamtv.smil/playlist.m3u8 live=true", icontest) 
  #  addLink("TVN", "rtmp://50.7.28.194/app playpath=17180?MTQ0OTY5Nzg5NTswNGU4ZjM2MTU3MzViOTVlZjEyMzYxMmM2OGNhZWMzNg== swfVfy=1 timeout=10 swfUrl=http://cdn.shidurlive.com/player.swf live=true pageUrl=http://www.shidurlive.com/embed/ghgfjghjgh", icon) 
    addLink("TVN [COLOR ff000055]stream 2 (org)[/COLOR]", "rtmpe://live.tutelehd.com/redirect?token=ssTbxoD2xZrX5jAEL7leVAExpired=1449701695 playpath=rweojgntrbgn swfUrl=http://tutelehd.com/player.swf swfVfy=1 flashver=WIN\2019,0,0,245 live=true token=0fea41113b03061a pageUrl=http://tutelehd.com/embed/embed.php?channel=rweojgntrbgn", icon) 
  #  addLink("TVN [COLOR ff000055]stream 3 (org)[/COLOR]", "rtmp://50.7.28.82/app playpath=17180?MTQ0OTY5ODgzNzs5NmI0MGM3MTkwYTNmZGYwZjYzYjU5OWRmNmViMDdmYg== swfVfy=1 timeout=10 swfUrl=http://cdn.shidurlive.com/player.swf live=true pageUrl=http://www.shidurlive.com/embed/ghgfjghjgh", icon) 
    addLink("TVN24", "rtmpe://stream.byetv.org/redirect?token=bV_IxEFlyPZeptIA_TLDNAExpired=1449699630 playpath=bya53u9w2 swfUrl=http://www.byetv.org/player.swf flashver=WIN\2019,0,0,245 token=0fea41113b03061a live=1 timeout=25 swfVfy=1 pageUrl=http://www.byetv.org/embed.php?a=1317&id=&width=700&height=400&autostart=true&strech=", icon) 
    addLink("TVP1 [COLOR ff000055](org)[/COLOR]", "rtmpe://stream.byetv.org/redirect?token=CEmPynnRYGdOVIoGSb8VgQExpired=1449699691 playpath=bya53srbf swfUrl=http://www.byetv.org/player.swf flashver=WIN\2019,0,0,245 token=0fea41113b03061a live=1 timeout=25 swfVfy=1 pageUrl=http://www.byetv.org/embed.php?a=1309&id=&width=700&height=400&autostart=true&strech=", icon) 
    addLink("TVP1 [COLOR ff000055]stream 2[/COLOR]", "rtmp://50.7.28.130/app playpath=17187?MTQ0OTY5Nzg1MTs2ZThjYmVkMDMzODNmNzQ3NmE4OGUxYzg5YWE4YTQxMA== swfVfy=1 timeout=10 swfUrl=http://cdn.shidurlive.com/player.swf live=true pageUrl=http://www.shidurlive.com/embed/xngfjhgjghjgh", icon) 
    addLink("TVP Info [I]HD[/I]   ", "http://195.245.213.230/live/warszawa.isml/warszawa.m3u8 live=true", iconimage)
    addLink("TVP Seriale", "rtmp://144.76.154.14/live/tvpseriale live=true", icon) 
    addLink("TVP Warszawa [I]HD[/I]", "http://195.245.213.230/live/warszawa2.isml/warszawa2.m3u8 live=true", iconimage) 

    addLink("                ",'none','none')
    addLink("abc News [USA]", "http://abclive.abcnews.com/i/abc_live4@136330/index_1200_av-b.m3u8?=key live=true", icon) 
    addLink("CBS News [USA] [I]FullHD[/I]", "http://cbsnewshd-lh.akamaihd.net/i/CBSNDC_4@199302/index_4000_av-b.m3u8?sd=10&rebase=on live=true", icon) 
    addLink("Global [CAN]", "https://glblvestu-f.akamaihd.net/i/glblvestu_1@78149/master.m3u8?__b__=900&hdnea=ip=99.18.68.202~st=1434303944~exp=1434304544~acl=/i/*~id=3f0edb02-c4e5-4596-8950-4331b8ce1baf~hmac=4acbecb511f7c3beaf085123ab9097c7a6acbd5d857fd4cefbfdfb733b666f57 live=true", icon) 
    addLink("Weather Nation [USA]", "http://cdnapi.kaltura.com/p/931702/sp/93170200/playManifest/entryId/1_oorxcge2/format/applehttp/protocol/http/uiConfId/28428751/a.m3u8?key= live=true", icon) 
    addLink("ARD [GER]", "http://daserste_live-lh.akamaihd.net/i/daserste_de@91204/master.m3u8?=key live=true", icon) 


    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    sys.exit(0)

main()




