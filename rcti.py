#!/usr/bin/python3

# RCTI+ API Python
# Created by:  @halakkita

from requests.packages import urllib3
import requests
import argparse
import base64
import re
import os
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

parser = argparse.ArgumentParser()
parser.add_argument("-n", "--channel-name", required=True, help="channel name")
parser.add_argument("output", nargs="?", help="output file")
args = parser.parse_args()

rplus_url = 'https://video.sindonews.com/tv/'
windows = False
if 'win' in sys.platform:
    windows = True

def getipaddr():
    get = requests.get('http://checkip.dyndns.com/')
    regex = re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)')
    return regex.search(str(get.text)).group(1)

def nosignal():
    url = 'https://raw.githubusercontent.com/halakkitach/ONLINE/master/erorya/1infoku.m3u8'
    m3u8_get = requests.get(f"{url}/index.m3u8").text
    for ts in ['01.m3u8', '02.m3u8']:
        m3u8_get = m3u8_get.replace(ts, f"{url}/{ts}")
    return m3u8_get

def grab(name):
    headers = {}
    headers['Accept'] = '*/*';
    headers['X-Forwarded-For'] = getipaddr()
    headers['Accept-Language'] = 'en-US,en;q=0.5'
    headers['Origin'] = f'https://www.{rplus_url}/'
    headers['DNT'] = '1'
    headers['Referer'] = f'https://embed.{rplus_url}/'
    headers['Access-Control-Allow-Origin'] = '*'
    headers['Access-Control-Allow-Headers'] = 'content-type'

    try:
        get = s.get(f"https://embed.{rplus_url}/live/{name}/inewsid", headers=headers, verify=False)

        findstr = r'(aHR0cHM6[-A-Z0-9+&@#\/%=~_|$?!:,.]*[A-Z0-9+&@#\/%=~_|$])'
        regex = re.compile(findstr, re.IGNORECASE)
        match = regex.findall(get.text)[0]
        decode = base64.b64decode(match).decode()

        http_parse = decode.split('://')
        url_parse = http_parse[1].split('/')[0]

        if '?' not in decode:
            return nosignal()
        else:
            headers = {}
            headers['Accept'] = '*/*';
            headers['X-Forwarded-For'] = getipaddr()
            headers['Accept-Language'] = 'en-US,en;q=0.5'
            headers['Origin'] = f'https://www.{rplus_url}/'
            headers['DNT'] = '1'
            headers['Referer'] = f'https://www.{rplus_url}/'
            headers['Access-Control-Allow-Origin'] = '*'
            headers['Access-Control-Allow-Headers'] = 'content-type'

            result = s.get(decode, headers=headers, verify=False).text
            repl = fr'{http_parse[0]}://{url_parse}/\1.m3u8'
            regex = re.compile(r'(.*).m3u8')
            return regex.sub(repl, result)
    except:
        return nosignal()

def gotresult(result):
    if args.output:
        open(args.output, "w").write(result)
    else:
        print(result)

for channel in \
    "rcti",    \
    "mnctv",   \
    "gtv",     \
    "inews":
    if args.channel_name == channel:
        nochannel = False
        break
    else:
        nochannel = True

if nochannel:
   gotresult(nosignal())
else:
   s = requests.Session()
   gotresult(grab(args.channel_name))
