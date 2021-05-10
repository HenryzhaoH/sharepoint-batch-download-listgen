#!/usr/bin/env python3 

###
# Generate Aria2 batch download list for SharePoint Links w/folder structure.
# 
# Author: Henryzhao
# Date:   2020/03/14
# 
# How to get the Real Path:
# 1. Open the SharePoint link in web browser.
# 2. Open DevTools -> Network tab and then reload the page.
# 3. Filter out 'RenderListDataAsStream' XHR request(s).
# 4. Copy the Real Path from '@a1' or '@listUrl' query parameter (without quotes).
#    (eg. /personal/aaaa_t_cccc_cn/Documents/)
# 5. Concat the host and the path. 
#    (eg. https://xxxx-my.sharepoint.com/personal/aaaa_t_cccc_cn/Documents/)
# 
# How to get FedAuth cookie:
# 1. Open the SharePoint link in web browser.
# 2. Open DevTools -> Network tab and then reload the page.
# 3. Locate the very first request after reloading or requests to your SharePoint 
#    domain.
# 4. Find either 'Cookie: FedAuth=' or 'Set-Cookie: FedAuth='.
# 5. Copy the text after 'Auth=' till the first semicolon(;).
# 
# Enjoy!
# 

import requests
import xml.etree.ElementTree as ElementTree
from urllib.parse import urlparse,quote,unquote

ARIA2_INPUT_FILE = 'aria2-links.txt'
DLPATH_PRIFIX = 'Downloads/'

COOKIE_FEDAUTH = None
SHAREPOINT_ROOT = None
SESSION = requests.Session()

def main():
    global COOKIE_FEDAUTH, SHAREPOINT_ROOT, SESSION, DLPATH_PRIFIX
    SHAREPOINT_ROOT = input("SharePoint Real Path (eg. https://xxxx-my.sharepoint.com/personal/aaaa_t_cccc_cn/Documents/):\n")
    SHAREPOINT_PATH = urlparse(SHAREPOINT_ROOT).path

    COOKIE_FEDAUTH = input("FedAuth cookie (base64 value only):\n")
    cookies={
        'FedAuth': COOKIE_FEDAUTH
    }
    requests.utils.add_dict_to_cookiejar(SESSION.cookies, cookies)

    download_dir = input("Download path (Default: Downloads/): ")
    if download_dir != '':
        DLPATH_PRIFIX = download_dir.rstrip('/') + '/'
    else:
        print(f"Using {DLPATH_PRIFIX}")
    
    print("Fetching file list ...")
    resp = SESSION.request("PROPFIND", SHAREPOINT_ROOT)
    try:
        xml_root = ElementTree.fromstring(resp.content.decode('utf8'))
    except ElementTree.ParseError:
        print(f"ERROR! Got Response <{resp.status_code}>: {resp.content.decode('utf8')}\nPossible invalid Real Path or FedAuth.")
        exit()

    print("Generating aria2 file list ...")
    fw = open(ARIA2_INPUT_FILE, 'w', encoding='utf-8')
    for e in xml_root.findall('.//{DAV:}href'):
        ''' Input file item:
        http://server/dir1/dir2/file.iso
          dir = dir1/dir2
        '''
        file_url = e.text
        if file_url.endswith('/'):
            continue
        url_info = urlparse(file_url)
        save_path = DLPATH_PRIFIX + "/".join(url_info.path.lstrip(SHAREPOINT_PATH).split('/')[:-1])
        save_path = unquote(save_path)
        encoded_url = url_info.geturl()
        fw.write(f'{encoded_url}\n  dir={save_path}\n\n')
    
    print(f'\nSucess!\nAria2 input file was saved to {ARIA2_INPUT_FILE}. Please run following command to start download:\n\naria2c --header="Cookie:FedAuth={COOKIE_FEDAUTH}" --input-file={ARIA2_INPUT_FILE} --max-concurrent-downloads=2 --max-connection-per-server=5 --save-session=session.txt --save-session-interval=30\n')

if __name__ == "__main__":
    main()