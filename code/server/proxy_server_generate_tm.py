# -*- coding: utf-8 -*-

"""
Install twisted (pip install twisted) and run the script.
Небольшой прокси сервер ловящий html контент страницы и модифицирующий его
добаляя после каждого слова состоящего из шести симвалов - ™
Проверенно на Firefox
В настройках Firefox необходимо задать:
HTTP Proxy -> localhost
Port -> 8080
После запустить скрипт и открыть страницу
-> http://habrahabr.ru/company/yandex/blog/258673/
Работает только с http
P.S. Можно попробывать погулять и по другим сайтам ;)
"""
from twisted.internet import reactor
from twisted.web import proxy, http
from HTMLParser import HTMLParser

import re

LST_SUB = []
LST_SUB_MODIFY = []


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.start_tag = ''
        self.str_start_tag = ''
        self.is_flag = True

    def handle_starttag(self, tag, attrs):
        self.start_tag = tag

    def handle_data(self, data):
        tmp_data = data
        if self.start_tag not in ['script', 'link']:
            if not self.is_flag:
                if self.str_start_tag == self.get_starttag_text():
                    self.str_start_tag = ''
                else:
                    self.is_flag = True
            if self.is_flag:
                self.str_start_tag = self.get_starttag_text()
                self.is_flag = False
            str_starttag_text = '%s%s' % (self.str_start_tag, tmp_data)
            LST_SUB.append(str_starttag_text)
            regex = re.compile(u'(\\b[a-zA-Zа-яА-Я]{6}\\b)', re.U)
            tmp_data = regex.sub(r'\1&trade;', tmp_data)
            str_modify_text = '%s%s' % (self.str_start_tag, tmp_data)
            LST_SUB_MODIFY.append(str_modify_text)
        HTMLParser.handle_data(self, tmp_data)


class LoggingProxyClient(proxy.ProxyClient):
    def __init__(self, command, rest, version, headers, data, father):
        del headers["accept-encoding"]
        proxy.ProxyClient.__init__(
            self, command, rest, version, headers, data, father
        )
        self.is_html = False
        self.buffer = ""

    def handleHeader(self, key, value):
        if key.lower() == "content-type" and value.startswith("text/html"):
            self.is_html = True
        proxy.ProxyClient.handleHeader(self, key, value)

    def handleResponsePart(self, buffer):
        self.buffer += buffer

    def handleResponseEnd(self):
        global LST_SUB
        global LST_SUB_MODIFY

        if not self._finished:
            if self.is_html:
                print "HTML -> PHTML"
                try:
                    tmp_buffer = self.buffer.decode('utf-8')
                    parser = MyHTMLParser()
                    parser.feed(tmp_buffer)
                    parser.close()
                    for index, item in enumerate(LST_SUB):
                        if item in tmp_buffer:
                            tmp_buffer = tmp_buffer.replace(
                                item, LST_SUB_MODIFY[index]
                            )

                    LST_SUB = []
                    LST_SUB_MODIFY = []

                    self.buffer = tmp_buffer.encode('utf-8')
                except UnicodeDecodeError:
                    pass

            self.father.responseHeaders.setRawHeaders(
                "Content-Length", [str(len(self.buffer))]
            )
            self.father.write(self.buffer)
            proxy.ProxyClient.handleResponseEnd(self)


class LoggingProxyClientFactory(proxy.ProxyClientFactory):
    protocol = LoggingProxyClient


class LoggingProxyRequest(proxy.ProxyRequest):
    protocols = {"http": LoggingProxyClientFactory}

    def process(self):
        is_http = self.uri.startswith("http://")
        is_https = self.uri.startswith("https://")
        if not is_http and not is_https:
            self.uri = "http://" + self.getHeader("Host") + self.uri
        print "Request from %s for %s" % (self.getClientIP(), self.uri)
        try:
            proxy.ProxyRequest.process(self)
        except KeyError:
            print "HTTPS is not supported at the moment!"


class LoggingProxy(proxy.Proxy):
    requestFactory = LoggingProxyRequest


class LoggingProxyFactory(http.HTTPFactory):
    def buildProtocol(self, addr):
        return LoggingProxy()


if __name__ == '__main__':
    reactor.listenTCP(8080, LoggingProxyFactory())
    reactor.run()
