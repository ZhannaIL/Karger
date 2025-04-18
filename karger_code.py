
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time
import os 
from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import json

def for_gender(author):
    for_gen = author.split(' ')
    name = for_gen[0]
    my_url = 'https://api.genderize.io?name='+name
    
    with requests.get(my_url) as response:
        response_json = response.json()
        return response_json['gender']
    
def gender_probability(author):
    for_gen = author.split(' ')
    name = for_gen[0]
    my_url = 'https://api.genderize.io?name='+name
    
    with requests.get(my_url) as response:
        response_json = response.json()
        return response_json['probability']

# authorization on the site OpenAthens
driver = webdriver.Firefox() 
driver.maximize_window()
driver.get('https://my.openathens.net/?passiveLogin=false')
button = driver.find_element('xpath', '/html/body/app-root/ng-component/div/footer/div[1]/nav/ul[1]/li[1]/div/div/button[1]')
button.click()
time.sleep(4)
input_nam = driver.find_element('id', 'type-ahead')
input_nam= input_nam.send_keys("Bar Ilan")
time.sleep(4)
button = driver.find_element('class name', 'wayfinder-nav-link')
button.click()
time.sleep(4)
button = driver.find_element('class name', 'ORRU02D-k-b')
button.click()
time.sleep(100).  #input login and password

input_search = driver.find_element('id', 'search')
input_search = input_search.send_keys('Karger')
time.sleep(3)
karger = driver.find_element('xpath', '/html/body/app-root/ng-component/div/main/ng-component/app-page-body/div/app-research-view-desktop/div/div[1]/app-card-column/app-resources-card/lib-card/div/app-resources-view/div/ul/li/app-resource-content/a')
karger.click()

#going to the Karger website and setting filters to search for research articles
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers_info={'User-Agent':user_agent}
driver.get("https://karger-com.eu1.proxy.openathens.net/pps")
accept = driver.find_element('xpath', '/html/body/div[1]/div[1]/div[2]/span[1]/a')
accept.click()
time.sleep(2)
content = driver.find_element('xpath', '/html/body/section[1]/div[2]/div[2]/div/div[2]/nav/ul/li[1]/a')
content.click()
time.sleep(2)
articles = driver.find_element('xpath', '/html/body/section[1]/div[2]/div[2]/div/div[2]/nav/ul/li[1]/ul/li[1]/a')
articles.click()
time.sleep(2)
checkbox = driver.find_element('id', 'article-type--Research_Articles-chk-0-0')
checkbox.click()

output = {'Paper title': [], 'paper DOI': [], 'Publication Date': [], 'Number of authors': [], 'Name of the first author': [], 'Name of the last author': [], 'Gender of the first author': [], 'Gender of the last author': [], 'First author gender probability': [], 'Last author gender probability': [], 'Affiliation of the first author': [], 'Affiliation of the last author': [], 'Number of Figures': [], 'Figure 1 caption': [], 'Figure 2 caption': [], 'Figure 3 caption': [], 'Figure 4 caption': [], 'Figure 5 caption': [], 'Figure 6 caption': [], 'Figure 7 caption': [], 'Figure 8 caption': [], 'Figure 9 caption': [], 'Figure 10 caption': [], 'Figure 1 Link': [], 'Figure 2 Link': [], 'Figure 3 Link': [], 'Figure 4 Link': [], 'Figure 5 Link': [], 'Figure 6 Link': [], 'Figure 7 Link': [], 'Figure 8 Link': [], 'Figure 9 Link': [], 'Figure 10 Link': [], 'Number of Tables': [], 'Table 1 caption': [], 'Table 2 caption': [], 'Table 3 caption': [], 'Table 4 caption': [], 'Table 5 caption': [], 'Table 6 caption': [], 'Table 7 caption': [], 'Table 8 caption': [], 'Table 9 caption': [], 'Table 10 caption': []} 

n = 2            #variable for Next button
for page in range(104): 
    elements = driver.find_elements('class name', 'sri-title') 
    for i in range(len(elements)):  # loop of articles
        counter_start = 0
        flag_start = True
        year_limit = True

        while flag_start and counter_start < 3:
            try:
                limit = driver.find_elements('class name', 'al-citation-list')
        
                if int(limit[i].text[22:26]) > 1997:       #check the year in the description of the article 
                    new_elements = driver.find_elements('class name', 'sri-title')
                    lnk = new_elements[i].find_elements('tag name', 'a') 
                    lnk[0].click()
                    time.sleep(4)
                    flag_start = False
                else:
                    year_limit = False
                    break
            except:
                driver.refresh()
                flag_start += 1
                year_limit = False
                print('error in first try')

        if year_limit == False: #if the year is less than 1998, go to the next article
            continue
            
        for key in output:         #create dictionary key values 'not available'
            output[key] = output.get(key, []) + ['Not Available']   
            
        try:
            time.sleep(4)
            title = driver.find_element('class name', 'wi-article-title')
            output['Paper title'][-1] = title.text

            DOI = driver.find_element('class name', 'citation-doi')
            output['paper DOI'][-1] = DOI.text

            date =driver.find_element('class name', 'article-date')
            year =date.text[-4:]
            output['Publication Date'][-1]= date.text

            time.sleep(4)
            try:   #authors search
                name = driver.find_element('class name', 'al-authors-list')
            except:
                try:
                    time.sleep(6)
                    name = driver.find_element('class name', 'al-authors-list')
                except:
                    name = False 

            if name:
                all_names = [i.strip(';') for i in name.text.split('\n') if i!=';']
                num_authors = len(all_names)
                first_author = all_names[0]
                last_author = all_names[-1]

                gen_first = for_gender(first_author)
                if not gen_first:
                    prob_first = 0.5
                else:
                    prob_first = gender_probability(first_author)   
                time.sleep(3)

                gen_last = for_gender(last_author)
                if not gen_last:
                    prob_last = 0.5
                else:
                    prob_last = gender_probability(last_author)     
                time.sleep(3)

                output['Number of authors'][-1] = num_authors
                output['Name of the first author'][-1] = first_author
                output['Name of the last author'][-1] = last_author
                output['Gender of the first author'][-1] = gen_first
                output['Gender of the last author'][-1] = gen_last
                output['First author gender probability'][-1] = prob_first
                output['Last author gender probability'][-1] = prob_last

                time.sleep(4)                # first affiliation 
                nam_aff = driver.find_elements('class name', 'al-author-name')
                first = nam_aff[0]
                but_af = first.find_element('class name', 'linked-name')
                but_af.click()

                try: 
                    time.sleep(4)
                    first_affil = first.find_element('class name', 'info-card-affilitation')
                except:
                    time.sleep(5)
                    wait = WebDriverWait(first, 10)
                    first_affil = wait.until(EC.presence_of_element_located(('class name', 'info-card-affilitation')))

                output['Affiliation of the first author'][-1] = first_affil.text
                but_af.click() #

                time.sleep(4)                 # last affiliation
                aff = driver.find_elements('class name', 'al-author-name')
                last = aff[-1]
                time.sleep(2)
                but = last.find_element('class name', 'linked-name')
                but.click()

                try:
                    time.sleep(5)
                    last_affil = last.find_element('class name', 'info-card-affilitation')
                except:
                    try:
                        but_af.click()
                        time.sleep(5)
                        but_af.click()
                        time.sleep(5)
                        wait = WebDriverWait(last, 10)
                        last_affil = wait.until(EC.presence_of_element_located(('class name', 'info-card-affilitation')))
                    except:
                        print('\oops\n')

                output['Affiliation of the last author'][-1] = last_affil.text

            time.sleep(5)
            try:           #Figures and caption 
                fig_capt = driver.find_elements('class name', 'fig-caption')
            except:
                time.sleep(5)
                fig_capt = driver.find_elements('class name', 'fig-caption')



            caption_f  = []
            count_f = 0
            for l1 in fig_capt:
                if l1.text not in caption_f and l1.text:
                    caption_f.append(l1.text)
                    count_f += 1

            output['Number of Figures'][-1] = count_f

            for cap in range(len(caption_f)):
                output['Figure '+str(cap+1)+' caption'][-1] = caption_f[cap]

            time.sleep(4)
	
	#Save pictures
            fig_l = driver.find_elements('class name', 'download-slide')
            link_list =[]
            counter = 0
            for l2 in fig_l:
                ln = l2.get_attribute('href')
                time.sleep(5)
                if ln not in link_list and ln:
                    response = requests.get(ln, headers=headers_info)
                    curr_path = f"//Users//janny//Desktop//pictures//{year}"
                    curr_path2 = f'//Users//janny//Desktop//pictures//{year}//{title.text}'

                    if not os.path.exists(curr_path):
                        os.mkdir(f"//Users//janny//Desktop//pictures//{year}")
                    if not os.path.exists(curr_path2):
                        os.mkdir(f'//Users//janny//Desktop//pictures//{year}//{title.text}')
                    with open(f"//Users//janny//Desktop//pictures//{year}//{title.text}//Fig{counter+1}.ppt", "wb") as f:
                            f.write(response.content)

                    link_list.append(ln)
                    counter+=1

            for link in range(len(link_list)):
                output['Figure '+str(link+1)+' Link'][-1] = curr_path2


            try:        #Tables and caption 
                time.sleep(4)
                tabl = driver.find_elements('class name', 'table-wrap-title')
            except:
                time.sleep(6)
                tabl = driver.find_elements('class name', 'table-wrap-title')
            count_t = 0
            cap_tab = []
            for l3 in tabl: 
                z = l3.find_element('class name', 'caption')
                cap_tab.append(z.text)
                count_t+=1
            output['Number of Tables'][-1] = count_t
            for num in range(len(cap_tab)):
                output['Table '+str(num+1)+' caption'][-1] = cap_tab[num]

            
            driver.back()

        except:
            driver.back()
            print(title.text)

    #button “Next” for next page
    button = driver.find_element('css selector', f'.pagination-bottom-outer-wrap > div:nth-child(1) > button:nth-child({n})')
    link_not_work = True
    times_to_try = 0
    
    while link_not_work and times_to_try < 3:
        try:
            time.sleep(10)
            button.click()
            link_not_work = False
        except:
            print('error in third try')
            driver.refresh()
            times_to_try += 1
    n=3                #variable for Next button. From page 2 always n=3    
    time.sleep(8)
    driver.refresh()

df= pd.DataFrame.from_dict(output)
df.to_excel("/Users/janny/output.xlsx")
