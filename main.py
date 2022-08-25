import datetime
import requests
import urllib.parse
import wxauto
from zhdate import ZhDate

# 对象
OBJ = 'PCPC'
# 海珠
url1 = 'https://tianqi.moji.com/weather/china/guangdong/haizhu-district'
# 南山
url2 = 'https://tianqi.moji.com/weather/china/guangdong/nanshan-district'
# 圣地亚戈
url3 = 'https://tianqi.moji.com/weather/united%20states/california/sandiego'


def GetWeather(url):
    response = requests.get(url)
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
气温：''' + tem + '''
风速：''' + wind + ws


def GetToday():
    global sentToday
    sentToday = True
    today = datetime.datetime.today()
    zhtoday = ZhDate.from_datetime(today)
    dstart = datetime.datetime(2017,9,26)
    itv = today - dstart
    return '''早上好JOJO！💪今天是
🥰爱你的第''' + str(itv.days) + '''天
🌞''' + today.strftime('%Y %B %d') + ' ' + today.strftime('%A') + '''
🌜''' + zhtoday.chinese()[5:] + '''

替身 Stone Free 为您报告⛅
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
    wx.ChatWith('PCPC')
    wxauto.WxUtils.SetClipboard(msg)
    for i in range(10):
        wx.SendClipboard()
    wx.ChatWith(OBJ)



def GenReply(msg):
    if msg == '/今天':
        rtn = GetToday()
    elif msg == '/彭川':
        callPC('快点回复雨洁！！！')
        rtn = '我已经帮您叫了他十次。'
    elif msg == '/索爱':
        callPC('说！你爱不爱周雨洁！')
        rtn = '作为您的替身，我负责任地告诉你：哪怕他闹脾气，再怎么说讨厌你，他都是爱你的。'
    elif msg == '/帮助':
        rtn = '''使用指南：
替身只会在空闲期间持续读取JOJO发的最新一条消息，因此请在替身完成上一个任务之后，再下达新的指令。除了翻译功能会回复两条消息（链接+翻译）之外，其他的功能都会在任务完成后回复一条消息。在等待翻译功能的第二条消息期间，可以点开链接来查看详情。

我可以做到的事情：(1) 从聊天列表里选取一个人/一个群 (2) 读取聊天记录、发送消息/文件/微信截图 (3) 访问公共互联网获取信息(用以保存/计算/发送)

现可公开指令：
/今天  发送每日消息 也会在每日早上8点自动发出
/彭川  呼叫彭川以尽快回复JOJO
/索爱  呼叫彭川以尽快表白JOJO
/帮助  调出使用指南
/关闭  关闭替身

更多功能请向彭川提出...
只要是可以从网上扒拉下来的信息都可以做哦
'''
    elif msg == '/关闭':
        raise TypeError("人为关闭")
    else:
        rtn = GetWord(msg)
    return rtn

# 读取微信会话
wx = wxauto.WeChat()
wx.GetSessionList()
# 定位到目标
wx.ChatWith(OBJ)
sentToday = False
thisDay = 0
wx.SendMsg('您的替身初始化完毕，如需帮助请发送 /帮助')
try:
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
except Exception as e:
    wxauto.WxUtils.SetClipboard('''出现错误：
''' + str(e) + '''
您的替身已下线，请联系彭川修复或启动！''')
    wx.SendClipboard()


