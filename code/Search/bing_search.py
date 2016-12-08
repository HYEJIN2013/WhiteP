# -*- coding: utf-8 -*-
# Author: @proclnas
# Created:     01/12/2015
# Licence:     <MIT>

import requests
import os
import argparse
from sys import exit
from bs4 import BeautifulSoup
from threading import Thread, Event
from Queue import Queue


class BingJw:

    def __init__(self, dork_file, output, threads):
        self.dork_file = dork_file
        self.output = output
        self.ptr_limit = 401

        self.q = Queue()
        self.t_stop = Event()
        self.threads = threads
        self.list_size = len(open(dork_file).readlines())
        self.counter = 0

    def save_buf(self, content):
        with open(self.output, 'a+') as fp:
            fp.write('{}\n'.format(content.encode("UTF-8")))

    def crawler(self, q):
        while not self.t_stop.is_set():
            self.t_stop.wait(1)

            try:
                word = q.get()

                ptr = 1
                while ptr <= self.ptr_limit:
                    print '[{}/{}] Searching with {}\n'.format(ptr, self.ptr_limit, word)
                    content = requests.get('http://www.bing.com/search?q={}&count=50&first={}'.format(word, str(ptr)))

                    if content.ok:
                        soup = BeautifulSoup(content.text)

                        for link in soup.find_all('a'):
                            try:
                                link = link.get('href')

                                if 'http' in link and not re.search('msn|microsoft|php-brasil|facebook|4shared|bing| \
                                                                     imasters|phpbrasil|php.net|yahoo|scrwordtbrasil| \
                                                                     under-linux|google|msdn', link):
                                    self.save_buf(link)
                            except Exception:
                                pass

                    ptr += 10
            except Exception:
                pass
            finally:
                self.counter += 1
                q.task_done()

    def start(self):
        for _ in xrange(self.threads):
            t = Thread(target=self.crawler, args=(self.q,))
            t.setDaemon(True)
            t.start()

        for word in open(self.dork_file):
            self.q.put(word.strip())

        try:
            while not self.t_stop.is_set():
                self.t_stop.wait(1)
                if self.counter == self.list_size:
                    self.t_stop.set()

        except KeyboardInterrupt:
            print '~ Sending signal to kill threads...'
            self.t_stop.set()
            exit(0)

        self.q.join()
        print 'Finished!'

if __name__ == "__main__":
    banner = '''
      _     _              _____                    _
     | |   (_)            / ____|                  | |
     | |__  _ _ __   __ _| |     _ __ __ ___      _| | ___ _ __
     | '_ \| | '_ \ / _` | |    | '__/ _` \ \ /\ / / |/ _ \ '__|
     | |_) | | | | | (_| | |____| | | (_| |\ V  V /| |  __/ |
     |_.__/|_|_| |_|\__, |\_____|_|  \__,_| \_/\_/ |_|\___|_|
                     __/ |By @proclnas
                    |___/
    '''

    parser = argparse.ArgumentParser(description='Bing Crawler')

    parser.add_argument('-f', '--file', action='store', dest='dork_file', help='List with dorks to scan (One per line)',
                        required=True)
    parser.add_argument('-o', '--output', action='store', dest='output', help='Output to save valid results',
                        default='output.txt')
    parser.add_argument('-t', '--threads', action='store', default=1, dest='threads', help='Concurrent workers',
                        type=int)
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    args = parser.parse_args()

    if args.dork_file:
        if not os.path.isfile(args.dork_file):
            exit('File {} not found'.format(args.dork_file))

        print banner
        bing_jw = BingJw(args.dork_file, args.output, args.threads)
        bing_jw.start()
