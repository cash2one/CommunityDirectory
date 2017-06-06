import time
import re
import uuid
import urllib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.proxy import *

myProxy = "69.147.248.240:8080"

proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'httpProxy': myProxy,
    'httpsProxy': myProxy,
    'sslProxy': myProxy,
    'noProxy': '' # set this value as desired
    })




caps = webdriver.DesiredCapabilities().FIREFOX
caps["marionette"] = False



profile = webdriver.FirefoxProfile()
profile.set_proxy(proxy)

browser = webdriver.Firefox(profile, capabilities=caps)


browser.get('http://www.google.com')

search = browser.find_element_by_name('q')
search.send_keys("site:https://play.google.com/store/apps/details?id= 'Tango Device'")
search.send_keys(Keys.RETURN) # hit return after you enter search text

# get max pages

WebDriverWait(browser, 10).until(EC.title_contains("Tango"))

max_pages = 15 

# extract from the current (1) page

#print "Starting Scrape..."
print "["


#print "Page 1"
tangoapps = browser.find_elements_by_class_name('r')
#print( str(len(tangoapps)) )
for someapp in tangoapps:
    applinks = someapp.find_elements_by_css_selector("a")
    for url in applinks:
	    urlstring = url.get_attribute('href').encode('utf-8')
	    browser.execute_script("window.open()") 
	    browser.switch_to_window(browser.window_handles[1])
	    browser.get(urlstring)
	    try: 
	    	WebDriverWait(browser, 10).until(EC.title_contains("Apps on Google Play"))
	    except TimeoutException:
 		browser.close()
		browser.switch_to_window(browser.window_handles[0])
		continue 
	    


	    print "{"
            print("\"name\": \""+browser.find_elements_by_class_name('id-app-title')[0].text.encode('utf-8')+"\",")
	    print("\"publisher\": \""+browser.find_elements_by_css_selector("[itemprop='name']")[1].text.encode('utf-8')+"\",") 
	    print("\"link\": \""+urlstring+"\",")
            
	    r = re.compile('play.google.com/store/apps/details\?id=(.*)')
            m = r.search(urlstring)
            if m:
                print("\"package_name\": \""+m.group(1)+"\",") 
	   
	    iconname = "icon-"+str(uuid.uuid4()) 
	    urllib.urlretrieve(browser.find_elements_by_class_name('cover-image')[0].get_attribute('src'), iconname ) 
	    print("\"icon\": \""+iconname+"\",") 
	    appdescription = (browser.find_elements_by_css_selector( "[itemprop='description']" )[0]).text.encode('utf-8')
 
	    print("\"description\": \""+appdescription.replace('"', "'")+"\",") 
	    bannername = "banner-"+str(uuid.uuid4())
	    urllib.urlretrieve(browser.find_elements_by_class_name('screenshot')[0].get_attribute('src'), bannername) 
	    print("\"banner\": \""+bannername+"\",")
            
	    print("\"genre\": \"Tango\",")
	    print("\"developerHW\": \"0\",")
	    print("\"consumerHW\": \"0\",")
	    print("\"google_promoted\": \"0\",")
	    print("\"optin_directory\": \"0\",")
	    print("\"optin_promotion\": \"0\"")
	    print("},") 
	    browser.close()
            browser.switch_to_window(browser.window_handles[0])
            time.sleep(5)

time.sleep(5)

# loop over the rest of the pages
for page in xrange(2, max_pages + 1):
    #print "Page %d" % page


    browser.find_element_by_id("pnnext").click()

    WebDriverWait(browser, 10).until(EC.title_contains("Tango"))

    time.sleep(5)

    tangoapps = browser.find_elements_by_class_name("r")
    
    for someapp in tangoapps:
       applinks = someapp.find_elements_by_css_selector("a")
       for url in applinks:
	    urlstring = url.get_attribute('href').encode('utf-8')
            browser.execute_script("window.open()")
            browser.switch_to_window(browser.window_handles[1])
            browser.get(urlstring)
            try:
                WebDriverWait(browser, 10).until(EC.title_contains("Apps on Google Play"))
            except TimeoutException:
                browser.close()
                browser.switch_to_window(browser.window_handles[0])
                continue



            print "{"
            print("\"name\": \""+browser.find_elements_by_class_name('id-app-title')[0].text.encode('utf-8')+"\",")
            print("\"publisher\": \""+browser.find_elements_by_css_selector("[itemprop='name']")[1].text.encode('utf-8')+"\",")
            print("\"link\": \""+urlstring+"\",")

            r = re.compile('play.google.com/store/apps/details\?id=(.*)')
            m = r.search(urlstring)
            if m:
                print("\"package_name\": \""+m.group(1)+"\",")

            iconname = "icon-"+str(uuid.uuid4())
            urllib.urlretrieve(browser.find_elements_by_class_name('cover-image')[0].get_attribute('src'), iconname )
            print("\"icon\": \""+iconname+"\",")
            appdescription = (browser.find_elements_by_css_selector( "[itemprop='description']" )[0]).text.encode('utf-8')

            print("\"description\": \""+appdescription.replace('"', "'")+"\",")
            bannername = "banner-"+str(uuid.uuid4())
            urllib.urlretrieve(browser.find_elements_by_class_name('screenshot')[0].get_attribute('src'), bannername)
            print("\"banner\": \""+bannername+"\",")

            print("\"genre\": \"Tango\",")
            print("\"developerHW\": \"0\",")
            print("\"consumerHW\": \"0\",")
            print("\"google_promoted\": \"0\",")
            print("\"optin_directory\": \"0\",")
            print("\"optin_promotion\": \"0\"")
            print("},")
            browser.close()
            browser.switch_to_window(browser.window_handles[0])
            time.sleep(5)
