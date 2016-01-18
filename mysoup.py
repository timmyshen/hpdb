import bs4
import pandas as pd
from bs4 import BeautifulSoup
import sys

def extract_table_cells(table):
    '''
    deprecated
    '''
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

def extract_tablelabel(table):
    td_table = table.find_all('tr')
    td_key1 = td_table.pop(0)
    td_key = [k.string for k in td_key1.find_all('td')]
    table_dict = dict()
    for t in td_table:
        td = t.find_all('td')
        for i,item in enumerate(td):
            if item['class'] == ['Label']:
                label = item.string
            elif item['class'] == ['value']:
                if label is None:
                    continue
                key = (label+td_key[i].string).encode('ascii','ignore')
                value = item.string
                table_dict[key] = value
    # print table_dict
    return pd.DataFrame(table_dict.items(),columns=['Key','Value'])


def extract_span(table):
    td_key = table.find_all("span", class_='iLabel')
    td_value = [k.find_next_sibling('span', class_='value') for k in td_key]
    kstring = [k.string.strip().encode('ascii', 'ignore') if k.string is not None else k.string for k in td_key]
    vstring = [v.string if v is not None else '' for v in td_value]
    vstring = [v.strip().encode('ascii','ignore') if v is not None else v for v in vstring]
    return pd.DataFrame(zip(kstring,vstring),
        columns=['Key','Value'])



def kvlist2df(kvlist):
    '''
    deprecated
    '''
    return pd.DataFrame(zip(kvlist[0::2], kvlist[1::2]),
     columns=['Key', 'Value'])

def page2df(pagehtml):
    soup = BeautifulSoup(open(pagehtml), 'lxml')
    #soup = soup.encode('ascii')
    tables = soup.findAll('table')
    # kvs = extract_table_cells(tables[3])
    # tables_extracted = [tables[3],tables[4]]
    tablelabel = tables[13]
    span_extracted = tables[14]
    kvs1 = extract_key_value(tables[3])
    kvs2 = extract_key_value(tables[4])
    kvs3 = extract_tablelabel(tablelabel)
    kvs4 = extract_span(span_extracted)
    # kvs3 = extract_key_value(tables[7])
    # df = kvlist2df(kvs[1:])
    #df.replace('\xa0', '', inplace=True)
    return pd.concat([kvs1,kvs2,kvs3,kvs4])

# df = page2df('naper_print.html')


if __name__ == '__main__':
    page = sys.argv[1]
    outfile = sys.argv[2]
    df = page2df(page)
    df.to_csv(outfile,index=False)
