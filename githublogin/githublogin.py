from lxml import etree
import requests
from urllib.parse import urlencode
import re
class gitlogain():
    def __init__(self,page):
        self.heads={
            'Referer': 'https://github.com',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 YaBrowser/18.6.1.770 Yowser/2.5 Safari/537.36',
            'Host':'github.com'
           }
        self.logainurl='https://github.com/login'
        self.posturl='https://github.com/session'
        self.session=requests.Session()
        self.page=page
        self.xmlurl='https://github.com/dashboard-feed?'

    def token(self):
        ruler=re.compile(r'name="authenticity_token" value="(.*)"./')
        auth=self.session.get(self.logainurl,headers=self.heads)
        z=auth.text
        authenticity_token=ruler.findall(z)
        print(authenticity_token[0])
        return authenticity_token[0]

    def login(self,email,password):
        post_data={
        'commit': 'Sign in',
        'utf8':'✓',
        'authenticity_token':self.token(),
        'login': email,
        'password': password
        }
        ss=self.session.post(self.posturl,headers=self.heads,data=post_data)
        if ss.status_code==200:
            self.dd()

    def dd(self):
        para={
            'page': self.page,
            'utf8':'✓'
        }
        xml=self.xmlurl+ urlencode(para)
        res=self.session.get(xml,headers=self.heads)
        if res.status_code==200:
            sele=etree.HTML(res.text)
            dynamics=sele.xpath('//div[@class="d-flex flex-justify-between flex-items-baseline"]')
            print(dynamics)
            for i in dynamics:
                str=''.join(i.xpath('./div//text()')).replace('\n','')#一个div的所有[//]text()全部解析出来，然后构成一个类别，并把换行符替换
                str=re.sub(' +',' ',str)#多个空白字符，换成一个
                print(str)
 
if __name__=='__main__':
    t=gitlogain(page=1)

    t.login(email='erblue@163.com',password='123456789wu!')



