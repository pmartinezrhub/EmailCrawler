import urllib.request


class WebRequester():
    
    def __init__(self, url, timeout_request, proxy=None):
        self.url = url
        self.timeout_request = timeout_request
        if proxy is not None:
            self.proxy_host = proxy
        else:
            self.proxy_host = None
            
    def request_url(self):
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:48.0) Gecko/20100101 Firefox/48.0"
            req = urllib.request.Request(self.url, headers=headers)
            if self.proxy_host is not None:
                req.set_proxy(self.proxy_host, 'http')
            html = urllib.request.urlopen(req, timeout=self.timeout_request).read()
            return(str(html))
        except Exception as e:
            print(e)
            return None
    
