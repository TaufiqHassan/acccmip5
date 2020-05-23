# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 17:43:49 2019

@author: Taufiq
"""

from urllib.request import urlopen # web scraping
import os, sys
import requests
import urllib.request
import re
from pathlib import Path

class color:
   PURPLE = '\033[35m'
   CYAN = '\033[36m'
   BLUE = '\033[34m'
   LBLUE='\033[94m'
   GREEN = '\033[32m'
   LGREEN='\033[92m'
   YELLOW = '\033[33m'
   RED = '\033[31m'
   LRED='\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class _fetch_url(object):    
    def __init__(self, url):
        self.url = url
        
    def __enter__(self):
        self.source = urlopen(self.url)
        fetched_data = str(self.source.read())
        return fetched_data

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.source.close()
        
class HidePrint:
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._stdout

class _dir_path(object):
    
    @staticmethod
    def _get_dir(path):
        if (path == ''):
            p=Path('.')
            dir_path = p.absolute() / 'CMIP5'
        else:
            dir_path = Path(path)
        return dir_path
    
    def _make_dir(self):
        p=Path('.')
        print("\nCurrent directory: ", p.absolute())
        print("\nDefault directory: ", p.absolute() / 'CMIP5')
        path = input("Please specify a directory here:\n")
        dir_path = _dir_path._get_dir(path)
        print("Selected directory: ", dir_path)
        if not os.path.exists(dir_path):
            print("\n"+str(dir_path)+" doesn't exist. Creating one...\n")
            os.makedirs(str(dir_path))
        return dir_path

def _choose_server():
    url3_4 = "https://esgf-data.dkrz.de/search/cmip5-dkrz/"
    url3_3 = "https://esgf-index1.ceda.ac.uk/search/cmip5-ceda/"
    url3_2 = "https://esgf-node.ipsl.upmc.fr/search/cmip5-ipsl/"

    try:
        if (requests.get(url3_2,timeout=10)):
            _Curl = url3_2
    except:
        try:
            if (requests.get(url3_3,timeout=10)):
                _Curl = url3_3
        except:
            try:
                if (requests.get(url3_4,timeout=10)):
                    _Curl = url3_4
            except:
                print("\nAll servers down!!\nCheck back later.")
    return _Curl

def _choose_server2():
    url4_4 = "https://esgf-node.ipsl.upmc.fr/esg-search/wget?project=CMIP5"
    url4_2 = "https://esgf-index1.ceda.ac.uk/esg-search/wget?project=CMIP5"
    url4_3 = "https://esgf-data.dkrz.de/esg-search/wget?project=CMIP5"

    try:
        if (requests.get(url4_2,timeout=10)):
            _Durl = url4_2
    except:
        try:
            if (requests.get(url4_3,timeout=10)):
                _Durl = url4_3
        except:
            try:
                if (requests.get(url4_4,timeout=10)):
                    _Durl = url4_4
            except:
                print("\nAll servers down!!\nCheck back later.")
    return _Durl


class _Construct_urls(object):
    
    _limit = 10000
    _Durl = "https://esgf-node.llnl.gov/esg-search/wget?project=CMIP5"
    
    def __init__(self,var,mod,realm,exp,freq,proj='CMIP5'):
         self.var = var
         self.mod = mod
         self.realm = realm
         self.exp = exp
         self.freq = freq
         
    def _add_options(self, x, zz):
        if (x=='mod'):
            return "&model="+str(self.mod[zz])
        if (x=='exp'):
            return "&experiment="+str(self.exp[zz])
        if (x=='freq'):
            return "&time_frequency="+str(self.freq[zz])
        if (x=='realm'):
            return "&realm="+str(self.realm[zz])
        if (x=='var'):
            return "&variable="+str(self.var[zz])
            
        
    def _get_url(self):
        if (self.mod):
            for zz in range(len(self.mod)):
               self._Durl = self._Durl + self._add_options('mod', zz)
        if (self.exp):
            for zz in range(len(self.exp)):
                self._Durl = self._Durl + self._add_options('exp',zz)
        if (self.var):
            for zz in range(len(self.var)):
                    self._Durl = self._Durl + self._add_options('var',zz)
        if (self.freq):
            for zz in range(len(self.freq)):
               self._Durl = self._Durl + self._add_options('freq',zz)
        if (self.realm):
            for zz in range(len(self.realm)):
                    self._Durl = self._Durl + self._add_options('realm',zz)
        return self._Durl+"&limit="+str(self._limit)
#        return self._Durl
     
    @classmethod
    def _set_limit(cls, limit):
        cls._limit = limit
        return cls._limit
    
    @classmethod
    def _set_Durl(cls, _Durl):
        cls._Durl = _Durl
        return cls._Durl
    
    def _get_wget(self, keep):
        url = self._get_url()
        try:
            requests.get(url, timeout = 10)
            p = Path('.')
            dir_path = p.absolute() / 'wget_script.sh'
            urllib.request.urlretrieve(url, str(dir_path))
        except:
            self._Durl = _Construct_urls._set_Durl(_choose_server2())
            url = self._get_url()
            p = Path('.')
            dir_path = p.absolute() / 'wget_script.sh'
            urllib.request.urlretrieve(url, str(dir_path))

        with open(str(dir_path)) as f:
            urls = f.read()
#            print(urls)
#            text=self.var[0]+'_'+self.freq[0]+'.*.nc'
#            links = re.findall(text,urls)
            link = re.findall('http://.*.nc',urls)
            if self.var==None or self.exp==None:
                links=link
            else:
                var_list = ['/' + s + '_' for s in self.var] # getting the variables
                exp_list = ['_' + s + '_' for s in self.exp] # getting the experiments
                links_v = [url for url in link if any(sub in url for sub in var_list)]
                links = [url for url in links_v if any(sub in url for sub in exp_list)]
            f.close()
        if (keep==0):
            os.remove(str(dir_path))
        return links

class _realizations(object):  

    def __init__(self,links):
         self.links = links
    
    def _all_realizations(self):
                
        er=[0]*len(self.links)
        for i in range(len(self.links)):
            try:
                er[i]=int(self.links[i].split('/')[len(self.links[i].split('/'))-1].split('_r')[1][0:2])
            except IndexError:
                try:
                    er[i]=int(self.links[i].split('/')[len(self.links[i].split('/'))-1].split('-r')[1][0:2])
                except:
                    er[i]=int(self.links[i].split('/')[len(self.links[i].split('/'))-1].split('-r')[1][0])
            except:
                try:
                    er[i]=int(self.links[i].split('/')[len(self.links[i].split('/'))-1].split('_r')[1][0])
                except ValueError:
                    er[i]=int(self.links[i].split('/')[len(self.links[i].split('/'))-1].split('_r')[2][0])
      
        ser=set(er)
        if 0 in ser:
            ser.remove(0)
        rlzn = list(ser)
        
        return rlzn

class _extract_info:
    
    def __init__(self,var,mod,realm,exp,freq,n_files,rlzn):
         self.var = var
         self.mod = mod
         self.realm = realm
         self.exp = exp
         self.freq = freq
         self.n_files = n_files
         self.rlzn = rlzn
    
    def _get_info(self):
         links = []
         links=_Construct_urls(self.var, self.mod, self.realm, self.exp, self.freq)._get_wget(0)
         rlzn = _realizations(links)._all_realizations()
         n_files=len(links)
         _mod=set()
         _realm=set()
         _exp=set()
         _var=set()
         _freq=set()
         for link in links:
             data=link.split('_')
             if (len(data)==6):
                 if '/' in data[1]:
#                     print(data)
                     _mod.add(data[3])
                     _realm.add(data[1].split('/')[7])
                     _exp.add(data[4])
                     _var.add(data[1].split('/')[(len(data[1].split('/')))-1])
                     _freq.add(data[1].split('/')[6])
                 else:  
                     _mod.add(data[2])
                     _realm.add(data[0].split('/')[12])
                     _exp.add(data[3])
                     _var.add(data[0].split('/')[(len(data[0].split('/')))-1])
                     _freq.add(data[0].split('/')[13])
             elif (len(data)==7):
                 if '/' in data[1]:
                     _mod.add(data[3])
                     _realm.add(data[1].split('/')[7])
                     _exp.add(data[4])
                     _var.add(data[1].split('/')[(len(data[1].split('/')))-1])
                     _freq.add(data[1].split('/')[6])
                 elif '/' in data[2]:
                     _mod.add(data[4])
                     _realm.add(data[2].split('/')[7])
                     _exp.add(data[5])
                     _var.add(data[2].split('/')[(len(data[2].split('/')))-1])
                     _freq.add(data[2].split('/')[6])
                 else:
                     _mod.add(data[2])
                     _realm.add(data[1])
                     _exp.add(data[3])
                     _var.add(data[0].split('/')[(len(data[0].split('/')))-1])
                     _freq.add(data[0].split('/')[13])
             else:
                 _mod.add(data[4])
                 _realm.add(data[3])
                 _exp.add(data[5])
                 _var.add(data[2].split('/')[(len(data[2].split('/')))-1])
                 _freq.add(data[2].split('/')[8])
                    
            
         return _extract_info(list(_var),list(_mod),list(_realm),list(_exp),list(_freq),n_files,rlzn)
   
class TooSlowException(Exception):
    pass

def convertBToMb(bytes):
    """converts Bytes to Megabytes"""
    bytes = float(bytes)
    megabytes = bytes / 1048576
    return megabytes

def _check_list(item):
    try:
        if (type(item.replace("'",'').strip('[]').split(','))==list):
            lm = str(item).replace("'",'').strip('[]').split(',')
            lm_nospace = [x.strip() for x in lm]
            item = str(lm_nospace).replace("'",'').strip('[]')
    except:
        pass
    return item

def _mod_help():
    print("\n"+color.PURPLE+"                <<You are using the CMIP5DB module now>>"+color.END)
    print("\nUse 'show' as the -m/-e/-f/-v/-r argument option instead of the names\n")
    print(color.BOLD+color.UNDERLINE+"Example:"+color.END+" acccmip -o M -m show >>> will generate a list of all currently available models in the CMIP5 database.")
    
def _get_rlzn_links(r,all_rlzn,links):    
    new_links=[]
    for rlzn in r:
        if rlzn in str(all_rlzn):
            for url in links:
                try:
                    try:
                        if (int(rlzn) == int(url.split('/')[len(url.split('/'))-1].split('-r')[1][0:2])):
                            new_links.append(url)
                    except:
                        if (int(rlzn) == int(url.split('/')[len(url.split('/'))-1].split('-r')[1][0])):
                            new_links.append(url)
                except:
                    try:
                        if (int(rlzn) == int(url.split('/')[len(url.split('/'))-1].split('_r')[1][0:2])):
                            new_links.append(url)
                    except:
                        try:
                            if (int(rlzn) == int(url.split('/')[len(url.split('/'))-1].split('_r')[1][0])):
                                new_links.append(url)
                        except:
                            if (int(rlzn) == int(url.split('/')[len(url.split('/'))-1].split('_r')[2][0])):
                                new_links.append(url)
        else:
            print(color.LRED+"\nSelected realzation is not available!"+color.END)
            raise SystemExit
    return new_links

def _get_skipped_links(links,val):
    skipped_items = [x.strip() for x in val.split(',')]
    new_links=[]
    for url in links:
        for item in skipped_items:
            if str(item) in url:
                new_links.append(url)
    return list(set(links)-set(new_links))
        
def _manual_wget(passed_urls,unused_links):
    def uncommon_elements(list1, list2):
        return [element for element in list1 if element not in list2]
    
    urls=passed_urls+unused_links
    l=[]
    with open("wget_script.sh") as f:
        for line in f:
            l.append(line.strip())
    s=[]
    for item in l:
        for url in urls:
            if url in item:
                s.append(item)  
    a = uncommon_elements(l,s)   
    with open('out.sh','w') as out:
        for item in a:
            out.write(item+"\n")
    f.close()
    out.close()
    os.remove('wget_script.sh')
    os.rename('out.sh', 'wget_script.sh')