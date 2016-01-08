import bs4
import pandas as pd
from bs4 import BeautifulSoup
import sys

def extract_table_cells(table):
    td_all = table.find_all('td')
    cells = [td.string.encode('ascii', 'ignore') for td in td_all
     if td.string is not None]
    return cells

def kvlist2df(kvlist):
    return pd.DataFrame(zip(kvlist[0::2], kvlist[1::2]),
     columns=['Key', 'Value'])

def page2df(pagehtml):
    soup = BeautifulSoup(open(pagehtml), 'lxml')
    #soup = soup.encode('ascii')
    tables = soup.findAll('table')
    kvs = extract_table_cells(tables[3])
    df = kvlist2df(kvs[1:])
    #df.replace('\xa0', '', inplace=True)
    return df

if __name__ == '__main__':
    page = sys.argv[1]
    outfile = sys.argv[2]
    df = page2df(page)
    df.to_csv(outfile)
