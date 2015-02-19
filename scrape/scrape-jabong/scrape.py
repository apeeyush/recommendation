from lxml import html
import requests
import re
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
import time

out_file = '10/10.data'

def parsePage(page_url):
    page = requests.get(page_url)
    if page.text.find('THE PRODUCT YOU ARE LOOKING FOR HAS BEEN DISCONTINUED FROM JABONG') >=0:
        print 'Product Discontinued'
    else:
        print 'Storing product info..'
        tree = html.fromstring(page.text)
        brand = tree.xpath('//*[@id="qa-prd-brand"]/text()')
        with open(out_file,'a') as f: f.write(page_url + ';')
        with open(out_file,'a') as f: f.write(brand[0].strip() + ';')
        

        scripts = tree.xpath('/html/body/script')
        for script in scripts:
            script_text = script.text
            if (script_text.find('recommendation') >=0 ):
                reg = r'"(.*recommendation.*)&minPrice'
                matchObj = re.search(reg, script_text)
                recommendation_url = matchObj.group(1)
                page = requests.get(recommendation_url)
                recommendation_tree = html.fromstring(page.text)
                items = recommendation_tree.xpath('//div[2]/ul/li')
                if items:
                    for item in items:
                        item_url = item.xpath('a[1]')[0].attrib['href']
                        with open(out_file,'a') as f: f.write(item_url + ';')
                else:
                    for i in range(12):
                        with open(out_file,'a') as f: f.write(';')

        rows = tree.xpath('//*[@id="productInfo"]/table/tr')
        for row in rows:
            a,b = row.getchildren()
            if (a.text and b.text):
                with open(out_file,'a') as f: f.write(a.text.strip() + ':' + b.text.strip() + ';')

        with open(out_file,'a') as f: f.write('\n')
        time.sleep(5)

def main():
    tree = ET.parse('10/10.xml')
    root = tree.getroot()

    for child in root:
        for child_element in child:
            if child_element.tag.find('loc') >=0:
                page_url = child_element.text            
                parsePage(page_url)

if __name__ == '__main__':
    main()
