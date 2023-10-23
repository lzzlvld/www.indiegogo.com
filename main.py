import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import datetime


def get_request(driver, url):
    driver.get(url)
    y = 10
    for timer in range(0,20):
        driver.execute_script("window.scrollTo(0, "+str(y)+")")
        y += 700
        time.sleep(1)
    data = driver.page_source
    soup = BeautifulSoup(data, 'lxml')
    return soup


def request(driver, url):
    driver.get(url)
    time.sleep(5)
    data = driver.page_source
    soup = BeautifulSoup(data, 'lxml')
    return soup


def main():
    WEBSITE_URL = 'https://www.indiegogo.com/'
    categories = {
        'education': 'https://www.indiegogo.com/explore/education?project_timing=all&sort=trending',
        'explore': 'https://www.indiegogo.com/explore/health-fitness?project_timing=all&sort=trending',
        'travel-outdoors': 'https://www.indiegogo.com/explore/travel-outdoors?project_timing=all&sort=trending',
        'video-games': 'https://www.indiegogo.com/explore/video-games?project_timing=all&sort=trending',
        'project_timing': 'https://www.indiegogo.com/explore/film?project_timing=all&sort=trending',
        'phones-accessories': 'https://www.indiegogo.com/explore/phones-accessories?project_timing=all&sort=trending'
    }

    items = []
    session = requests.Session()

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    category_index = 0
    id = 0
    for category in categories:
        list = []
        for key in categories.keys():
            list.append(key)
        soup = get_request(driver, categories[category])
        project_headers = soup.find_all('div', {'class': 'baseDiscoverableCard'})
        print(len(project_headers))

        
        project_links = []
        for project_header in project_headers:
            project_link = WEBSITE_URL + project_header.next_element['href']
            project_links.append(project_link)


        for project_link in project_links:
            id += 1
            soup = request(driver, project_link)
            try:
                image = soup.find('iframe', {'class': 'videoWrapper'})['src']
            except:
                image = 'No image'
            
            try:
                location = soup.find('div', {'class': 'basicsSection-statusLabel is-hidden-tablet t-label--sm fundingColor'}).text.strip()
            except:
                location = 'Ended'

            try:
                title = soup.find('div', {'class': 'basicsSection-title is-hidden-tablet t-h3--sansSerif'}).text.strip()
            except:
                title = 'None'

            try:
                short_story = soup.find('div', {'class': 'basicsSection-tagline widescreen t-body--sansSerif--lg'}).text.strip()
            except:
                short_story = None

            try:
                campaignowner = soup.find('div', {'class': 'mobile campaignOwnerName-tooltip t-body--sansSerif'}).text.strip()
            except:
                campaignowner = None

            try:
                campaigncount = soup.find('div', {'class': 'basicsCampaignOwner-details-count'}).text.strip()
            except:
                campaigncount = None

            try:
                string1 = soup.find('span', 'basicsGoalProgress-claimedOrBackers').text
                string2 = string1.replace('by', "")
                backers = string2.replace('backers', "")
            except:
                backers = 'No backer'

            try:
                string = soup.find('span', {'class': 'basicsGoalProgress-amountSold t-h5--sansSerif t-weight--bold'}).text.strip()
                salary = string.replace('€', "")
                print(salary)
            except:
                salary = 'No Data'

            try:
                string = soup.find('span', 'basicsGoalProgress-progressDetails-detailsGoal-goalPercentageOrInitiallyRaised').text.strip()
                if '%' in string:
                    separator = '%'
                    campaignpercent = string.split(separator, 1)[0]
                else:
                    campaignpercent = '100'
            except:
                campaignpercent = 'No Data'

            try:
                campaignende = soup.find('div', 'basicsGoalProgress-progressDetails-detailsTimeLeft column t-body--sansSerif t-align--right').next_element.text
            except:
                campaignende = 'Ended'

            try:
                description = soup.find('div', {'class': 'routerContentStory-storyBody'}).text.strip()
            except:
                description = None
            
            time1 = time.ctime()

            element = {
            'id': id,
            'cat_id': list[category_index],
            'title': title,
            'page_url': project_link,
            'campaignpercent(%)': campaignpercent,
            'campaignende(days)': campaignende,
            'location': location,
            'campaignowner': campaignowner,
            'campaigncount': campaigncount,
            'image': image,
            'salary(€)': salary,
            'backers': backers,
            'short_story': short_story,
            'description': description,
            'created_at': time1,
            'updated_at': time1,
            }

            items.append(element)
        category_index += 1

    driver.close()

    df = pd.DataFrame(items)
    df.to_excel('exported_data.xlsx', index=False)


if __name__ == '__main__':
    main()