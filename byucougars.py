#import necessary packages
import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd


#creating the soup object
page = requests.get('https://byucougars.com/components/nav/nav.html')
soup = BeautifulSoup(page.text,"html.parser")
results = soup.find(id = "myNavmenu")

#finding men's sports and links
menresults = results.select('li[class = "col-md-5 col-sm-5 mens-sports"]')
mentitle = menresults[0].select('li[class*="sports-menu-sport"] > a')
msid = []
for i in range(len(mentitle)):
    att = mentitle[i].attrs
    values = att['ui-sref']
    sportsid = re.search("'(.*?)'", values)
    msid.append(sportsid.group(1))
mensportslist = [i.text for i in mentitle]
print(mensportslist)
print(msid)

#finding women's sports and links
womenresults = results.select('li[class*="womens-sport"]')
womentitle = womenresults[0].select('li[class*="sports-menu-sport"] > a')
wsid = []
for i in range(len(womentitle)):
    att = womentitle[i].attrs
    values = att['ui-sref']
    sportsid = re.search("'(.*?)'", values)
    wsid.append(sportsid.group(1))
womensportslist = [i.text for i in womentitle]
print(womensportslist)
print(wsid)

#finding contents in womens sports
name = []
urls = []
title = []
phone = []
email = []
sport = []
category = []

for i in range(len(wsid)):
    
    # finding out the tid of the staff
    wsport = womensportslist[i]
    wcategory = "Women" 
    url = requests.get('https://byucougars.com/dl/feeds/menu-'+wsid[i])
    js = url.json()
    results = [];
    searchField = "name";
    searchVal = "Staff";
    for i in range(len(js)):
        if(js[i][searchField] == searchVal):
            results.append(js[i])
    tid = results[0]['tid']
    
    # using the tid to locate the staff details
    results1 = [];
    searchField1 = "parent_tid";
    searchVal1 = tid;
    for i in range(len(js)):
        if(js[i][searchField1] == searchVal1):
            results1.append(js[i])
            
    # finding the contents and storing
    for i in range(len(results1)):
        name.append(results1[i]['name'])
        sport.append(wsport)
        category.append(wcategory)
        urlw = results1[i]['field_nav_url']
        if urlw.startswith('http'):
            urls.append(urlw)
        else:
            urls.append('https://byucougars.com'+urlw)
        s = urlw.split("/")
        profileurl = requests.get('https://byucougars.com/dl/feeds/staff-bio-all/'+s[-2])
        p = profileurl.json()
        title.append(p[0]['field_job_title'])
        phone.append(p[0]['field_office_phone'])
        email.append(p[0]['field_email_address'])
    
    #logging the progress
    print(wsport + " is complete")

data = pd.DataFrame({'name' : name,'urls' : urls, 'title' : title, 'phone' : phone,'email' : email,'sport' : sport, 'category' : category})
data

#finding contents in mens sports
name1 = []
urls1 = []
title1 = []
phone1 = []
email1 = []
sport1 = []
category1 = []

for i in range(len(msid)):
    # finding out the tid of the staff
    msport = mensportslist[i]
    mcategory = "Men" 
    url1 = requests.get('https://byucougars.com/dl/feeds/menu-'+msid[i])
    js1 = url1.json()
    results1 = [];
    searchField2 = "name";
    searchVal2 = "Staff";
    for i in range(len(js1)):
        if(js1[i][searchField2] == searchVal2):
            results1.append(js1[i])
    tid1 = results1[0]['tid']
    
    # using the tid to locate the staff details
    results2 = [];
    searchField3 = "parent_tid";
    searchVal3 = tid1;
    for i in range(len(js1)):
        if(js1[i][searchField3] == searchVal3):
            results2.append(js1[i])
            
    # finding the contents and storing
    for i in range(len(results2)):
        sport1.append(msport)
        category1.append(mcategory)
        name1.append(results2[i]['name'])
        url1 = results2[i]['field_nav_url']
        if url1.startswith('http'):
            urls1.append(url1)
        else:
            urls1.append('https://byucougars.com'+url1)
        s1 = url1.split("/")
        profileurl1 = requests.get('https://byucougars.com/dl/feeds/staff-bio-all/'+s1[-2])
        p1 = profileurl1.json()
        try:
            title1.append(p1[0]['field_job_title'])
            phone1.append(p1[0]['field_office_phone'])
            email1.append(p1[0]['field_email_address'])
        except IndexError:
            title1.append("")
            phone1.append("")
            email1.append("")
                
    #logging the progress
    print(msport + " is complete")

# storing the result in a dataframe
data1 = pd.DataFrame({'name' : name1 ,'urls' : urls1, 'title' : title1, 'phone' : phone1,'email' : email1,'sport' : sport1, 'category' : category1})
data1

#merging both results
alldata = data.append(data1)
alldata

#storing in csv
alldata.to_csv('byusports.csv')
