import urllib
import mechanize
import urlparse
import json
from bs4 import BeautifulSoup
import xlsxwriter


workbook = xlsxwriter.Workbook('subdued.xlsx')
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


for head,col in (headers) :
    worksheet.write(0,col,head)

i=1

br = mechanize.Browser()

br.set_handle_robots(False)
br.addheaders = [('User-agent','Mozilla')]
cj = mechanize.CookieJar()
br.set_cookiejar(cj)

main = "http://www.subdued.it/en/1-COLLECTION"
htmltext = br.open(main).read()

soup = BeautifulSoup(htmltext.decode('utf8'))

categ = soup.findAll('ul',{'style':'list-style: none; line-height: 1.6;'})[0].findAll('li')

for c in categ :
#c=categ[0]
#if c!='' :
    #print c.text +" -> "+c.a['href'].replace('http://www.subdued.it/en/','').replace('?tp=&x=','')

    print "xxxxxxxxxxxxxxxxxxxxxxxxxxx "+c.text+" xxxxxxxxxxxxxxxxxxxxxxxxxx"

    p=1
    length=48
    while length==48:
        main = "http://www.subdued.it/en/"+c.a['href'].replace('http://www.subdued.it/en/','').replace('?tp=&x=','')+"?p="+str(p)+"&ajaxscroll=1"
        htmltext = br.open(main).read()
        print main
        soup = BeautifulSoup(htmltext.decode('utf8'))

        #print c.text.lstrip()
        j=0

        
        
        
        print len(soup.findAll('a'))
        length = len(soup.findAll('a'))
        it = soup.findAll('a')
        while j<length:
            worksheet.write(i,2,c.text.lstrip())
            print it[j+1]['title']
            worksheet.write(i,3,it[j+1]['title'])
            #print soup.findAll('label',{'style':''})[0].text

            htmltext = br.open(it[j]['href']).read()

            worksheet.write(i,9,it[j]['href'])

            soup = BeautifulSoup(htmltext.decode('utf8'))

            sizes=''
            k=0
            while k<len(soup.findAll('div',{'class':'divAttr'})):
                if(k>0):
                    sizes=sizes+" , "

                sizes=sizes+soup.findAll('div',{'class':'divAttr'})[k]['title']

                k=k+1

            print sizes
            worksheet.write(i,13,sizes)
            worksheet.write(i,1,"Subdued ")
                
            print soup.findAll('img',{'id':'bigpic'})[0]['src']
            worksheet.write(i,10,soup.findAll('img',{'id':'bigpic'})[0]['src'])
            worksheet.write(i,12,soup.findAll('img',{'id':'bigpic'})[0]['src'].replace('list','small'))

            k=0
            oimg=" "
            
            for img in soup.findAll('ul',{'id':'thumbs_list_frame'})[0].findAll('img'):
                #print img['src'].replace('medium','list')

                if k>0 :
                    oimg=oimg+" , "

                oimg=oimg+img['src'].replace('medium','list')

                k=k+1

            print oimg

            worksheet.write(i,11,oimg)   

            desc= soup.findAll('div',{'id':'short_description_content'})[0].findAll('p')
            print str(desc)
            
            try :
                    
                if(len(desc)==1):
                    d= str(desc[0]).replace('<p>','').replace('</p>','').split('<br/>')
                    print d[0]
                    print d[1]

                    worksheet.write(i,0,d[0].encode('utf8'))
                    worksheet.write(i,8,d[1])

                if(len(desc)>1):
                    print str(desc[0].text).replace('<p>','').replace('</p>','')
                    print str(desc[1].text).replace('<p>','').replace('</p>','').decode('utf8')

                    worksheet.write(i,0,str(desc[0].text).replace('<p>','').replace('</p>',''))
                    worksheet.write(i,8,str(desc[1].text).replace('<p>','').replace('</p>','').decode('utf8'))
            except :
                print "excepting"
                worksheet.write(i,14,str(desc).decode('utf8'))
            
            k=0
            colors=""
            try :
                for td in soup.findAll('div',{'id':'color_picker'})[0].findAll('td'):
                    #print td['title']
                    
                    if k>0 :
                        colors=colors+" , "

                    colors=colors+td['title']

                    k=k+1

                print colors

                worksheet.write(i,7,colors)
            except :
                print "No color found"
                    

            
            pr= soup.findAll('div',{'id':'short_description_block'})[0].label.text
            print pr
            worksheet.write(i,4,pr)
            worksheet.write(i,5,"0.0 ")
            worksheet.write(i,6,pr)
            #    print "Please update the discount manually  "

            print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


            j=j+2
            i=i+1

        p=p+1
        
        if(main =='http://www.subdued.it/en/13-SWEATSHIRTS?p=1&ajaxscroll=1') :
            length=47
        



workbook.close()








