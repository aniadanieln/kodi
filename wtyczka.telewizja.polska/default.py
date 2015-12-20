# -*- coding: utf-8 -*-
#from __future__ import unicode_literals
 
import sys,xbmc,xbmcaddon
import resources.lib.requests as requests
import re,os,xbmcplugin,xbmcgui

addon_handle = int(sys.argv[1])
xbmcplugin.setContent(addon_handle, 'movies')
xbmc.executebuiltin('Container.SetViewMode(500)') # "Thumbnail" view
    
Addon = xbmcaddon.Addon('wtyczka.telewizja.polska')
home = Addon.getAddonInfo('path')

sys.path.append( xbmc.translatePath("special://home/addons/wtyczka.telewizja.polska/resources/lib") )
sys.path.append( xbmc.translatePath("special://home/addons/wtyczka.telewizja.polska/obrazy") )
sys.path.append( xbmc.translatePath("special://home/addons/wtyczka.telewizja.polska/host/strm") )
sys.path.append( os.path.join( Addon.getAddonInfo('path'), "host" ) )


if 'extrafanart' in sys.argv[2]: sys.exit(0)

if 'runstream' in sys.argv[2]:
    url = sys.argv[2].replace('?runstream=','')
    px = xbmc.translatePath("special://home/addons/wtyczka.telewizja.polska/resources/lib/zapping.py")
    xbmc.executebuiltin('RunScript('+px+',url='+url+')')
    sys.exit(0)

icon = xbmc.translatePath( os.path.join( home, 'icon.png' ) )
iconimage = icon
eskaicon = xbmc.translatePath( os.path.join( home, 'resources/lib/eska.png' ) )
eskaricon = xbmc.translatePath( os.path.join( home, 'resources/lib/eskar.png' ) )
net = xbmc.translatePath( os.path.join( home, 'resources/lib/net.png') )
telewizjada = xbmc.translatePath('special://home/addons/wtyczka.telewizja.polska/host/strm/')
update = xbmc.translatePath( os.path.join( home, 'host/update.bat' ) )

fanart = xbmc.translatePath( os.path.join( home, 'fanart.jpg' ) )

xbmcPlayer = xbmc.Player()
playList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
mode = sys.argv[2]
####################### TEST Ikon TV ################
dodatki = 'https://raw.githubusercontent.com/neopack1/kodi/master/dodatki/'
tv = 'https://raw.githubusercontent.com/neopack1/kodi/master/dodatki/logo_tv/'
radio = 'https://raw.githubusercontent.com/neopack1/kodi/master/dodatki/logo_radio/'
images = 'https://raw.githubusercontent.com/neopack1/kodi/master/dodatki/images/'

defaultvideo = images+'defaultvideo.png'
play = images+'play.png'

#xbmc.executebuiltin('XBMC.Notification('+idx[1]+' , Aktualnie odtwarzana audycja ,20000,'+idx[2]+')')


def main():

    if 'xcat1' in mode: tvp()
    elif 'xcat2' in mode: eska()
    elif 'xcat3' in mode: looknij()
    elif 'xcat4' in mode: telewizja()
    elif 'xcat5' in mode: filmboxlive()
    elif 'xcat6' in mode: lokalna()
    elif 'xcat7' in mode: itivi()
    elif 'xcat8' in mode: youtube()
    elif 'xcat9' in mode: telewizjada()
    else:
        addDir('[COLOR gold][B] Telewizjada [/B][/COLOR][CR](testy)', 'plugin://wtyczka.telewizja.polska/?xcat9x', images+'dir_telewizjada.png')
        addDir('[B] Telewizja [/B]', 'plugin://wtyczka.telewizja.polska/?xcat4x', images+'dir_tv.png')
        addDir('[B]FilmBox[/B][CR][COLOR red] Live [/COLOR] ', 'plugin://wtyczka.telewizja.polska/?xcat5x', images+'dir_filmboxlive.png' )
        addDir('[B]ITIVI[/B][CR]Telewizja Internetowa', 'plugin://wtyczka.telewizja.polska/?xcat7x', images+'dir_itivi.png')
        addDir(' Looknij TV ', 'plugin://wtyczka.telewizja.polska/?xcat3', images+'dir_looknijtv.png' )
        addDir(' Eska GO ', 'plugin://wtyczka.telewizja.polska/?xcat2x', images+'dir_eskago.png')
        addDir('TVP[CR]Stream', 'plugin://wtyczka.telewizja.polska/?xcat1x', images+'dir_tvpstream.png')
        addDir('Telewizja[CR]Lokalna', 'plugin://wtyczka.telewizja.polska/?xcat6x', images+'dir_tvlokalna.png')
        addDir('[B][COLOR white]You[/COLOR][COLOR red]Tube[/COLOR][/B][CR]Kanały', 'plugin://wtyczka.telewizja.polska/?xcat8x', images+'dir_youtube.png')
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
        sys.exit(0)
    
def addLink(name,url,iconimage):
        ok=True
        if 'looknij.tv' in url: url = 'plugin://wtyczka.telewizja.polska/?runstream=' + url + '***' + name + '***' + iconimage	
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty( "Fanart_Image", fanart )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,iconimage):
    print iconimage
    liz=xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setProperty( "Fanart_Image", fanart )
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

    addLink("TVP 1","http://looknij.tv/?port=Tvp1",tv+'tvp_1.png')
    addLink("TVP 2","http://looknij.tv/?port=Tvp-2",tv+'tvp_2.png')
    addLink("TVP Info","http://looknij.tv/?port=tvp-info",tv+'tvp_info.png')
    addLink("TVP Seriale","http://looknij.tv/?port=tvp-seriale",tv+'tvp_seriale.png')
    addLink("TVP Sport","http://looknij.tv/?port=tvp-sport",tv+'tvp_sport.png')
    addLink("TTV","http://looknij.tv/?port=ttv",tv+'ttv.png')
    addLink("TVN","http://looknij.tv/?port=tvn",tv+'tvn.png')
    addLink("TVN 24","http://looknij.tv/?port=tvn-24",tv+'tvn_24.png')
    addLink("TVN Turbo","http://looknij.tv/?port=tvn-turbo",tv+'tvn_turbo.png')
    addLink("TVN Style","http://looknij.tv/?port=tvn-style",tv+'tvn_style.png')
    addLink("Canal+","http://looknij.tv/?port=canal",tv+'canal_plus.png')
    addLink("Canal+ Sport","http://looknij.tv/?port=canal-sport",tv+'canal_plus_sport.png')
    addLink("Eurosport","http://looknij.tv/?port=eurosport",tv+'eurosport.png')
    addLink("Eurosport 2","http://looknij.tv/?port=eurosport-2",tv+'eurosport_2.png')
    addLink("Eleven","http://looknij.tv/?port=eleven",tv+'eleven.png')
    addLink("Eleven Sports","http://looknij.tv/?port=11-sport",tv+'eleven_sports.png')
    addLink("Orange Sport","http://looknij.tv/?port=orange-sport",tv+'orange_sport.png')
    addLink("nSport+","http://looknij.tv/?port=n-sport",tv+'nsport_plus.png')
    addLink("FOX Comedy","http://looknij.tv/?port=fox-comedy",tv+'fox_comedy.png')
    addLink("Disney Channel","http://looknij.tv/?port=disney-channel",tv+'disney_channel.png')
    addLink("AXN","http://looknij.tv/?port=axn",tv+'axn.png')
    addLink("AXN White","http://looknij.tv/?port=axn-white",tv+'axn_white.png')
    addLink("AXN Black","http://looknij.tv/?port=axn-black",tv+'axn_black.png')
    addLink("Domo+","http://looknij.tv/?port=domo",tv+'domo_plus.png')
    addLink("National Geographic","http://looknij.tv/?port=national-geographic",tv+'national_geographic.png')
    addLink("Discovery","http://looknij.tv/?port=discovery",tv+'discovery_channel.png')
    addLink("HBO","http://looknij.tv/?port=hbo",tv+'hbo.png')
    addLink("HBO 2","http://looknij.tv/?port=hbo-2",tv+'hbo_2.png')
    addLink("HBO Comedy","http://looknij.tv/?port=hbo-comedy",tv+'hbo_comedy.png')
    addLink("Cinemax","http://looknij.tv/?port=cinemax-2",tv+'cinemax.png') 

    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    sys.exit(0)

############################################################################################################

def eska():
# tv
    addLink("Eska TV", "rtmp://stream.smcloud.net/live2/eskatv/eskatv_480p", eskaicon)
    addLink("Eska Best Music HD", "rtmp://stream.smcloud.net/live2/best/best_720p", eskaicon) 
    addLink("Eska Party HD","rtmp://stream.smcloud.net/live2/eska_party/eska_party_720p live=1",eskaicon)
    addLink("Eska Rock HD","rtmp://stream.smcloud.net/live2/eska_rock/eska_rock_720p live=1",eskaicon)
    addLink("Eska Polo Party HD", "rtmp://stream.smcloud.net/live2/polo_party/polo_party_720p", eskaicon) 
    addLink("VOX Music TV", "rtmp://stream.smcloud.net/live/vox2/stream1", eskaicon) 
    addLink("VOX Old's Cool HD", "rtmp://stream.smcloud.net/live2/vox/vox_720p", eskaicon) 
    addLink("WaWa HD", "rtmp://stream.smcloud.net/live2/wawa/wawa_720p", eskaicon) 
    addLink("Polo TV","rtmp://stream.smcloud.net/live/polotv",eskaicon)
# radio
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

    addLink("FilmBox                    ", "http://spi-live.ercdn.net/spi/smil:filmboxbasicsd_pl_0.smil/chunklist_b800000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", tv+'filmbox.png') 
    addLink("FilmBox Premium HD         ", "http://spi-live.ercdn.net/spi/smil:filmboxextrasd_pl_0.smil/chunklist_b800000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", tv+'filmbox_premium.png') 
    addLink("FilmBox Premium HD         ", "http://inea.live.e238-po.insyscd.net/filmboxextra.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", tv+'filmbox_premium.png')
    addLink("FilmBox Extra HD           ", "http://inea.live.e238-po.insyscd.net/filmboxhd.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", tv+'filmbox_extra.png') 
    addLink("FilmBox Extra HD           ", "http://spi-live.ercdn.net/spi/smil:filmboxhd_pl_0.smil/chunklist_b1800000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", tv+'filmbox_extra.png') 
    addLink("FilmBox Action HD          ", "http://inea.live.e238-po.insyscd.net/filmboxaction.smil/chunklist_.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", tv+'filmbox_action.png')
    addLink("FilmBox Family HD          ", "http://inea.live.e238-po.insyscd.net/filmboxfamily.smil/chunklist_b2400000.m3u8", tv+'filmbox_family.png')
    addLink("FightBox HD                ", "http://spi-live.ercdn.net/spi/smil:fightboxhd_1.smil/chunklist_b1800000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", tv+'fightbox.png') 
    addLink("Kino Polska                ", "http://spi-live.ercdn.net/spi/smil:kinopolskahd_international_0.smil/chunklist_b1200000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", tv+'kino_polska.png') 
    addLink("Kino Polska HD             ", "http://inea.live.e238-po.insyscd.net/kinopolska.smil/chunklist_.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", tv+'kino_polska.png') 
    addLink("Kino Polska Muzyka         ", "http://spi-live.ercdn.net/spi/smil:kinopolskamuzikasd_international_0.smil/chunklist_b800000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", tv+'kino_polska_muzyka.png') 
    addLink("ArtHouse HD                ", "http://spi-live.ercdn.net/spi/smil:fbarthousesd_pl_0.smil/chunklist_b800000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", tv+'FilmBox_Arthouse.png') 
    addLink("DocuBox HD                 ", "http://spi-live.ercdn.net/spi/smil:docuboxhd_0.smil/chunklist_b1600000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", tv+'docubox.png') 
    addLink("FasionBox HD               ", "http://spi-live.ercdn.net/spi/smil:fashionboxhd_0.smil/chunklist_b1600000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", tv+'fasionbox.png') 
    addLink("360TuneBox HD              ", "http://spi-live.ercdn.net/spi/smil:360tuneboxhd_0.smil/chunklist_b1600000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", tv+'360_tunebox.png') 
    addLink("Fast'n'Fun HD              ", "http://spi-live.ercdn.net/spi/smil:fastnfunhd_0.smil/chunklist_b1200000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", tv+'fastandfunbox.png') 
    addLink("Madscreen                  ", "http://spi-live.ercdn.net/spi/smil:madscreen_0.smil/chunklist_b1800000.m3u8|User-Agent=Mozilla%2f5.0+(iPad%3b+CPU+OS+6_0+like+Mac+OS+X)+AppleWebKit%2f536.26+(KHTML%2c+?like+Gecko)+Version%2f6.0+Mobile%2f10A5355d+Safari%2f8536.25", tv+'madscreen.png') 

    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    sys.exit(0)

##############################################################################################################
def lokalna():

    addLink("TV Kujawy          ", "rtmp://stream.tvkujawy.pl/live/broadcast live=true", defaultvideo) 
    addLink("Stella             ", "rtmp://live-tvk.tvkstella.pl/flvplayback playpath=StellaLive swfUrl=http://www.tvkstella.pl/flowplayer-3.2.7.swf pageUrl=http://www.tvkstella.pl/live_tv live=true swfVfy=true live=true", defaultvideo) 
    addLink("WTK                ", "http://wtk.live-ext.e96-jw.insyscd.net/wtk.smil/playlist.m3u8 live=true", defaultvideo) 
    addLink("CW24TV             ", "rtmp://cdn4.stream360.pl:1935/CW24/transmisja_live live=true", defaultvideo) 
    addLink("Pomerania          ", "rtmp://153.19.248.4:1935/publishlive/pomeraniatv", defaultvideo) 
    addLink("Lech TV            ", "http://wtk.live-ext.e96-jw.insyscd.net/lechtv.smil/playlist.m3u8 live=true", defaultvideo) 
    addLink("Pomorska TV        ", "rtmp://stream.trefl.com/livepkgr/ playpath=livestream_2 swfUrl=http://pomorska.tv/player/jwplayer.flash.swf pageUrl=http://pomorska.tv/livestream live=true swfVfy=true live=true", defaultvideo) 
    addLink("Tawizja            ", "rtmp://w-stream2.4vod.tv:1935/lduitv/ playpath=lduitv.stream swfUrl=http://www.tawizja.pl/video/lduflash.swf pageUrl=http://www.tawizja.pl/video/program-emisja-na-zywo.htm live=true swfVfy=true live=true", defaultvideo) 
    addLink("TVP Warszawa       ", "http://195.245.213.230/live/warszawa2.isml/warszawa2.m3u8 live=true", tv+'tvp_warszawa.png') 
    addLink("TVP Bialystok      ", "http://195.245.213.230/live/bialystok.isml/bialystok.m3u8 live=true", tv+'tvp_regionalna.png') 
    addLink("TVP Bydgoszcz      ", "http://195.245.213.230/live/bydgoszcz.isml/bydgoszcz.m3u8 live=true", tv+'tvp_regionalna.png') 
    addLink("TVP Gdansk         ", "http://195.245.213.230/live/gdansk.isml/gdansk.m3u8 live=true", tv+'tvp_regionalna.png') 
    addLink("TVP Gorzow Wlkp.   ", "http://195.245.213.230/live/gorzow.isml/gorzow.m3u8 live=true", tv+'tvp_regionalna.png') 
    addLink("TVP Katowice       ", "http://195.245.213.230/live/katowice.isml/katowice.m3u8 live=true", tv+'tvp_regionalna.png') 
    addLink("TVP Kielce         ", "http://195.245.213.230/live/kielce.isml/kielce.m3u8 live=true", tv+'tvp_regionalna.png') 
    addLink("TVP Krakow         ", "http://195.245.213.230/live/krakow.isml/krakow.m3u8 live=true", tv+'tvp_regionalna.png') 
    addLink("TVP Lublin         ", "http://195.245.213.230/live/lublin.isml/lublin.m3u8 live=true", tv+'tvp_regionalna.png') 
    addLink("TVP Lodz           ", "http://195.245.213.230/live/lodz.isml/lodz.m3u8 live=true", tv+'tvp_regionalna.png') 
    addLink("TVP Olsztyn        ", "http://195.245.213.230/live/olsztyn.isml/olsztyn.m3u8 live=true", tv+'tvp_regionalna.png') 
    addLink("TVP Opole          ", "http://195.245.213.230/live/opole.isml/opole.m3u8 live=true", tv+'tvp_regionalna.png') 
    addLink("TVP Poznan         ", "http://195.245.213.230/live/poznan.isml/poznan.m3u8 live=true", tv+'tvp_regionalna.png') 
    addLink("TVP Rzeszow        ", "http://195.245.213.230/live/rzeszow.isml/rzeszow.m3u8 live=true", tv+'tvp_regionalna.png') 
    addLink("TVP Szczecin       ", "http://195.245.213.230/live/szczecin.isml/szczecin.m3u8 live=true", tv+'tvp_regionalna.png') 
    addLink("TVP Wroclaw        ", "http://195.245.213.230/live/wroclaw.isml/wroclaw.m3u8 live=true", tv+'tvp_regionalna.png') 


    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    sys.exit(0)
########################################################################################################
def zagraniczne():
    addLink("abc News [USA]", "http://abclive.abcnews.com/i/abc_live4@136330/index_1200_av-b.m3u8?=key live=true", icon) 
    addLink("CBS News [USA] [I]FullHD[/I]", "http://cbsnewshd-lh.akamaihd.net/i/CBSNDC_4@199302/index_4000_av-b.m3u8?sd=10&rebase=on live=true", icon) 
    addLink("Global [CAN]", "https://glblvestu-f.akamaihd.net/i/glblvestu_1@78149/master.m3u8?__b__=900&hdnea=ip=99.18.68.202~st=1434303944~exp=1434304544~acl=/i/*~id=3f0edb02-c4e5-4596-8950-4331b8ce1baf~hmac=4acbecb511f7c3beaf085123ab9097c7a6acbd5d857fd4cefbfdfb733b666f57 live=true", icon) 
    addLink("Weather Nation [USA]", "http://cdnapi.kaltura.com/p/931702/sp/93170200/playManifest/entryId/1_oorxcge2/format/applehttp/protocol/http/uiConfId/28428751/a.m3u8?key= live=true", icon) 
    addLink("ARD [GR]", "http://daserste_live-lh.akamaihd.net/i/daserste_de@91204/master.m3u8?=key live=true", icon) 
    addLink("abc News [USA]", "http://abclive.abcnews.com/i/abc_live4@136330/index_1200_av-b.m3u8?=key live=true", icon) 
    addLink("CBS News [USA] [I]FullHD[/I]", "http://cbsnewshd-lh.akamaihd.net/i/CBSNDC_4@199302/index_4000_av-b.m3u8?sd=10&rebase=on live=true", icon) 
    addLink("Global [CAN]", "https://glblvestu-f.akamaihd.net/i/glblvestu_1@78149/master.m3u8?__b__=900&hdnea=ip=99.18.68.202~st=1434303944~exp=1434304544~acl=/i/*~id=3f0edb02-c4e5-4596-8950-4331b8ce1baf~hmac=4acbecb511f7c3beaf085123ab9097c7a6acbd5d857fd4cefbfdfb733b666f57 live=true", icon) 
    addLink("Weather Nation [USA]", "http://cdnapi.kaltura.com/p/931702/sp/93170200/playManifest/entryId/1_oorxcge2/format/applehttp/protocol/http/uiConfId/28428751/a.m3u8?key= live=true", icon) 
    addLink("ARD [GER]", "http://daserste_live-lh.akamaihd.net/i/daserste_de@91204/master.m3u8?=key live=true", icon) 


    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    sys.exit(0)

########################################################################################################
def telewizja():

    addLink("4fun TV","rtmp://edge4.popler.tv:1935/publishlive?play=123452/4funtv live=1 swfUrl=http://images.popler.tv/player/flowplayer.commercial.swf pageUrl=http://www.popler.tv/live/4funtv",tv+'4_fun_tv.png')
#C
    addLink("Czwórka Polskie Radio", "rtmp://stream85.polskieradio.pl/video/czworka.sdp", radio+'pr4.png')
#D
    addLink("Discovery [I]HD[/I]", "http://inea.live.e238-po.insyscd.net/discoverychannelhd.smil/chunklist_b2400000.m3u8", tv+'discovery_channel.png')
    addLink("Discovery ID [I]HD[/I]", "http://inea.live.e238-po.insyscd.net/id.smil/chunklist_.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", tv+'id.png') 
    addLink("Discovery Life [I]HD[/I]", "http://inea.live.e238-po.insyscd.net/animalplanet.smil/chunklist_.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", tv+'discovery_life.png') 
    addLink("Discovery Science [I]HD[/I]", "http://inea.live.e238-po.insyscd.net/discoveryscience.smil/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", tv+'discovery_science.png') 
    addLink("Discovery Turbo Xtra [I]HD[/I]", "http://inea.live.e238-po.insyscd.net/dtx.smil/chunklist_.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", tv+'discovery_turbo_xtra.png') 

#E
    addLink("Edusat", "rtmp://178.73.10.66:1935/live/mpegts.stream", tv+'edusat.png')
    addLink("Eurosport [I]HD[/I]", "http://inea.live.e238-po.insyscd.net/eurosport.smil/chunklist_b2400000.m3u8", tv+'eurosport.png')
    addLink("Eurosport 2 [I]HD[/I]", "http://inea.live.e238-po.insyscd.net/eurosport2hd.smil/chunklist_b2400000.m3u8", tv+'eurosport_2.png')

#F
    addLink("Fokus", "rtmp://stream.smcloud.net/live/fokustv live=true swfVfy=true pageUrl=", tv+'fokus.png') 

#H


#K
    addLink("Kino Polska [I]HD[/I]", "http://inea.live.e238-po.insyscd.net/kinopolska.smil/chunklist_.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", tv+'kino_polska.png') 

#M
    addLink("Mango24", "rtmp://stream.mango.pl/rtplive playpath=live/1 swfUrl=http://tv.mango.pl/player.swf pageUrl=http://tv.mango.pl/ live=true swfVfy=true live=true", tv+'mango_24.png') 

#N
#    addLink("National Geographic", "rtmp://144.76.154.14/live playpath=nageo swfUrl= live=1 pageUrl= live=true", icon) 
    addLink("Nat Geo Wild [I]HD[/I]", "http://inea.live.e238-po.insyscd.net/natgeowildhd.smil/chunklist_.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", tv+'neo_geo_wild.png') 

#O

#P

    addLink("Polsat Sport News", "http://n-2-4.dcs.redcdn.pl/hls/o2/ATM-Lab/borys/MotoGP/live.livx/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", tv+'polsat_sport_news.png') 

#R
    addLink("RBL.tv", "rtmp://153.19.248.4:1935/publishlive/rebeltv", tv+'rbl.png') 
    addLink("Republika", "http://stream4.videostar.pl/999_tvrtest/smil:4321abr.ism/playlist.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", tv+'republika.png') 
    addLink("Republika [COLOR ff000055]stream 2[/COLOR]", "http://stream6.videostar.pl/999_tvrtest/smil:4321high.ism/playlist.m3u8?key= live=true", tv+'republika.png') 

#S
    addLink("Stars.tv", "http://starstv.live.e55-po.insyscd.net/starstvhd.smil/chunklist_.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", tv+'stars.png') 
    addLink("SuperStacja [I]HD[/I]", "http://inea.live.e238-po.insyscd.net/superstacja.smil/chunklist_.m3u8|User-Agent=Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", tv+'superstacja.png') 

#T
    addLink("TLC [I]HD[/I]", "http://inea.live.e238-po.insyscd.net/tlchd.smil/chunklist_b2400000.m3u8", tv+'tlc.png')
    addLink("Trwam", "http://trwamtv.live.e96-jw.insyscd.net/trwamtv.smil/playlist.m3u8 live=true", tv+'trwam.png') 
    addLink("TVP Info [I]HD[/I]   ", "http://195.245.213.230/live/warszawa.isml/warszawa.m3u8 live=true", tv+'tvp_info.png')
    addLink("TVP Seriale", "rtmp://144.76.154.14/live/tvpseriale live=true", tv+'tvp_seriale.png') 
    addLink("TVP Warszawa [I]HD[/I]", "http://195.245.213.230/live/warszawa2.isml/warszawa2.m3u8 live=true", tv+'tvp_warszawa.png') 


    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    sys.exit(0)
#########################################################################
######################################################################



def itivi():
    addLink("TVP1","rtmp://weeb.tv.itivi.pl/live/ playpath=RTS?user=demo&pass=demopassword swfUrl=http://itivi.pl/js/jwplayer-7.0.3/jwplayer.flash.swf pageUrl=http://itivi.pl/program-telewizyjny/TVP_1_HD",tv+'tvp_1.png')
    addLink("TVP2","rtmp://weeb.tv.itivi.pl/live/ playpath=SXT2?user=demo&pass=demopassword swfUrl=http://itivi.pl/js/jwplayer-7.0.3/jwplayer.flash.swf pageUrl=http://itivi.pl/program-telewizyjny/TVP_2",tv+'tvp_2.png')
    addLink("TVN","rtmp://weeb.tv.itivi.pl/live/ playpath=S2T2?user=demo&pass=demopassword swfUrl=http://itivi.pl/js/jwplayer-7.0.3/jwplayer.flash.swf pageUrl=http://itivi.pl/program-telewizyjny/TVN",tv+'tvn.png')
    addLink("TVN24","rtmp://weeb.tv.itivi.pl/live/ playpath=CH1?user=demo&pass=demopassword swfUrl=http://itivi.pl/js/jwplayer-7.0.3/jwplayer.flash.swf pageUrl=http://itivi.pl/program-telewizyjny/TVN24_",tv+'tvn_24.png')
    addLink("Polsat 2","rtmp://weeb.tv.itivi.pl/live/ playpath=POL2PL?user=demo&pass=demopassword swfUrl=http://itivi.pl/js/jwplayer-7.0.3/jwplayer.flash.swf pageUrl=http://itivi.pl/program-telewizyjny/POLSAT_2",tv+'polsat_2.png')
    addLink("Discovery","rtmp://weeb.tv.itivi.pl/live/ playpath=CHDN?user=demo&pass=demopassword swfUrl=http://itivi.pl/js/jwplayer-7.0.3/jwplayer.flash.swf pageUrl=http://itivi.pl/program-telewizyjny/Discovery_Channel",tv+'discovery_channel.png')
    addLink("HBO Comedy","rtmp://weeb.tv.itivi.pl/live/ playpath=CHA2?user=demo&pass=demopassword swfUrl=http://itivi.pl/js/jwplayer-7.0.3/jwplayer.flash.swf pageUrl=http://itivi.pl/program-telewizyjny/HBO_COMEDY",tv+'hbo_comedy.png')
    addLink("TVP Seriale","rtmp://weeb.tv.itivi.pl/live/ playpath=CH1TSC?user=demo&pass=demopassword swfUrl=http://itivi.pl/js/jwplayer-7.0.3/jwplayer.flash.swf pageUrl=http://itivi.pl/program-telewizyjny/TVP_SERIALE",tv+'tvp_seriale.png')
    addLink("Kino Polska","rtmp://weeb.tv.itivi.pl/live/ playpath=CH304?user=demo&pass=demopassword swfUrl=http://itivi.pl/js/jwplayer-7.0.3/jwplayer.flash.swf pageUrl=http://itivi.pl/program-telewizyjny/KINO_POLSKA",tv+'kino_polska.png')
    addLink("National Geographic","rtmp://weeb.tv.itivi.pl/live/ playpath=S323?user=demo&pass=demopassword swfUrl=http://itivi.pl/js/jwplayer-7.0.3/jwplayer.flash.swf pageUrl=http://itivi.pl/program-telewizyjny/NATGEO_PL",tv+'national_geographic.png')
    addLink("Eurosport","rtmp://weeb.tv.itivi.pl/live/ playpath=CH174?user=demo&pass=demopassword swfUrl=http://itivi.pl/js/jwplayer-7.0.3/jwplayer.flash.swf pageUrl=http://itivi.pl/program-telewizyjny/EURO_SPORT",tv+'eurosport.png')
    addLink("AXN","rtmp://weeb.tv.itivi.pl/live/ playpath=CHA1?user=demo&pass=demopassword swfUrl=http://itivi.pl/js/jwplayer-7.0.3/jwplayer.flash.swf pageUrl=http://itivi.pl/program-telewizyjny/AXN_HD",tv+'axn.png')
    addLink("nSport+","rtmp://weeb.tv.itivi.pl/live/ playpath=CH500?user=demo&pass=demopassword swfUrl=http://itivi.pl/js/jwplayer-7.0.3/jwplayer.flash.swf pageUrl=http://itivi.pl/program-telewizyjny/NSPORT_HD",tv+'nsport_plus.png')
    addLink("MTV Polska","rtmp://weeb.tv.itivi.pl/live/ playpath=CH3?user=demo&pass=demopassword swfUrl=http://itivi.pl/js/jwplayer-7.0.3/jwplayer.flash.swf pageUrl=http://itivi.pl/program-telewizyjny/MTV_POLSKA",tv+'mtv.png')
    addLink("FilBox Premium","rtmp://51.255.51.111/live/ playpath=S1 swfUrl=http://itivi.pl/js/jwplayer-7.0.3/jwplayer.flash.swf pageUrl=http://itivi.pl/program-telewizyjny/FILMBOX_PREMIUM",tv+'filmbox_premium.png')
    addLink("Moto Wizja","rtmp://weeb.tv.itivi.pl/live/ playpath=CH10?user=demo&pass=demopassword swfUrl=http://itivi.pl/js/jwplayer-7.0.3/jwplayer.flash.swf pageUrl=http://itivi.pl/program-telewizyjny/MOTOWIZJA",tv+'moto_wizja.png')
    addLink("Cinemax","rtmp://weeb.tv.itivi.pl/live/ playpath=CH8?user=demo&pass=demopassword swfUrl=http://itivi.pl/js/jwplayer-7.0.3/jwplayer.flash.swf pageUrl=http://itivi.pl/program-telewizyjny/CINEMAX_HD",tv+'cinemax.png')
    addLink("HBO","rtmp://weeb.tv.itivi.pl/live/ playpath=CH7?user=demo&pass=demopassword swfUrl=http://itivi.pl/js/jwplayer-7.0.3/jwplayer.flash.swf pageUrl=http://itivi.pl/program-telewizyjny/HBO_HD",tv+'hbo.png')
    addLink("TVN Turbo","rtmp://weeb.tv.itivi.pl/live/ playpath=CH6?user=demo&pass=demopassword swfUrl=http://itivi.pl/js/jwplayer-7.0.3/jwplayer.flash.swf pageUrl=http://itivi.pl/program-telewizyjny/TVN_TURBO",tv+'tvn_turbo.png')
    addLink("Discovery Historia","rtmp://weeb.tv.itivi.pl/live/ playpath=CH5?user=demo&pass=demopassword swfUrl=http://itivi.pl/js/jwplayer-7.0.3/jwplayer.flash.swf pageUrl=http://itivi.pl/program-telewizyjny/DISCOVERY_HISTORIA",tv+'discovery_historia.png')
    addLink("Polsat","rtmp://weeb.tv.itivi.pl/live/ playpath=SPL?user=demo&pass=demopassword swfUrl=http://itivi.pl/js/jwplayer-7.0.3/jwplayer.flash.swf pageUrl=http://itivi.pl/program-telewizyjny/POLSAT_HD",tv+'polsat.png')

    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    sys.exit(0)

def telewizjada():
    xbmc.executebuiltin("Notification([COLOR red]Uruchom UPDATE.EXE[/COLOR],UPDATE.EXE znajdziesz w katalogu 'host' wtyczki, 10000)")

    addLink("13 Ulica",'special://home/addons/wtyczka.telewizja.polska/host/strm/13_ulica.strm', tv+'13_ulica.png')
    addLink("Polsat Sport",'special://home/addons/wtyczka.telewizja.polska/host/strm/polsat_sport.strm', tv+'polsat_sport.png')
    addLink("Polsat Sport Extra",'special://home/addons/wtyczka.telewizja.polska/host/strm/polsat_sport_extra.strm', tv+'polsat_sport_extra.png')
                            
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    sys.exit(0)
    
def youtube():

    xbmc.executebuiltin('Container.SetViewMode(500)') # "Thumbnail" view
    addDir('Blok Ekipa', 'plugin://plugin.video.youtube/channel/UCxJDH_2HXzwUtT62HgWJqCg/playlist/PLdhsyudOIKSbc-Hx6JWgKgrC8GtVV2Zl-/', images+'blok_ekipa.png')
    addDir(' iTVP ', 'plugin://plugin.video.youtube/channel/UC03sVDw-tRhwDuQACRFBpGw/playlists/', images+'dir_itvp.png')
    

    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    sys.exit(0)
    
    
main()