import re
import bs4
import requests

from flask import Flask, render_template_string

DOMAIN = 'https://habrahabr.ru/'
DEL_TAG = ['meta', 'script', 'style', 'title', 'pre', 'code', 'head']

app = Flask(__name__)


@app.route("/")
@app.route('/<path:url>')
def start(url=''):
    full_url = DOMAIN + url
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36',
        'Content-Type': 'text/html',
    }

    response = requests.get(full_url, headers=headers)
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    for link in soup.find_all(['link', 'script', 'a']):
        if link.parent.name == 'link':
            link['href'] = link['href'].replace('/images/favicons/', 'https://habrahabr.ru/images/favicons/')

        if link.name == 'script' and link.get('src'):
            link['src'] = link['src'].replace('/viewcount/custom/', 'https://habrahabr.ru/viewcount/custom/')

        if link.name == 'a' and link.get('href'):
            link['href'] = link['href'].replace('http://habrahabr.ru', '')
            link['href'] = link['href'].replace('https://habrahabr.ru', '')

    for text in soup.find_all(text=True):
        if text.parent.name in DEL_TAG:
            font = re.compile(r'(/fonts/0/)').sub(r'https://habrahabr.ru/fonts/0/', text)
            text.string.replace_with(font)
            continue

        if type(text) == bs4.element.Doctype or type(text) == bs4.element.Comment:
            continue

        text_re = re.compile(r'(\b\w{6}\b)').sub(r'\1™', text)
        text.string.replace_with(text_re)

    return render_template_string(str(soup))


if __name__ == "__main__":
    app.run()
