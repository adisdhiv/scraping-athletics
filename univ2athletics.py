#import libraries
from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time

# Function to replace text in nested sublists
def nestrepl(lst, what, repl):
    for index, item in enumerate(lst):
        if type(item) == list:
            nestrepl(item, what, repl)
        else:
            if item == what:
                lst[index] = repl


# Read the csv input file containing list of universities websites
df = pd.read_csv(r'Book1.csv')
df

# Setting up the driver. Install the necessary drivers for selenium. I have used gecko driver for firefox
driver = webdriver.Firefox() 

#Finding the url
elements = ['Athletics', 'ATHLETICS', 'Sports', 'SPORTS'] #add other categories also if you have
athleticsurl = []
for i in range(len(df)):
    url = []
    website = df['University website'][i]
    driver.get(website)
    for j in elements:
        try:
            link = driver.find_element_by_link_text(j)
            link.click()
            driver.switch_to_window(driver.window_handles[-1])
            time.sleep(5)
            url.append(driver.current_url)
            break
        except NoSuchElementException:
            url.append('None')
    athleticsurl.append(url)

print(athleticsurl)

#Cleaning and printing the result

#Removing none
nestrepl(athleticsurl, 'None', '')

#Combining it to a single list
sportslist = []
for i in range(len(athleticsurl)):
    t = ""
    for j in range(len(athleticsurl[i])):
        t += athleticsurl[i][j]
    sportslist.append(t)

#Printing the list
sportslist

#Convertint to dataframe
data = pd.DataFrame(sportslist, columns =['Sports website']) 

#Concatenating 2 dataframe
df_col = pd.concat([df,data], axis=1)
df_col

#Converting to csv
df_col.to_csv('output.csv')