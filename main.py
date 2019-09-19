from selenium import webdriver
from bs4 import BeautifulSoup

input_text = input()
base_url = 'https://www.onlinejobs.ph'


def open_site(word):
    browser = webdriver.Firefox()
    browser.get(base_url + '/jobseekers/jobsearch')

    input = browser.find_element_by_id('jobkeyword')
    input.send_keys(word)

    button = browser.find_element_by_name('search')
    button.click()

    scrap_info(browser)
    browser.close()


def scrap_info(page):
    bs = BeautifulSoup(page.page_source, 'html.parser')

    content = bs.select('.latest-job-post')
    if len(content) > 0:
        for key, value in enumerate(content):
            job_title = value.find('h4').getText()
            job_position = value.find('span', {'class': 'badge'}).getText()
            job_url = value.find('a', href=True)['href']
            job_body = value.find('div', {'class': 'desc'}).getText()

            save_jobs(clean_text(job_title), clean_text(job_position), clean_text(job_url), clean_text(job_body))

        print('Done!')


def clean_text(text):
    return text.strip()


def save_jobs(title, position, url, body):
    with open('job_posting.txt', 'a+') as file:
        file.write(title + '\n')
        file.write(position + '\n')
        file.write(base_url + url + '\n')
        file.write(body + '\n')
        file.write('\n')


open_site(input_text)
