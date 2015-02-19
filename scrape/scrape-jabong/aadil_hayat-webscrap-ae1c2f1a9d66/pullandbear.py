import urllib
import mechanize
import urlparse
import json
from bs4 import BeautifulSoup
import xlsxwriter


workbook = xlsxwriter.Workbook('pullandbear.xlsx')
worksheet = workbook.add_worksheet()

headers = (
    ['Product Code', 0],
    ['Brand',   1],
    ['Category',  2],
    ['Name',    3],
    ['Price', 4],
    ['Discount',   5],
    ['Net Price',  6],
    ['Color',    7],
    ['Details',   8],
    ['Product URL',  9],
    ['Image URL',    10],
    ['Other Image URL' , 11],
    ['Thumbnail',12],
    ['Sizes',13],
    ['Exception',14]
)

kind={}
kind['1']="Exterior "
kind['2']="Lining "
kind['3']="Interior "


for head,col in (headers) :
    worksheet.write(0,col,head)

i=1

br = mechanize.Browser()

br.set_handle_robots(False)
br.addheaders = [('User-agent','Mozilla')]
cj = mechanize.CookieJar()
br.set_cookiejar(cj)


items = "http://www.pullandbear.com/itxrest/1/catalog/store/24009405/20109402/category/359505/product?languageId=-1"

htmltext = br.open(items).read()

soup = BeautifulSoup(htmltext.decode('utf8'))

#print soup.findAll('div',{'id':'grid_innerContainerRestyling'})
#print soup.prettify().encode('utf8')
data = json.loads(htmltext)
print len(data['products'])
for product in data['products']:
    print "================================"+str(product['id'])+"========================"

    worksheet.write(i,0,product['id'])

    main = "http://www.pullandbear.com/webapp/wcs/stores/servlet/ProductDetailJSON?catalogId=20109402&langId=-1&productId="+str(product['id'])+"&storeId=24009405"
    htmltext = br.open(main).read()

    soup = BeautifulSoup(htmltext.decode('utf8'))

    worksheet.write(i,1,"Pull And Bear")
    worksheet.write(i,2,"Coats")

    #print soup.findAll('div',{'id':'grid_innerContainerRestyling'})
    #print soup.prettify().encode('utf8')
    data = json.loads(htmltext)
    print data['name']
    worksheet.write(i,3,data['name'])
    print data['onSale']
    if(data['onSale']=='0'):
        worksheet.write(i,4,u'\u20ac'+" "+data['curPrice'])
        worksheet.write(i,5,u'\u20ac'+" 0.0")
        worksheet.write(i,6,u'\u20ac'+" "+data['curPrice'])

    if(data['onSale']=='1'):
        worksheet.write(i,4,u'\u20ac'+" "+data['oldPrice'])
        worksheet.write(i,5,u'\u20ac'+" "+str(float(data['curPrice'])-float(data['oldPrice'])))
        worksheet.write(i,6,u'\u20ac'+" "+data['curPrice'])
    
    
    
    print data['curPrice']
    print data['oldPrice']

    
    prev = data['composition'][0]['identifier'].split('[')[2].split(']')[0]
    comp=kind[prev]+" : "
    for c in data['composition']:
        cur= c['identifier'].split('[')[2].split(']')[0]
        if cur>prev :
            comp=comp+" ; "+kind[cur]+" : "

        comp=comp+str(c['percent'])+"%"+c['component']+" "
        #print str(c['percent'])+"% "+c['component']


    print comp
    worksheet.write(i,8,comp)

    
    l=0
    colors=""
    oimg=" "
    img=""
    thumb=""
    j=0
    for c in data['colors']:
        if(l>0):
            colors=colors+" , "
        
        #print c['nameColor']
        colors=colors+c['nameColor']
        sizes=""
        k=0
        for s in c['sizes']:
            if(k>0):
                sizes=sizes+" , "
            #print s['desc']
            sizes=sizes+s['desc']
            k=k+1

        for im in c['images']:
            if(j==0):
                img=im['zoom']
                thumb=im['thumb']
            else:
                oimg=oimg+" , "

            oimg=oimg+im['zoom']


            j=j+1

        l=l+1

    print colors
    worksheet.write(i,7,colors)
    print sizes
    worksheet.write(i,13,sizes)
    print img
    worksheet.write(i,10,img)
    print thumb
    worksheet.write(i,12,thumb)
    print oimg
    worksheet.write(i,11,oimg)

    print data['link']['full']
    worksheet.write(i,9,data['link']['full'])
    print main

    i=i+1



workbook.close()
