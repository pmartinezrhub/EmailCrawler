License GPLv3 -- Do whatever you want with it. This script collects emails from public the Internet randomly, so is fair and legal to use it.

What diferences this kind of scrapping from others i did in past is than this one?, It doesn't request more than once per domain and it seems to work faster than to scrap entire domains looking for mails.

Features:

    Perpetual crawler
    Email validation
    Simplicity :)

Configuration:

Just adjust next variables:

proxy_host = None #not recomended to use tor proxy but i can work in some escenarios timeout_request = 5 The timeout of the requests. max_urls = 20000 Maximum url to store on memory. Once this limit its reached, the script make a clean of the queue initial_url = "https://www.wikipedia.org/" This is the initial URL where the scrapping begins.
