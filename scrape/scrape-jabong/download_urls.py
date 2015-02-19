import urllib
link = 'http://www.jabong.com/sitemapgen/sitemapxml/product/id/'
for i in range (1,12):
	urllib.urlretrieve(link+str(i),filename=str(i)+".xml")

# XPath : /urlset/url[1]/loc