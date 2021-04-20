# SharePoint Download List Generator

This project can generate Aria2 batch download list for SharePoint Links with folder structure.

## Instructions

[Aria2](https://github.com/aria2/aria2) is recommended, download from [Aria2/releases](https://github.com/aria2/aria2/releases).

How to get the Real Path:

1. Open the SharePoint link in web browser.
2. Open DevTools -> Network tab and then reload the page.
3. Filter out 'RenderListDataAsStream' XHR request(s).
4. Copy the Real Path from '@a1' or '@listUrl' query parameter (without quotes).  
   (eg. /personal/aaaa_t_cccc_cn/Documents/)
5. Concat the host and the path.   
   (eg. https://xxxx-my.sharepoint.com/personal/aaaa_t_cccc_cn/Documents/)

How to get FedAuth cookie:

1. Open the SharePoint link in web browser.
2. Open DevTools -> Network tab and then reload the page.
3. Locate the very first request after reloading or requests to your SharePoint domain.
4. Find either 'Cookie: FedAuth=' or 'Set-Cookie: FedAuth='.
5. Copy the text after 'Auth=' till the first semicolon(;).

Enjoy!

## Useage

Python3 is required to run the script.

```
# Following command might be pip3 or python3 depends on system.
pip install -r requirements.txt
python sharepoint_gen_aria2_download_list.py
# Follow the instuctions.
```
