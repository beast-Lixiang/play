import urllib.request
import gzip
import json
import pprint
import charset

class spider:


    def __init__(self, header=None,cinema=None):
        self.sum = 0
        self.header = header
        self.inputfilm = "魔兽"
        self.url = None
        self.page = None
        self.film_name = None
        self.hallName = None
        self.price = None
        self.showTime = None
        self.rebateprice = None
        self.mstring = None
        self.dicts = None
        self.dimesional = None
        self.inputlx = "IMAX-3D"
        self.cinema = cinema
        self.dateday = None

    def ungzip(self,data):
        try:
            data = gzip.decompress(data)
        except Exception as err:
            print(err)
        return data

    def setinputfilm(self,filename):
        self.inputfilm = filename

    def inputleixing(self, lx):
        self.inputlx = lx

    def modify(self,string,cinema,dateday):
        self.url = string
        self.cinema = cinema
        self.dateday = dateday

    def clear(sefl,string):
        if string == "url":
            self.url = None
        if string == "page":
            self.header = None
        if string == "header":
            self.header = None

    def findmovie(self):
        dicts = self.dicts
        try:
            if 'film_name' in dicts and dicts['film_name'] == self.inputfilm and 'dimensional' in dicts \
                    and dicts['dimensional'] == self.inputlx:
                self.film_name = self.inputfilm
                self.dimesional = self.inputlx
                if 'hallName' in dicts:
                    self.hallName = dicts['hallName']
                if 'rebateprice' in dicts:
                    self.rebateprice = dicts['rebateprice']
                if 'price' in dicts:
                    self.price = dicts['price']
                if 'showTime' in dicts:
                    self.showTime = dicts['showTime']
                self.printf()
        except Exception as err:
            print(err)

    def dealstring(self):
        self.dicts = json.loads(self.mstring)
        self.findmovie()

    def pagedeal(self):
        dpage = self.page
        si = None
        sj = None
        for i in range(0,len(dpage)):
            if dpage[i] == '{':
                si = i
            if dpage[i] == '}' and si is not None:
                sj = i
                if si - sj < len(dpage):
                    mstring = dpage[si:sj+1]
                    self.mstring = mstring

                    self.dealstring()
                    si = None
                    sj = None

    def request(self):
        req = urllib.request.Request(url=self.url, headers=self.header)
        data = urllib.request.urlopen(req)
        page = data.read()
        page = self.ungzip(page)
        self.page = page.decode('utf8')

    def printf(self):
        if self.cinema == 304:
            cinema = "魔兽"
        elif self.cinema == 311:
            cinema = "天通苑万达影院"
        elif self.cinema == 333:
            cinema = "石景山万达影院"
        elif self.cinema == 849:
            cinema = '通州万达影院'
        else:
            cinema = "未知影院"
        self.sum += 1
        print("发现第",self.sum,"条记录^_^")
        print("影院：",cinema,"片名:",self.film_name," 类型：",self.dimesional,"时间:","2016_06_"+self.dateday+" "+self.showTime," 厅号:",self.hallName," 价格:",self.price)

if __name__ == '__main__':
    header = {'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Host':'www.wandafilm.com',
    'Referer':'http://www.wandafilm.com/trade/movie_times.jsp',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
                 ' (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    spider = spider(header)
    cinema = [304, 311, 333, 849]
    date = ['03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21']
    a = input("请输入电影名！！")
    spider.setinputfilm(a)
    a = input("请输入类型！！")
    spider.inputleixing(a)
    print("开始查找.....")
    for c in cinema:
        for i in date:
            url = ("http://www.wandafilm.com/trade/time.do?m=init&city_code=undefined&cinema_id=%s&day=2016_06_%s&rond=0.4841693847287514&_=1464070889825"%(str(c),str(i)))
            print("start....")
            spider.modify(url,c,i)
            spider.request()
            spider.pagedeal()
    print("查找结束！！！")

# f = open("/home/zm/桌面/a.html","w+",encoding = 'utf8')
# f.write(page)