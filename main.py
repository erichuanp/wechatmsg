import datetime
import requests
import urllib.parse
import wxauto
# 海珠

url1 = 'https://tianqi.moji.com/weather/china/guangdong/haizhu-district'
# 南山
url2 = 'https://tianqi.moji.com/weather/china/guangdong/nanshan-district'
# 圣地亚戈
url3 = 'https://tianqi.moji.com/weather/united%20states/california/sandiego'


def GetWeather(url):
    print('正在访问' + url)
    response = requests.get(url)
    print('访问结束...')
    response.encoding = 'utf-8'
    response = response.text

    loc = response[response.find('>【') + 2:response.find('】')]

    start = response.find('今天</a>')
    end = response.find('  </strong>', start)
    response = response[start:end]

    tq1 = response.find('alt=\"') + 5
    tq2 = response.find('>', tq1)
    tq = response[tq1:tq2].replace('"', '')
    response = response[tq2:]

    tem1 = response.find('<li>') + 4
    tem2 = response.find('</li>', tem1)
    tem = response[tem1:tem2]
    response = response[tem2:]

    wind1 = response.find('<em>') + 4
    wind2 = response.find('</em>', wind1)
    wind = response[wind1:wind2]
    response = response[wind2:]

    ws1 = response.find('<b>') + 3
    ws2 = response.find('</b>', ws1)
    ws = response[ws1:ws2]

    return '''今日''' + loc + tq + '''
气温：''' + tem + '''    风速：''' + wind + ws


def GetToday():
    global sentToday
    sentToday = True
    return '''早上好JOJO！今天是''' + str(datetime.date.today()) + '''！
您的替身 Stone Free 为您报告
''' + GetWeather(url1) + '''
''' + GetWeather(url2) + '''
''' + GetWeather(url3) + '''
'''


def GetWord(msg):

    rtn = ''
    i = 1
    urlw = 'https://dict.youdao.com/suggest?doctype=json&q=' + urllib.parse.quote(msg)
    trans = requests.get(urlw).json()
    if trans['result']['code'] == 200:
        trans = trans['data']['entries']
        for entry in trans:
            rtn += '(' + str(i) + ') ' + entry['entry'] + '''
''' + entry['explain'] + ''''
'''
            i+=1
        urlw = 'https://www.youdao.com/result?word=' + urllib.parse.quote(msg) + '&lang=en'
        wxauto.WxUtils.SetClipboard(urlw)
        wx.SendClipboard()
        return rtn.replace("'", "")

    urlw = 'https://www.youdao.com/result?word=' + urllib.parse.quote(msg) + '&lang=en'
    wxauto.WxUtils.SetClipboard(urlw)
    wx.SendClipboard()
    response = requests.get(urlw)
    response.encoding = 'uft-8'
    response = response.text


    if response.find('class="pos"') >= 0:
        start = response.find('class="pos"')
        while start >= 0:
            response = response[start+5:]
            rtn += '(' + str(i) + ') ' + response[response.find('>') + 1:response.find('</')] + ' '
            response = response[response.find('class="trans"'):]
            rtn += response[response.find('>') + 1:response.find('</')] + '''
        '''
            start = response.find('class="pos"')
            i += 1
    elif response.find('class="point"') >= 0:
        start = response.find('class="point"')
        response = response[:response.find('"catalogue_paraphrasing"')]
        while start >= 0 and response.find('class="maybe_word"') < 0:
            response = response[start+5:]
            rtn += '(' + str(i) + ') ' + response[response.find('>') + 1:response.find('</')] + ' '
            start = response.find('class="point"')
            i += 1

    if response.find('class="trans-content"') >= 0:
        response = response[response.find('class="trans-content"'):]
        rtn += '翻译内容：' + response[response.find('>') + 1:response.find('</')] + ' '

    if rtn == '':
        wxauto.WxUtils.SetClipboard("您输入的是：" + msg)
        wx.SendClipboard()
        return '翻译失败！请发送有效词！'
    return rtn.replace('&lt;', '<').replace('&gt;', '>')

def callPC(msg):
    wx.ChatWith('加把劲SAKANA骑士')
    wxauto.WxUtils.SetClipboard(msg)
    for i in range(10):
        wx.SendClipboard()
    wx.ChatWith(OBJ)



def GenReply(msg):
    if msg == 'jt':
        rtn = GetToday()
    elif msg == 'pc':
        callPC('快点回复雨洁！！！')
        rtn = '我已经帮您叫了他十次。'
    elif msg == '索爱口令':
        callPC('说！你爱不爱周雨洁！')
        rtn = '作为您的替身，我负责任地告诉你，哪怕他再怎么说讨厌你，他都是爱你的。'
    else:
        rtn = GetWord(msg)
    return rtn

# 读取微信会话
wx = wxauto.WeChat()
wx.GetSessionList()
# 定位到目标
OBJ = 'JOJO'
wx.ChatWith(OBJ)
sentToday = False
thisDay = 0
while True:
    now = datetime.datetime.now()
    latest = wx.GetLastMessage
    if not sentToday and now.hour == 8:
        wxauto.WxUtils.SetClipboard(GenReply('jt'))
        wx.SendClipboard()
        thisDay = now.day
    elif thisDay < now.day:
        sentToday = False

    if latest[0] == OBJ:
        wxauto.WxUtils.SetClipboard(GenReply(latest[1]))
        wx.SendClipboard()
