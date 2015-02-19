import urllib
import mechanize
import urlparse
import json
from bs4 import BeautifulSoup
import xlsxwriter
import re
import string

# out = open("marella.csv", "w")

# out.write("Code , Mini Description , Value Stock , Name , Brand , Price , Avalability , Front Image Url , Back Image Url , Product Url , Colors ,  Description \n")

workbook = xlsxwriter.Workbook('marella3.xlsx')
worksheet = workbook.add_worksheet()

headers = (
    ['Code', 0],
    ['Mini Description',   1],
    ['Value Stock',  2],
    ['Name',    3],
    ['Brand', 4],
    ['Price',   5],
    ['Availability',  6],
    ['Front Image Url',    7],
    ['Back Image Url', 8],
    ['Product Url',   9],
    ['Colors',  10],
    ['Description',    12],
    ['Category' , 11],
    ['Sizes',13],
    ['Details',14],
    ['Instructions',15]
)


for head,col in (headers) :
        worksheet.write(0,col,head)

# print headers[0][0]


br = mechanize.Browser()

br.set_handle_robots(False)
br.addheaders = [('User-agent','Mozilla')]
cj = mechanize.CookieJar()
br.set_cookiejar(cj)
i=1

param = { 'naz':'it' }
try :
    data = urllib.urlencode(param)
except :
    print "error encoding params"


htmltext = br.open("http://it.marella.com/it/shop-online/",data).read()

categ = ["coats-and-trench-coats","dresses","jackets","jeans","jumpsuits","knitwear-and-sweatshirts","padded-items","skirts","t-shirts-and-shirts","trousers","bags","belts","gloves","hats","scarves","shoes-and-sandals","small-accessories"]




main = "http://it.marella.com/en/shop/online-"





x=0

while x<len(categ) :

        start=1




        while True :
                parameters = {
                    'start':start
                    }
                try :
                    data = urllib.urlencode(parameters)
                except :
                    print "error encoding params"


                htmltext = br.open(main+categ[x],data).read()

                # print htmltext
                #jdata = json.loads(htmltext)

                try :
                    jdata = json.loads(htmltext)
                except :
                    print htmltext
                        
                
                

                if len(jdata)==0 :
                        break

                # print jdata[0]['name']
                j=0

                while j<len(jdata) :
                        
                        print "==================== "+str(i)+" ======================="
                        print jdata[j]["mini_desc"]
                        print jdata[j]["prezzo"].replace('&#128;&nbsp;',' ')
                        worksheet.write(i,0,jdata[j]["codice"])
                        worksheet.write(i,1,jdata[j]["mini_desc"])
                        worksheet.write(i,2,jdata[j]["valore_giacenza"])
                        worksheet.write(i,3,jdata[j]["name"])
                        worksheet.write(i,4,jdata[j]["label_brand"])
                        worksheet.write(i,5,u'\u20ac'+jdata[j]["prezzo"].replace('&#128;&nbsp;',' '))
                        worksheet.write(i,6,jdata[j]["disponibile"])
                        worksheet.write(i,7,"http:"+jdata[j]["fronte_src"])
                        worksheet.write(i,8,"http:"+jdata[j]["retro_src"])
                        worksheet.write(i,9,"http://eu.marella.com"+jdata[j]["href_dettaglio"])

                        a=0
                        colors=""

                        while a<len(jdata[j]["lista_colori"]) :
                                if a>0 :
                                        colors=colors+" , "

                                colors=colors + jdata[j]["lista_colori"][a]["descrizione"]
        

                                a=a+1


                        print colors
                        worksheet.write(i,10,colors)
                        htmltext = br.open("http://it.marella.com"+jdata[j]["href_layer"],data).read()

                        idata = json.loads(htmltext)
                        #print idata
                        #print "http://eu.marella.com"+jdata[j]["href_layer"]


                        worksheet.write(i,12,idata["message"]["descrizione_breve"])
                        worksheet.write(i,11,categ[x])

                        
                        try :
                                
                                htmltext = br.open("http://it.marella.com"+jdata[j]["href_dettaglio"],data).read()
                        
                                soup = BeautifulSoup(htmltext)
                                #print soup.prettify()
                                sizes = soup.findAll('div',{"class" : "quadrato-taglia"})

                                #print str(sizes[0]).replace('">','"><p>').replace('</','</p></')

                                #soup2 = BeautifulSoup(str(sizes[0]).replace('">','"><p>').replace('</','</p></'))
                                #print soup2.findAll('p')

                                a=0
                                s=""
                                
                                while a<len(sizes) :
                                        if a>0 :
                                                s=s+" , "

                                        soup2 = BeautifulSoup(str(sizes[a]).replace('">','"><p>').replace('</','</p></'))
                                        s2= str(soup2.findAll('p')[0]).replace('<p>','').replace('</p>','').lstrip().rstrip()
                                        #print s2
                                        s=s+s2

                                        a=a+1

                                print s

                                worksheet.write(i,13,s)

                                details = soup.findAll('li',{"class" : "li-comp-lav"})

                                if len(details)>1 :
                                        detail= str(details[0]).replace('<li class="li-comp-lav">','').replace('</li>','').lstrip().rstrip()
                                        print detail
                                        worksheet.write(i,14,detail.decode("utf8"))
                                
                                
                                if len(details)>1 :
                                        instruc= str(details[1]).replace('<li class="li-comp-lav">','').replace('</li>','').lstrip().rstrip()
                                        print instruc
                                        worksheet.write(i,15,instruc.decode("utf8"))


                        except :
                              print "Cant get more details about this product"  
                        

                        i=i+1
                        j=j+1



                start=start+10



        x=x+1













# out.close()
workbook.close()
