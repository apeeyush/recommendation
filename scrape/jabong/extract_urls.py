from lxml import html
import requests
import re
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring
import time

in_file = '22/22.xml'
out_file = '22/22urls'

tree = ET.parse(in_file)
root = tree.getroot()

for child in root:
    for child_element in child:
        if child_element.tag.find('loc') >=0:
            page_url = child_element.text
            with open(out_file,'a') as f: f.write(page_url+'\n')

