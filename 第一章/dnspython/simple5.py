#!/usr/bin/python

import dns.resolver
import os
import httplib

iplist=[]    #定义域名IP列表变量
appdomain="www.google.com.hk"    #定义业务域名

def get_iplist(domain=""):    #域名解析函数，解析成功IP将追加到iplist
    try:
        A = dns.resolver.query(domain, 'A')    #解析A记录类型
    except Exception,e:
        print "dns resolver error:"+str(e)
        return
    for i in A.response.answer:
        for j in i.items:
            iplist.append(j.address)    #追加到iplist
    return True

def checkip(ip):
    checkurl=ip+":80"
    getcontent=""
    httplib.socket.setdefaulttimeout(5)    #定义http连接超时时间(5秒)
    conn=httplib.HTTPConnection(checkurl)    #创建http连接对象

    try:
        conn.request("GET", "/", headers = {"Host" : domain})
        r = conn.getresponse()
        
        if r.status == 200: #服务器返回status 200，表示成功
            print ip + " [OK]"
        else:
            print ip + " [ERROR]" #此处可放告警程序，可以是邮件、短信通知
        except Exception, e:
            print "Cannot get response: " + str(e)  

if __name__=="__main__":
    if get_iplist(appdomain) and len(iplist)>0:    #条件：域名解析正确且至少要返回一个IP
        for ip in iplist:
            checkip(ip)
    else:
        print "dns resolver error."
