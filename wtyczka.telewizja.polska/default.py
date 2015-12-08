# -*- coding: cp1250 -*-
from __future__ import unicode_literals
 
import sys,xbmc,xbmcaddon
import resources.lib.requests as requests
import re,os,xbmcplugin,xbmcgui

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')

Addon = xbmcaddon.Addon('wtyczka.telewizja.polska')
home = Addon.getAddonInfo('path')

sys.path.append( xbmc.translatePath("special://home/addons/wtyczka.telewizja.polska/resources/lib") )


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

def main():

    if 'xcat1' in mode: tvp()
    elif 'xcat2' in mode: eska()
    elif 'xcat3' in mode: looknij()
    elif 'xcat4' in mode: telewizja()
    elif 'xcat5' in mode: filmboxlive()
    elif 'xcat6' in mode: lokalna()
    else:
        addDir('  Telewizja  ', 'plugin://wtyczka.telewizja.polska/?xcat4x', icontv)
        addDir('FilmBox Live', 'plugin://wtyczka.telewizja.polska/?xcat5x', xbmc.translatePath( os.path.join( obrazy, 'filmboxlive.png' ) ) )
#        addDir('Looknij.tv', 'plugin://wtyczka.telewizja.polska/?xcat3', icon)
        addDir('Eska GO', 'plugin://wtyczka.telewizja.polska/?xcat2x', eskaicon)
        addDir('Audycje TVP', 'plugin://wtyczka.telewizja.polska/?xcat1x', tvpicon)
        addDir('Lokalna TV', 'plugin://wtyczka.telewizja.polska/?xcat6x', tvpregionalna)

        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        sys.exit(0)
    
def addLink(name,url,iconimage):
        ok=True
        if 'looknij.tv' in url: url = 'plugin://wtyczka.telewizja.polska/?runstream=' + url + '***' + name + '***' + iconimage	
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
# tło        liz.setProperty( "Fanart_Image", iconimage )
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

#####################################################################################################

def tvp():
    link = get_url()
    for i in link:
        url = 'plugin://wtyczka.telewizja.polska/?runstream=' + i[0] + '***' + i[1] + '***' + i[2]
        addLink(i[1],url,i[2])
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    sys.exit(0)

def looknij():
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
    addLink("FilmBox Extra HD           ", "http://spi-live.ercdn.net/spi/smil:filmboxhd_pl_0.smil/chunklist_b1800000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", icontest) 
    addLink("FilmBox Action HD          ", "http://inea.live.e238-po.insyscd.net/filmboxaction.smil/chunklist_.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", icontest)
    addLink("FightBox HD                ", "http://spi-live.ercdn.net/spi/smil:fightboxhd_1.smil/chunklist_b1800000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", icontest) 
    addLink("Kino Polska                ", "http://spi-live.ercdn.net/spi/smil:kinopolskahd_international_0.smil/chunklist_b1200000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", icontest) 
    addLink("Kino Polska Muzyka         ", "http://spi-live.ercdn.net/spi/smil:kinopolskamuzikasd_international_0.smil/chunklist_b800000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", icontest) 
    addLink("ArtHouse HD [COLOR ff2e2e1e][I](napisy)[/I][/COLOR]    ", "http://spi-live.ercdn.net/spi/smil:fbarthousesd_pl_0.smil/chunklist_b800000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", icontest) 
    addLink("DocuBox HD                 ", "http://spi-live.ercdn.net/spi/smil:docuboxhd_0.smil/chunklist_b1600000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", icontest) 
    addLink("FasionBox HD", "http://spi-live.ercdn.net/spi/smil:fashionboxhd_0.smil/chunklist_b1600000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", icontest) 
    addLink("360TuneBox HD              ", "http://spi-live.ercdn.net/spi/smil:360tuneboxhd_0.smil/chunklist_b1600000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", icontest) 
    addLink("Fast'n'Fun HD              ", "http://spi-live.ercdn.net/spi/smil:fastnfunhd_0.smil/chunklist_b1200000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", icontest) 
    addLink("Madscreen                  ", "http://spi-live.ercdn.net/spi/smil:madscreen_0.smil/chunklist_b1800000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", icontest) 

    addLink("[LIGHT][COLOR ff2e2e1e][I]—< ALTERNATYWNE >———————————————————————————[/I][/COLOR][/LIGHT]",'none','none')

    addLink("[LIGHT]FilmBox Premium HD  [/LIGHT]", "http://inea.live.e238-po.insyscd.net/filmboxextra.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", icontest)
    addLink("[LIGHT]FilmBox Extra HD    [/LIGHT]", "http://inea.live.e238-po.insyscd.net/filmboxhd.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", icontest) 


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
    addLink("TVP Warszawa   [I](TVP Info)[/I]     ", "http://195.245.213.230/live/warszawa.isml/warszawa.m3u8 live=true", tvpregionalna) 
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

def telewizja():

    addLink("Fokus", "rtmp://stream.smcloud.net/live/fokustv live=true swfVfy=true pageUrl=", icontest) 
    addLink("Opoka.tv", "rtmp://153.19.248.4:1935/publishlive/Opokatv", icontest) 
    addLink("RBL.tv", "rtmp://153.19.248.4:1935/publishlive/rebeltv", icontest) 



    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    sys.exit(0)

main()




