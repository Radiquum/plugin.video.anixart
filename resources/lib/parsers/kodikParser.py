import sys
import requests
from bs4 import BeautifulSoup
import re
import json
import ast
import urllib.parse
import base64
import xbmcgui
import xbmcplugin


URL = sys.argv[0]
PLUGIN_URL = f"plugin://{sys.argv[0].split('/')[2]}"


def kodikAddQualitySources(url):
    links = fetchSourceUrls(url)
    for quality in links.keys():
        decryptedSrc = decryptSourceUrl(links[quality][0]['src'])
        # .replace(':hls:manifest.m3u8', '')
        url = f"{PLUGIN_URL}/play?{urllib.parse.urlencode({'url': decryptedSrc, 'player': 'kodik', 'action': 'play'})}"
        list_item = xbmcgui.ListItem(label=quality)
        list_item.setProperty('IsPlayable', 'True')
        xbmcplugin.addDirectoryItem(int(sys.argv[1]), url, list_item, False)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))


def fetchSourceUrls(releaseUrl):
    r = requests.get(releaseUrl)

    urlSplit = releaseUrl.replace("https://aniqit.com/", "").split("/")
    soup = BeautifulSoup(r.text, "html.parser")
    script = soup.find("script")

    # FROM PAGE
    # d={domain}
    # d_sign={domain_sign}
    # pd={player_domain}
    # pd_sign={player_domain_sign}
    # ref={referrer}
    # ref_sign={referrer_sign}

    # FROM URL
    # type={type}
    # hash={hash}
    # id={id}

    urlParamsPattern = re.compile(r'var (urlParams) = (.*);')

    if script:
        urlParamsMatch = urlParamsPattern.search(script.text)
        if urlParamsMatch:
            urlParams = ast.literal_eval(urlParamsMatch.group(2).rstrip())
            urlParams = json.loads(urlParams)
            urlParams["bad_user"] = False
            urlParams["cdn_is_working"] = True
            urlParams["type"] = urlSplit[0]
            urlParams["hash"] = urlSplit[2]
            urlParams["id"] = urlSplit[1]
    else:
        raise Exception("Script tag not found")

    # https://aniqit.com/ftor - endpoint to get sources urls
    r = requests.post("https://aniqit.com/ftor", data=urlParams)
    response = r.json()

    # { ..., links: {
    # 'quality': [
    #     {
    #         'src': 'encrypted m3u8 file source',
    #         'type': 'application/x-mpegURL'
    #     },...
    # ], ...},

    return response.get("links")


def decryptSourceUrl(encryptedSourceUrl):

    # Ported from kodik wrapper JavaScript source
    #
    # for (const [, sources] of Object.entries(links)) {
    #     for (const source of sources) {
    #         const decryptedBase64 = source.src.replace(/[a-zA-Z]/g, (e) => {
    #         let eCharCode = e.charCodeAt(0);
    #         const zCharCode = "Z".charCodeAt(0);
    #         return String.fromCharCode(
    #             (eCharCode <= zCharCode ? 90 : 122) >= (eCharCode = eCharCode + 13)
    #             ? eCharCode
    #             : eCharCode - 26
    #         );
    #         });
    #         console.log(atob(decryptedBase64));
    #     }
    # }

    decrypted_base64 = ""
    zCharCode = ord('Z')
    NumbersCharCodes = [ord('1'), ord('2'), ord('3'), ord('4'), ord('5'), ord('6'), ord('7'), ord('8'), ord('9'), ord('0')]
    for c in encryptedSourceUrl:
        eCharCode = ord(c)
        if eCharCode in NumbersCharCodes:
            decrypted_base64 += chr(eCharCode)
            continue

        if eCharCode <= zCharCode: biggerCharCode = 90
        else: biggerCharCode = 122

        tCharCode = eCharCode + 13
        if biggerCharCode >= tCharCode: finCharCode = tCharCode
        else: finCharCode = tCharCode - 26

        decrypted_base64 += chr(finCharCode)

    return f"https:{base64.urlsafe_b64decode(decrypted_base64).decode('utf-8')}"