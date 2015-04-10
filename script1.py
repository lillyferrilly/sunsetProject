import urllib2
from HTMLParser import HTMLParser
import re

class myHTMLParser(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.found = False
        self.match = False
        self.lastTag = ""
        self.data = ""
    
    def handle_starttag(self, tag, attrs):
        self.found = False
        if tag == 'span':
            for name, value in attrs:
                if name == 'id' and value == 'cc-sun-set':
                    self.found = True
                    self.lastTag = tag
        
    def handle_endtag(self, tag):
        while tag == 'span' and self.found == True:
            self.match = True
            self.found = False
        
    def handle_data(self, data):
        if self.lastTag == 'span' and self.match == False and self.found == True:
            self.data = data

response = urllib2.urlopen('http://www.wunderground.com/cgi-bin/findweather/getForecast?query=Burlington%2C+VT')
html = response.read()
            
parser = myHTMLParser()
parser.feed(html)
data = parser.data
data = 'Sunset: ' + data + 'PM'

HTMLfile = open('sunsetWebpageTemplate.php', 'r')
html1 = HTMLfile.read()
#print "original code: ", html1
html2 = re.sub(r'@tag',data,html1)
#print "new code: ", html1 

def deleteContent(pfile):
    pfile.seek(0)
    pfile.truncate()

file = open('actualSunsetWebpage.php', 'w')
deleteContent(file)
file.write(html2)
file.close()


