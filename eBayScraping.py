#!/usr/bin/env python
import time

import requests, json
import datetime
import re
import urllib.request, os
import csv

#eBay client id
appID = ''

idArray = []

#vendors' URL to make a request for all listings
vendorsURL ={1: "http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsAdvanced&SECURITY-APPNAME="+appID+"&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&itemFilter(0).name=Seller&itemFilter(0).value(0)=canucklarry&categoryId=47151&paginationInput.entriesPerPage=100&paginationInput.pageNumber=",
            2: "http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsAdvanced&SECURITY-APPNAME="+appID+"&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&itemFilter(0).name=Seller&itemFilter(0).value(0)=wwfdcs&categoryId=47151&keywords=canada%20FDCs&paginationInput.entriesPerPage=100&paginationInput.pageNumber=",
            3: "http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsAdvanced&SECURITY-APPNAME="+appID+"&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&itemFilter(0).name=Seller&itemFilter(0).value(0)=cdncoinz&categoryId=47151&paginationInput.entriesPerPage=100&paginationInput.pageNumber=",
            4: "http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsAdvanced&SECURITY-APPNAME="+appID+"&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&itemFilter(0).name=Seller&itemFilter(0).value(0)=inka2547&categoryId=47151&keywords=canada%20fdc&paginationInput.entriesPerPage=100&paginationInput.pageNumber=",
            5: "http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsAdvanced&SECURITY-APPNAME="+appID+"&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&itemFilter(0).name=Seller&itemFilter(0).value(0)=saskconnection&categoryId=47151&keywords=canada%20fdc&paginationInput.entriesPerPage=100&paginationInput.pageNumber="

}
#vendors' list
toChose = input('for get items from canucklarry press 1 \n'
                'for get items form wwfdcs press 2 \n'
                'for get items form cdncoinz press 3\n'
                'for get items form inka2547 press 4\n'
                'for get items form saskconnection press 5\n')

today = datetime.datetime.today()

vendors = {
    1:'canucklarry',
    2:'wwfdcs',
    3:'cdncoinz',
    4:'inka2547',
    5:'saskconnection'
}

#Item's class
class Item:
    def __init__(self):
        vendor = ''
        id = ''
        itemLink = ''
        picURL = ''
        price = ''
        title = ''
        scNum = ''
        year = ''
        localUrl = ''
        place = ''
        imName = ''

#First day cover places list
dictionary = ['ULpb', 'URpb', 'LRpb', 'LLpb', 'MRpb', 'MLpb', 'UL', 'UR', 'LR', 'LL', 'MR', 'ML', 'BK', 'TR', 'TL', 'BL', 'BR',
                 'ulpb', 'urpb', 'lrpb', 'llpb', 'mrpb', 'mlpb']

#First day cover places dictionary
recode = {
    'UL' : 'UL',
    'UR' : 'UR',
    'LR' : 'LR',
    'LL' : 'LL',
    'MR' : 'MR',
    'ML' : 'ML',
    'BK' : 'BK',
    'n/a' : 'n/a',
    'N/A' : 'N/A',
    'TR' : 'UR',
    'TL' : 'UL',
    'BR' : 'LR',
    'BL' : 'LL',
    'ul': 'UL',
    'ur': 'UR',
    'lr': 'LR',
    'll': 'LL',
    'mr': 'MR',
    'ml': 'ML'
}

def recoded(t, ob):
    t.replace('UL', 'UL')
    t.replace('UR', 'UR')
    t.replace('LR' , 'LR')
    t.replace('LL' ,  'LL')
    t.replace('MR', 'MR')
    t.replace('ML', 'ML')
    t.replace('BK', 'BK')
    t.replace('n/a', 'n/a')
    t.replace('N/A', 'N/A')
    t.replace('TR', 'UR')
    t.replace('TL', 'UL')
    t.replace('BR', 'LR')
    t.replace('BL', 'LL')
    ob.place = t

def canucklarry(res,ob):
    p = ob.title.replace('  ', ' ')
    p = p.lower()
    p = p.split()
    tit = ' '.join(map(str, p))
    tit = tit.replace('canada', '')
    tit = tit.replace('# ', '#')
    tit = tit.replace('new ', '')
    tit = tit.replace('used ', '')
    tit = tit.replace('cover ', '')
    tit = tit.replace('unaddressed', '')
    tit = tit.replace('& ', '')
    tit = tit.replace(' - ', '-')
    tit = tit.replace('ofdc ', '')
    tit = tit.replace('fdc ', '')

    iname = ''
    numb = '0000'
    place = 'n/a'
    year = '1970-01-01'

    n = tit.split()
    n.sort()

    try:
        place = next((item for item in n if item in dictionary))
        place = place.replace('pb', '')
        ob.place = recode[place]
    except:
        ob.place = 'N/A'

    try:
        ob.scNum = next((item for item in n if '#' in item))
    except:
        ob.scNum = '0000'

    for i in n:
        if i.__len__() != 4:
            n.remove(i)

    n.sort()

    for o in n:
        try:
            int(o)
            if int(o) in range(1970, today.year + 1):
                ob.year = o
            else:
                ob.year = '1970-01-01'
            break
        except:
            ob.year = '1970-01-01'
    iname = tit.replace(numb, '')
    iname = iname.replace(year, '')
    iname = iname.replace(place + 'pb', '')
    iname = iname.replace('  ', ' ')
    # iname.split()
    # iname = ''.join(map(str,iname))

    iname = iname.replace(' ', '-')
    ob.imName = iname.replace('--', '-')

def saskconnection(res,ob):
    rem = ob.title
    sp = ob.title.split()
    ob.scNum = sp[1]
    year = res['Item']['ItemSpecifics']['NameValueList']
    try:
        need = next((item for item in year if item["Name"] == "Year of Issue"))
        # year itself
        ob.year = need['Value'][0]
    except:
        ob.year = '1971-01-01'
    try:
        if sp[2] in dictionary:
            ob.place = sp[2]
        else:
            ob.place = 'N/A'
    except:
        ob.place = 'N/A'

    n = rem.lower()
    n.replace(ob.year, '')
    n.replace(ob.scNum, '')
    n.replace(ob.place.lower(), '')
    n.replace('first day cover', '')
    ob.imName = n

def wwfdcs(res, ob):
    i = ob.title.lower()
    rem = i.replace('sc # ', 'sc#')
    rem = rem.replace('scott # ', 'scott#')
    rem = rem.replace('sc ', 'sc#')
    rem = rem.replace('sc#', 'scott#')
    rem = rem.replace('scott# ','scott#')
    rem = rem.replace('canada ', '')
    rem = rem.replace('fdc', '')
    rem = rem.replace('- ', '-')
    rem = rem.replace(' -', '-')
    rem = rem.replace('/','')
    sp = rem.split()
    try:
        if int(sp[0]):
            year = sp[0]
        else:
            try:
                sc = []
                for i in sp:
                    sc.append(i.replace('^0-9\s#', ''))
                sc.sort()
                year = next((item for item in sc if
                             item.__len__() == 4 and '#' not in item and int(item) in range(1971, today.year)))
            except:
                year = '1971-01-01'
    except:
        try:
            sc = []
            for i in sp:
                sc.append(i.replace('^0-9\s#',''))
            sc.sort()
            year = next((item for item in sc if item.__len__() == 4 and '#' not in item and int(item) in range(1971, today.year)))
        except:
            year = '1971-01-01'
    try:
        number = next((item for item in sp if 'scott#' in item))
        let = sp.index(number, 0, sp.__len__() - 1)
        if '-' in sp[let + 1] and sp[let + 1].__len__() < 4:
            le = sp[let + 1]
            number = number.replace('scott#', '')
            number = number.upper() + le
        elif sp[let + 1].__len__() < 3 & 'in' not in sp[let + 1] and 'on' not in sp[let + 1]:
            le = sp[let + 1]
            number = number.replace('scott#', '')
            number = number.upper() + le
        else:

            number = number.replace('scott#', '').upper()

    except:
        if 'scott#' in sp[1]:

            number = sp[1]
            number = number.replace('scott#', '')

            if '-' in sp[2] and sp[2].__len__() < 4:
                le = sp[2]
                number = number.replace('scott#', '')
                number = number.upper() + le
            elif sp[2].__len__() < 3 and 'in' not in sp[2]:
                le = sp[2]
                number = number.replace('scott#', '')
                number = number.upper() + le
            else:
                number = number.replace('scott#', '').upper()
        else:
            number = '0000'
    try:
        place = next((item for item in sp if item.upper() in dictionary))
        place = place.upper()
    except:
        place = 'n/a'
    for item in dictionary:
        number = number.replace(item.lower(), '')

        ob.year = year
        ob.scNum = number
        ob.place = place

    n = rem.lower()
    n.replace(ob.year, '')
    n.replace(ob.scNum, '')
    n.replace(place.lower(), '')
    n.replace('first day cover', '')
    ob.imName = n

def cdncoinz(res, ob):
    i = ob.title.lower()
    rem = i.replace('# ', '#')
    rem = rem.replace(' - ', '-')
    rem = rem.replace('canada ','')
    sp = rem.split()
    try:

        year = next((item for item in sp if int(item) in range(1971, today.year+1)))
    except:
        year = '1971-01-01'
    try:
        number = next((item for item in sp if '#' in item))

    except:
        number = '0000'
    try:
        place = next((item for item in sp if item.upper() in dictionary))
        place = place.upper()
    except:
        place = 'n/a'

    n = rem.lower()
    n.replace(year, '')
    n.replace(number, '')
    n.replace(place.lower(), '')
    n.replace('first day cover', '')

    ob.imName = n
    ob.year = year
    ob.scNum = number
    ob.place = place

def inka2547(res, ob):
    i = ob.title.lower()
    rem = i.replace('sc # ', 'sc#')
    rem = rem.replace('# ', '#')
    rem = rem.replace('    ', ' ')
    rem = rem.replace('   ', ' ')
    rem = rem.replace('  ', ' ')
    rem = rem.replace('  ', ' ')
    rem = rem.replace('scott # ', 'scott#')
    rem = rem.replace('sc ', 'sc#')
    rem = rem.replace('sc#', 'scott#')
    rem = rem.replace('scott#', '#')
    rem = rem.replace('scott ', '#')
    rem = rem.replace('canada ', '')
    rem = rem.replace('fdc ', '')
    rem = rem.replace('- ', '-')
    rem = rem.replace(' -', '-')
    rem = rem.replace(' \"', '')
    rem = rem.replace('\"', '')
    rem = rem.replace('&', '')
    rem = rem.replace('  ', ' ')
    sp = rem.split(' ')
    try:
        spa = sp
        for itm in spa:
            if itm.__len__() != 4:
                spa.remove(itm)
        if spa.__len__() > 0:
            for im in spa:
                if im.__len__() == 4 and '#' not in im and int(im) in range(1971, today.year):
                    ob.year = im
                else:
                    ob.year = '1971-01-01'
        else:
            ob.year = '1971-01-01'

    except:
        for it in range(0, sp.__len__()):
            try:
                if sp[it].__len__() == 4 and '#' not in sp[it] and int(sp[it]) in range(1971, today.year):
                    ob.year = sp[it]
                else:
                    ob.year = '1971-01-01'
            except:
                ob.year = '1971-01-01'
    sp = rem.split(' ')
    try:
        number = next((item for item in sp if '#' in item))
        let = sp.index(number, 0, sp.__len__() - 1)
        if '-' in sp[let + 1] and sp[let + 1].__len__() < 4:
            le = sp[let + 1]
            number = number.replace('#', '').upper() + le
        elif sp[let + 1].__len__() < 3 & 'in' not in sp[let + 1] and 'on' not in sp[let + 1]:
            le = sp[let + 1]
            number = number.replace('#', '').upper() + le
        else:
            number = number.replace('#', '').upper()
        for item in dictionary:
            number = number.replace(item.lower(), '')
        ob.scNum = number

    except:
        try:
            number = next((item for item in sp if '#' in item))
            for item in dictionary:
                number = number.replace(item.lower(), '')
            ob.scNum = number.replace('#', '')
        except:
            for s in sp:
                if s.__len__() > 1 and '#' in s:
                    for item in dictionary:
                        s = s.replace(item.lower(), '')
                    ob.scNum = s.replace('#', '')
                else:
                    ob.scNum = '0000'

    try:
        place = next((item for item in sp if item.upper() in dictionary))
        place = place.upper()
        ob.place = place
    except:
        place = 'n/a'
        ob.place = place
    n = rem.lower()
    n.replace(ob.year, '')
    n.replace(ob.scNum, '')
    n.replace(place.lower(), '')
    n.replace('first day cover', '')
    ob.imName = n


def dLoading(array, ob):#must be a list if links to product's images and object name

    path = os.path.dirname(os.path.realpath(__file__))+'\images\\'+vendors[int(toChose)]+'\\'+str(today.date())+'\\'
    if not os.path.exists(path):
        os.makedirs(path)
    c = array.__len__()
    urls = []
    if c > 1:
        counter = 0
        for i in array:
            if 'N/A' in i:
                urls.append('N/A')
            else:
                url = i
                names = []
                name = ob.imName
                name = name.replace('"', '')
                name = name.replace('on ','')
                name = name.replace('fdc','')
                name = name.replace('\'s','')
                name = name.split()
                for s in name:
                    if s == ob.year:
                        name.remove(s)
                    elif s == ob.scNum:
                        name.remove(s)
                    else:
                        names.append(s)
                n = ' '.join(map(str, names))
                n = n.replace('canada ','')
                n = n.replace('new ', '')
                n = n.replace(' ', '-')
                n = n.replace(',', '')
                n = n.replace('>','')
                n = n.replace('<','')
                n = n.replace('|','')
                n = n.replace('/','')
                n = n.replace('\\','')
                n = n.replace(':','')
                n = n.replace('*','')
                n = n.replace('?','')
                n = n.replace('--','-')
                n = n.replace('--','-')

                urllib.request.urlretrieve(url,path+'CN0000'+'_'+'Sc'+ob.scNum.replace('/','')+'_'+n+'_'+str(counter)+'.jpg')
                urls.append(path+'CN0000'+'_'+'Sc'+ob.scNum.replace('/','')+'_'+n+'_'+str(counter)+'.jpg')
                counter += 1
        ob.localUrl = ';'.join(map(str, urls))

    else:
        for i in array:
            if 'N/A' in i:
                urls.append('N/A')
            else:
                url = i
                names = []
                name = ob.imName
                name = name.replace('"', '')
                name = name.replace('on ','')
                name = name.replace('fdc','')
                name = name.replace('\'s','')
                name = name.replace('first day cover','')
                name = name.split()
                for s in name:
                    if s == ob.year:
                        name.remove(s)
                    elif s == ob.scNum:
                        name.remove(s)
                    else:
                        names.append(s)
                n = ' '.join(map(str, names))
                n = n.replace('canada ', '')
                n = n.replace('new ', '')
                n = n.replace(' ', '-')
                n = n.replace(',', '')
                n = n.replace('>','')
                n = n.replace('<','')
                n = n.replace('|','')
                n = n.replace('/','')
                n = n.replace('\\','')
                n = n.replace('/','')
                n = n.replace(':','')
                n = n.replace('*','')
                n = n.replace('?','')
                n = n.replace('--','-')
                n = n.replace('--','-')

                urllib.request.urlretrieve(url,
                                           path + '_CN0000' + '_'+'Sc'+ob.scNum.replace('/','')+'_'+n+'.jpg')
                urls.append(
                    path + '_CN0000' + '_' + 'Sc' + ob.scNum.replace('/','') + '_' + n + '.jpg')
        ob.localUrl = ';'.join(map(str, urls))

def titleParce(res, ob):
    if int(toChose) == 1:
        canucklarry(res, ob)
    elif int(toChose) == 2:
        wwfdcs(res, ob)
    elif int(toChose) == 3:
        cdncoinz(res, ob)
    elif int(toChose) == 4:
        inka2547(res, ob)
    elif int(toChose) == 5:
        saskconnection(res, ob)



def ListOfProducts(link):#for getting item's ID
    reqLink = requests.get(link+'1')
    res = json.loads(reqLink.content.decode('utf-8'))
    pageNum = res['findItemsAdvancedResponse'][0]['paginationOutput'][0]['totalPages']
    for i in range(1,int(pageNum[0])+1):
        itemsList = requests.get(link + '&paginationInput.pageNumber=' + str(i))
        itemList = json.loads(itemsList.content.decode('utf-8'))
        for u in range(0,100):
            try:
                itemsID = itemList['findItemsAdvancedResponse'][0]['searchResult'][0]['item'][u]['itemId']
                idArray.append(itemsID[0])
            except:
                print("Keep moving if you need to parse items' details or restart if you need to parse another one!")
                break

def ProductDetails(file):#for getting Item's details.
    file.write('Vendor Name' + '^' + 'Item Number' + '^' + 'Title' + '^' + 'Price' + '^' + 'Year of Issue' + '^' + 'Scott\'s Number' + '^' + 'Block Location' + '^'
               + 'eBay Link' + '^' + 'Image Link' + '^' + 'Local Path' + '\n')
    count = 0
    for i in idArray:
        count +=1
        req = requests.get('http://open.api.ebay.com/shopping?callname=GetSingleItem&version=1063&appid='+appID+'&ItemID='+i+
                           '&responseencoding=JSON&IncludeSelector=ItemSpecifics')
        response = json.loads(req.content.decode('utf-8'))
        ob = Item()
        if response['Ack'] == 'Success':
            ob.vendor = vendors[int(toChose)]
            ob.id = i
            try:
                ob.itemLink = response['Item']['ViewItemURLForNaturalSearch']
            except:
                try:
                    ob.itemLink = response['Item'][0]['ViewItemURLForNaturalSearch']
                except:
                    ob.itemLink = 'N/A'
            try:
                picURL = response['Item']['PictureURL']
            except:
                picURL =['']
            uriAr = []
            for i in picURL:
                url = i
                url = url.replace('//', '/')
                url = url.split('/')
                try:
                    url = 'https://i.ebayimg.com/images/g/' + url[url.__len__()-2] + '/s-l1600.jpg'
                except:
                    url = 'N/A'
                    ob.localUrl = 'N/A'
                uriAr.append(url)
            ob.picURL = ';'.join(map(str,uriAr))
            ob.price = str(response['Item']['ConvertedCurrentPrice']['Value'])
            ob.title = response['Item']['Title']
            titleParce(response,ob)
            dLoading(uriAr,ob)
            print(ob.id + ' - ' + str(count) + ' items scraped from ' + ob.vendor)
            ob.place = ob.place.replace('bp','')
            ob.place = ob.place.replace('pb','')
            try:
                ob.place = recode[ob.place]
            except:
                ob.place = 'N/A'
            file.write(ob.vendor + '^' + ob.id + '^' + ob.title + '^' + ob.price + '^' + ob.year + '^' + ob.scNum + '^' + ob.place + '^' + ob.itemLink + '^' +  ob.picURL + '^' + ob.localUrl+'\n')
        else:
            print('You has reached the limit of requests. Please wait for 24 hours or stop the running program.')
            time.sleep(86401)



def run():

    template = open(str(today.date())+'_'+vendors[int(toChose)]+'.csv', 'w', encoding='utf-8')

    if int(toChose) in range(1, 6):

        ListOfProducts(vendorsURL[int(toChose)])

        way = input('Total items quantity: ' + str(idArray.__len__()) + '. Press Enter ro continue or CTRL+C to break down. '
                                                                        'Please note - you have only 5,000 requests per hour')

        ProductDetails(template)

    else:
        print('It\'s look like you missclicked and enter a wrong number. Please restart and try again!')


run()

