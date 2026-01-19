# Python script to scrape an article given the url of the article and store the extracted text in a file
# Url: https://medium.com/@subashgandyer/papa-what-is-a-neural-network-c5e5cc427c7
import os
import requests
import re
import sys
# Code here - Import BeautifulSoup library
from bs4 import BeautifulSoup
import sys
# Code ends here
# function to get the html source text of the medium article
def get_page():
    global url

    url = input("Enter url of a Medium article: ").strip()

    # The original Medium links may return 403 when accessed via script
    if not re.match(r'https?://(web.archive.org/.*medium.com/|medium.com/)', url):
        print('Please enter a valid website, or make sure it is a Medium article')
        sys.exit(1)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    # Send GET request
    res = requests.get(url, headers=headers)
    res.raise_for_status()

    print(f"HTML downloaded, length: {len(res.text)}")
    soup = BeautifulSoup(res.text, 'html.parser')
    return soup

# function to remove all the html tags and replace some with specific strings
def clean(text):
    rep = {"<br>": "\n", "<br/>": "\n", "<li>": "\n"}
    rep = dict((re.escape(k), v) for k, v in rep.items()) 
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    text = re.sub('<(.*?)>', '', text)
    return text

# function to collect text from <p> tags
def collect_text(soup):
    text = f'URL: {url}\n\n'
    para_text = soup.find_all('p')
    print(f"Number of paragraphs found: {len(para_text)}")
    for para in para_text:
        text += f"{para.text}\n\n"
    return text
# function to save file in the current directory
def save_file(text):
    if not os.path.exists('./scraped_articles'):
        os.mkdir('./scraped_articles')
        print("Folder scraped_articles created")

    name = url.rstrip('/').split("/")[-1]
    print(name)
    fname = f'scraped_articles/{name}.txt'

    # write a file using with (2 lines)
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(text)
    # Code ends here

    print(f'File saved in directory {fname}')

# Main execution
if __name__ == '__main__':
    soup = get_page()
    text = collect_text(soup)
    text = clean(text)
    save_file(text)

    # https://web.archive.org/web/20191126074327/https://medium.com/@subashgandyer/papa-what-is-a-neural-network-c5e5cc427c7
