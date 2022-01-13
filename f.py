
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import urlopen


def textextract2(url):
    address = url
    soup = BeautifulSoup(urlopen(address).read(), 'lxml')
    span = soup.find("div", {"class": "article__body-content"})
    paras = [x for x in span.findAllNext("p")]
    middle = "\n\n".join(["".join(x.findAll(text = True)) for x in paras[: -1]])
    return(middle)

def textextract1(url):
    y = " "
    url = urlopen(url)
    content = url.read()
    soup = BeautifulSoup(content, 'lxml')
    table = soup.find("div",{"class":"ssrcss-uf6wea-RichTextComponentWrapper e1xue1i85"})
    paras = [x for x in table.findAllNext("p")]
    middle = "\n\n".join(["".join(x.findAll(text = True)) for x in paras[: -1]])
    return(middle)


def newextract(url):
    y = " "
    url = urlopen(url)
    content = url.read()
    soup = BeautifulSoup(content, 'lxml')
    table = soup.find("div",{"class":"gel-layout__item gel-2/3@l"})
    paras = [x for x in table.findAllNext("p")]
    middle = "\n\n".join(["".join(x.findAll(text = True)) for x in paras[: -1]])
    return(middle)