from lxml import html
import requests
import re
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
import time

in_file = '13/13.xml'
out_file = '13/13data'

def parsePage(page_url):
    page = requests.get(page_url)
    if page.text.find('THE PRODUCT YOU ARE LOOKING FOR HAS BEEN DISCONTINUED FROM JABONG') >=0:
        print 'Product Discontinued'
    else:
        print 'Storing product info..'
        tree = html.fromstring(page.text)
        brand = tree.xpath('//*[@id="qa-prd-brand"]/text()')
        with open(out_file,'a') as f: f.write(page_url + ';')
        if brand:
            with open(out_file,'a') as f: f.write(brand[0].strip().encode('ascii', 'ignore') + ';')
        # Product Description
        product_description = tree.xpath('//*[@id="productInfo"]/p/text()')
        if product_description:
            with open(out_file,'a') as f: f.write('product_description' + ':' + product_description[0].strip().encode('ascii', 'ignore') + ';')
        # Product key-value pairs
        rows = tree.xpath('//*[@id="productInfo"]/table/tr')
        for row in rows:
            a,b = row.getchildren()
            if (a.text and b.text):
                with open(out_file,'a') as f: f.write(a.text.strip().encode('ascii', 'ignore') + ':' + b.text.strip().encode('ascii', 'ignore') + ';')
        # Product images URL
        images_list = tree.xpath('//*[@id="prdbig"]/ul/li')
        for image in images_list:
            print image
            if image.find('img').get('src'):
                with open(out_file,'a') as f: f.write('image' + ':' + image.find('img').get('src') + ';')
        # newline
        with open(out_file,'a') as f: f.write('\n')

def main():
    tree = ET.parse(in_file)
    root = tree.getroot()

    for child in root:
        for child_element in child:
            if child_element.tag.find('loc') >=0:
                page_url = child_element.text
                parsePage(page_url)

if __name__ == '__main__':
    main()
