#!/bin/python
# -*- coding: utf-8 -*-
from Urlfinder import UrlFinder 
from EmailFinder import EmailFinder
from WebRequester import WebRequester
from urllib.parse import urlparse
import logging
import datetime
from termcolor import colored
import random
import time
from time import sleep
from os import system
import sys
logging.basicConfig(format='%(message)s', level=logging.INFO , filename='crawler.log')

# SETUP
#proxy_host = '127.0.0.1:8118'
proxy_host = None
timeout_request = 5
max_urls = 20000
initial_url = "https://www.wikipedia.org/"


def calculate_percent(discovered_urls, max_urls):
    result = round(((100 * len(discovered_urls))/ max_urls), 2)
    return result

def secs_to_readable(start_time):
    secs = round(time.time() - start_time)
    return str(datetime.timedelta(seconds=secs))

def reorder_log():
    print(colored("[+]Reordering crawler.log file....", "cyan"))
    system("sort -u crawler.log -o crawler.log")

def clean_urls_of_already_visited_domains(already_visited_domains, discoverd_urls):
    system("clear")
    reorder_log()
    print(colored("[+]Cleaning URLs......", "cyan"))
    sleep(2)
    discoverd_urls_copy = discoverd_urls
    for url in discoverd_urls_copy:
        for domain in already_visited_domains:
            if url.find(domain) != -1:
                try:
                    discoverd_urls.remove(url)
                    print(colored("[-]Removing URL => " + url, "blue"))
                except Exception:
                    pass
                
    return discoverd_urls

def check_is_file_extension(file_extensions, item):
    for extension in file_extensions:
        if item.find(extension) != -1:
            return True
    return False

def print_colored(start_time, discovered_urls, already_visited_domains, discovered_emails, max_urls):
        print(colored("========RESUME======================", "cyan"))
        print(colored("Uptime %s" % secs_to_readable(start_time), 'cyan'))
        percent = calculate_percent(discovered_urls, max_urls)
        print(colored("Stored URLs " + str(len(discovered_urls)) + " " + str(percent) + "% to MAX", "cyan"))
        print(colored("Domains found " + str(len(already_visited_domains)), "cyan"))
        if discovered_emails:
            print(colored("Emails found => " + str(len(discovered_emails)), "cyan"))
            average = "Avg x min %s" % str(round((len(discovered_emails) / (round(time.time() - start_time)/60 )), 2)) 
            print(colored(average, 'cyan'))
        print(colored("=====================================", "cyan"))

def visit_url(url, timeout_request, proxy_host):
    webrequester = WebRequester(url, timeout_request, proxy_host)
    raw_html = webrequester.request_url()
    return raw_html

def extract_domain(url):
    try:
        domain = urlparse(url).netloc
        if domain:
            withoutsubdomains = domain.split(".")[-2:]
            return str(withoutsubdomains[-2] + "." + withoutsubdomains[-1])
    except:
        return None

def extract_emails(discovered_emails, file_extensions):
    discovered_emails = EmailFinder(raw_html).search_emails()
    if discovered_emails is not None:
        for mail in discovered_emails:
            if mail not in saved_emails:
                if mail is not False:
                    if not check_is_file_extension(file_extensions, mail):
                        saved_emails.append(mail)
                        print(colored("[+]Found email: " + mail, "white"))
                        logging.info(mail)
                    
    return saved_emails  

def extract_urls(discovered_urls, max_urls, raw_html, already_visited_domains, file_extensions):
    new_urls = UrlFinder(raw_html).search_urls()
    actual_size_discovered_urls = len(discovered_urls)
    for url in new_urls:
        domain = extract_domain(url)
        if domain:
            if domain not in already_visited_domains:
                if not check_is_file_extension(file_extensions, url):
                    if actual_size_discovered_urls < max_urls:
                        if url not in discovered_urls:
                            discovered_urls.append(url)
                            actual_size_discovered_urls = len(discovered_urls)
                            print(colored("[+]Adding URL => " + url, "yellow"))
            
    if discovered_urls:                    
        if actual_size_discovered_urls >= max_urls:
            discoverd_urls_copy = discovered_urls
            print(colored("[+]Max number of URLs reach old are begin to be removed!!!!", "blue"))
            discovered_urls = clean_urls_of_already_visited_domains(already_visited_domains, discoverd_urls_copy)
            
    return(discovered_urls)

def initial_charge(discovered_urls, proxy_host):
    system("clear")
    #system("echo '' > crawler.log")
    print("=========================START==========================================")
    if proxy_host is not None:
        print(colored("[+]Using proxy => " + proxy_host, "yellow"))
    print(colored("[+]Max URLs " + str(max_urls), "yellow"))
    print(colored("[+]Visiting initial URL => " + initial_url + ".....", "yellow"))
    #first launch shoul find new url + domains who can looped over
    webrequester = WebRequester(initial_url, timeout_request, proxy_host)
    raw_html = webrequester.request_url()
    if raw_html is not None:
            discovered_urls = UrlFinder(raw_html).search_urls()
            print(colored("[+]In the initial URL search " + str(len(discovered_urls)) + " links where found!!", "yellow"))
            print("========================================================================")
    return discovered_urls

#Begin
#Big files can cause freeze the request so is better to avoid
file_extensions = [".ico", ".js", ".css", ".jpg", ".png", ".gif", ".jpeg", ".svg", ".mp3", ".mp4", ".avi", ".flv", ".webm", "webp",
    ".torrent", ".iso", ".dmg", ".dvd", ".img", ".raw", ".cue", ".pdf", ".zip", ".rar", ".exe", ".apk", ".bin"] 
discovered_urls = []
discovered_emails = []
saved_emails = []
already_visited_domains = []
raw_html = None
###First Load###
discovered_urls = initial_charge(discovered_urls, proxy_host)
sleep(4)    
start_time = time.time()
    
# main loop
while 1:
    #system("clear")
    try:
        if discovered_urls:    
            url = random.choice(discovered_urls)
            print("[+]Requests => " + url)
        try:
            domain = extract_domain(url)
            print("[+]Domain " + domain)
        except:
            pass
        
        if domain not in already_visited_domains:
            already_visited_domains.append(domain)
            if not check_is_file_extension(file_extensions, url):
                raw_html = visit_url(url, timeout_request, proxy_host)
            else:
                print(colored("[-]Skiping URL file => " + url, "red"))
            if raw_html:
                discovered_urls_copy = discovered_urls
                discovered_emails_copy = discovered_emails
                discovered_urls = extract_urls(discovered_urls_copy, max_urls, raw_html, already_visited_domains, file_extensions)
                discovered_emails = extract_emails(discovered_emails_copy, file_extensions)
        else:
            print(colored("[-]Duplicated domain => " + domain,  "red"))
            try:
                discovered_urls.remove(url)   
            except:
                pass
            print(colored("[-]Removing URL => " + url, "red"))

            
        print_colored(start_time, discovered_urls, already_visited_domains, discovered_emails, max_urls)
        #sleep(0.1)
        if len(discovered_urls) == 0:
            print(colored("Empty of URLs, need more luck next time or another initial URL.... :( END", "yellow"))
            sys.exit()

    except KeyboardInterrupt:
        print(colored("Want to finish? (y/n)", "red"))
        answer = input()
        if answer == "y":
            reorder_log()
            sys.exit()

