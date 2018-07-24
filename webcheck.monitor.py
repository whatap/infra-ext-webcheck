#!/usr/bin/python

import os, sys, time, glob
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import urllib2

def printHistory(name, key, value, buf):
    buf.write('H ')
    buf.write(name)
    buf.write(' ')
    buf.write(key)
    buf.write(' ')
    buf.write(str(value))
    buf.write('\n')

def printMeta(name, key, value, buf):
    buf.write('M ')
    buf.write(name)
    buf.write(' ')
    buf.write(key)
    buf.write(' ')
    buf.write(str(value).strip())
    buf.write('\n')

def printWebcheck(buf, response_dic):
    printHistory(response_dic['url'], "webcheck.ping.response_time", response_dic['response_time'], buf)
    printHistory(response_dic['url'], "webcheck.ping.status_code", response_dic['status_code'], buf)
    printHistory(response_dic['url'], "webcheck.ping.online", response_dic['online'], buf)

def listdir(prefix=os.path.split(os.path.realpath(__file__))[0]):
    buf = StringIO()
    for filepath in glob.glob('%s/*.conf'%(prefix)):
        f = open(filepath,'r')
        if f:
            for line in f.read().splitlines():
                line = line.strip()
                if not line:
                    continue
                url = validationUrl(line)

                try:
                    result = check(url)
                    printWebcheck(buf, result)
                except Exception, e:
                    dic = {
                        'url': url,
                        'response_time': -1,
                        'status_code': -1,
                        'online': 0
                    }
                    printWebcheck(buf, dic)
                    #import traceback
                    #print url, traceback.format_exc(sys.exc_info())
                    #print("listdir error, line: %s"%line)
                sys.stdout.write(buf.getvalue())

def request(url):
    result = {}
    start = time.time()

    if url.lower().startswith('https://'):
        opener = urllib2.build_opener(urllib2.HTTPSHandler())
    else:
        opener = urllib2.build_opener(urllib2.HTTPHandler())

    request = urllib2.Request(url, headers={'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'})
    request.get_method = lambda: 'GET'
    try:
        r = opener.open(request, timeout=10)
    except urllib2.HTTPError, e:
        print e
    result['url'] = url
    result['response_time'] = int((time.time() - start) * 1000.0)
    result['status_code'] = r.getcode()
    return result

def isDown(r):
    if r['status_code'] < 400 and r['response_time'] <= 2000:
        r['online'] = 1
        return False
    else:
        r['online'] = 0
        return True

def check(url):
    result = request(url)
    if isDown(result):
        response_times = []
        for i in range(0, 3):
            retry = request(url)
            if not isDown(retry):
                result = retry
                response_times.append(retry['response_time'])
        if len(response_times) > 0:
            result['response_time'] = int(sum(response_times) / len(response_times))
    return result

def validationUrl(url):
    validUrl = url
    isHttp = url.startswith("http://")
    isHttps = url.startswith("https://")
    if (not isHttp) and (not isHttps):
        validUrl = "http://" + url
    return validUrl
    
if __name__ == '__main__':
    listdir()