from urllib.request import urlopen
from pyquery import PyQuery
import re


def download_html(url):
    with urlopen(url) as webpage:
        return webpage.read().decode()


# for now loads objections and replies only from questions where there are as many replies as objections,
def extract_objections(html):
    objections = []
    replies = []
    pq = PyQuery(html)
    paragraphs = pq('p')
    for paragraph in paragraphs.items():
        text = paragraph.text()
        if re.search('^Objection [1-9]. ', text):
            text = re.sub('^Objection [1-9]. ', '', text)
            objections.append(text)
        elif re.search('^Reply to Objection [1-9]. ', text):
            text = re.sub('^Reply to Objection [1-9]. ', '', text)
            replies.append(text)
    if len(objections) == len(replies):
        return objections, replies
    return [], []


base_url = 'https://www.newadvent.org/summa/'


def download_question(index):
    html = download_html(base_url + str(index) + '.htm')
    objections, replies = extract_objections(html)
    for objection in objections:
        objections_file.write(objection + '\n')
    for reply in replies:
        replies_file.write(reply + '\n')


with open('objections.txt', 'a') as objections_file, open('replies.txt', 'a') as replies_file:
    # Prima pars
    for q in range(1001, 1119):
        download_question(q)
    # Prima Secundae Partis
    for q in range(2001, 2114):
        download_question(q)
    # Secunda Secundae Partis
    for q in range(3001, 3189):
        download_question(q)
    # Tertia Pars
    for q in range(4001, 4090):
        download_question(q)
    # Supplementum Tertiae Partis
    for q in range(5001, 5099):
        download_question(q)
