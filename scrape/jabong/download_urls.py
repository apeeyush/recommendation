import urllib
import os

link = 'http://www.jabong.com/sitemapgen/sitemapxml/product/id/'
for i in range (20,21):
    directory = str(i)
    if not os.path.exists(directory):
        os.makedirs(directory)
    urllib.urlretrieve(link+str(i),filename=directory+'/'+str(i)+".xml")

# XPath : /urlset/url[1]/loc
