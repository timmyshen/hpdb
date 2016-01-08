import bs4
import pandas as pd
from bs4 import BeautifulSoup
import sys

def extract_table_cells(table):
    td_all = table.find_all('td')
    cells = [td.string.encode('ascii', 'ignore') for td in td_all
     if td.string is not None]
    return cells

def extract_key_value(table):
    td_key = table.find_all("td", class_='Label')
    td_value = [k.find_next_sibling('td', class_='value') for k in td_key]
    kstring = [k.string.strip().encode('ascii', 'ignore') if k.string is not None else k.string for k in td_key]
    vstring = [v.string if v is not None else '' for v in td_value]
    vstring = [v.strip().encode('ascii','ignore') if v is not None else v for v in vstring]
    return pd.DataFrame(zip(kstring,vstring),
        columns=['Key','Value'])

def kvlist2df(kvlist):
    return pd.DataFrame(zip(kvlist[0::2], kvlist[1::2]),
     columns=['Key', 'Value'])

def page2df(pagehtml):
    soup = BeautifulSoup(open(pagehtml), 'lxml')
    #soup = soup.encode('ascii')
    tables = soup.findAll('table')
    # kvs = extract_table_cells(tables[3])
    kvs = extract_key_value(tables[3])
    # df = kvlist2df(kvs[1:])
    #df.replace('\xa0', '', inplace=True)
    return kvs

# print page2df('naper_print.html')
if __name__ == '__main__':
    page = sys.argv[1]
    outfile = sys.argv[2]
    df = page2df(page)
    df.to_csv(outfile,index=False)
