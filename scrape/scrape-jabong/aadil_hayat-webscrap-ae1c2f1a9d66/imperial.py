import urllib
import mechanize
import urlparse
import json
from bs4 import BeautifulSoup
import xlsxwriter


workbook = xlsxwriter.Workbook('imperial.xlsx')
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
    ['Description', 8],
    ['Details',   9],
    ['Product URL',  10],
    ['Image URL',    11],
    ['Other Image URL' , 12],
    ['Quantities Available' , 13],
    ['Gender',14]

)


for head,col in (headers) :
    worksheet.write(0,col,head)



br = mechanize.Browser()

br.set_handle_robots(False)
br.addheaders = [('User-agent','Mozilla')]
cj = mechanize.CookieJar()
br.set_cookiejar(cj)


main = "http://www.imperialfashion.com/en/shoponline-woman/9999"

i=1

categ={}

categ['W']={}
categ['M']={}

categ['W']['V']="Blousons"
categ['W']['K']="Coats"
categ['W']['A']="Dresses"
categ['W']['L']="Gilet"
categ['W']['J']="Jackets"
categ['W']['l']="Leather Jackets"
categ['W']['Y']="Overalls and Salopettes"
categ['W']['P']="Pants"
categ['W']['C']="Shirts"
categ['W']['R']="Singlets"
categ['W']['G']="Skirts"
categ['W']['M']="Sweaters and T-shirts"
categ['W']['1']="Leather Jackets"






# parameters = {
# 		    'start':'1'
# 		    }
# try :
#     data = urllib.urlencode(parameters)
# except :
#     print "error encoding params"


htmltext = br.open(main).read()

soup = BeautifulSoup(htmltext.decode('utf8'))

soup2= BeautifulSoup(str(soup.findAll('center')[2]))

#print soup2.prettify()


#print soup2.findAll('a')[0]['href']
items = soup2.findAll('a')
j=0

while j<len(items):
    
    #print items[j]['href']

    htmltext2 = br.open(str(items[j]['href'])).read()
    #print htmltext2

    soup3= BeautifulSoup(htmltext2.decode('utf8'))

    x = soup3.findAll('input',{"id" : "hdn_Articolo"})[0]['value']

    #print x.encode('utf8')

    idata = json.loads(x.encode('utf8'))

    print "======================================="+str(j)+"=========================="
    print idata['CodArt']

    worksheet.write(i,0,idata['CodArt'])

    print idata['Descrizione']

    worksheet.write(i,3,idata['Descrizione'])
    worksheet.write(i,1,"Imperial")
    worksheet.write(i,14,"Woman")
    worksheet.write(i,2,categ['W'][idata['CodSottoGruppo']])
    worksheet.write(i,4,u'\u20ac'+" "+str(idata['Prezzo']))
    worksheet.write(i,5,str(idata['Sconto'])+" %")
    worksheet.write(i,6,u'\u20ac'+" "+str(idata['PrezzoUFinale']))

    print categ['W'][idata['CodSottoGruppo']]
    print u'\u20ac'+" "+str(idata['PrezzoUFinale'])
    
    worksheet.write(i,9,idata['Composizione'])
    worksheet.write(i,10,"http://www.imperialfashion.com"+items[j]['href'].replace('codlin=1','codlin=0'))
    print "http://www.imperialfashion.com"+items[j]['href'].replace('codlin=1','codlin=0')
    worksheet.write(i,11,"http://b2b.imperialfashion.com/images/imgarticoli/"+idata['ImmagineFrontale'])
    print "http://b2b.imperialfashion.com/images/imgarticoli/"+idata['ImmagineFrontale']

    oimg = " "
    k=0
    while k<len(idata['Immagini']) :
        if(k>0):
            oimg=oimg+" , "

        oimg=oimg + "http://b2b.imperialfashion.com/images/imgarticoli/"+idata['Immagini'][k]['Immagine']

        k=k+1


    print oimg

    worksheet.write(i,12,oimg)

    descr=""
    k=0

    while k<len(idata['Caratteristiche']):
        if(k>0):
            descr=descr+" , "

        descr=descr+idata['Caratteristiche'][k]

        k=k+1

    print descr
    
    worksheet.write(i,8,descr)

    colors=[]
    c=""
    q=""
    k=0

    while k<len(idata['QuantitaVendibili']):
        if(k>0):
            q=q+" , "

        if idata['QuantitaVendibili'][k]['Colore'] not in colors :
            if len(colors)>0 :
                c=c+" , "
            colors.append(idata['QuantitaVendibili'][k]['Colore'])
            c=c+idata['QuantitaVendibili'][k]['Colore'].rstrip()

        q=q+idata['QuantitaVendibili'][k]['Taglia']+" "+idata['QuantitaVendibili'][k]['Colore'].rstrip()+" "+str(idata['QuantitaVendibili'][k]['Quantita'])
        

        k=k+1

    print c
    print q

    worksheet.write(i,7,c)
    worksheet.write(i,13,q)

    


    #print htmltext


    #yourstring = yourstring.encode('ascii', 'ignore').decode('ascii')

    i=i+1
    j=j+1


workbook.close()
