# -*- coding: utf-8 -*-
MNAME='utilmy.util_download'
HELP=""" Download utilities


"""
import os, glob, sys, time, json, functools, random, yaml, gc, copy, requests, shutil
import pandas as pd, numpy as np
from pathlib import Path; from collections import defaultdict, OrderedDict
from typing import List, Optional, Tuple, Union  ; from numpy import ndarray
from box import Box


from utilmy import pd_read_file, os_makedirs, pd_to_file, glob_glob

#############################################################################################
from utilmy import log, log2
def help():
    """function help        """
    from utilmy import help_create
    print( HELP + help_create(MNAME) )



#############################################################################################
def test_all() -> None:
    """function test_all   to be used in test.py         """
    log(MNAME)
    test1()


def test1() -> None:
    """function test1
    """
    d = Box({})
    dirtmp ="./ztmp/"


#############################################################################################
COVEO_INTERACTION_DATASET_S3_URL = 'https://reclist-datasets-6d3c836d-6djh887d.s3.us-west-2.amazonaws.com/coveo_sigir.zip'
SPOTIFY_PLAYLIST_DATASET_S3_URL  = 'https://reclist-datasets-6d3c836d-6djh887d.s3.us-west-2.amazonaws.com/small_spotify_playlist.zip'
MOVIELENS_DATASET_S3_URL         = "https://reclist-datasets-6d3c836d-6djh887d.s3.us-west-2.amazonaws.com/movielens_25m.zip"






#############################################################################################
def download_github(url="https://github.com/arita37/dsa2_data/blob/main/input/titanic/train/features.zip", 
                   dirout="./ztmp/"):
    """Fetch dataset from a given URL and save it.

    Parameters
    ----------
    :param url:   URL to send
    :param fileout:   Path to save files
    :param fileout:   File to save files

    Examples
    --------
    https://github.com/arita37/dsa2_data/raw/main/input/titanic/train/features.zip
    https://github.com/arita37/dsa2_data/raw/main/input/titanic/train/features.zip            
    https://raw.githubusercontent.com/arita37/dsa2_data/main/input/titanic/train/features.csv            
    https://raw.githubusercontent.com/arita37/dsa2_data/tree/main/input/titanic/train/features.zip             
    https://github.com/arita37/dsa2_data/blob/main/input/titanic/train/features.zip
    """
    log("###### Download ##################################################")
    from tempfile import mktemp, mkdtemp
    from urllib.parse import urlparse, parse_qs
    import pathlib, requests

    supported_extensions = [ ".zip" ]

    dirout = dirout.replace("\\", "/")
    os.makedirs(dirout, exist_ok=True)

    # urlx = url.replace(  "github.com", "raw.githubusercontent.com" )
    urlx = url.replace("/blob/", "/raw/")
    urlx = urlx.replace("/tree/", "/raw/")
    log(urlx)


    urlpath = urlx.replace("https://github.com/", "github_")
    urlpath = urlpath.split("/")
    fpath = "-".join(urlpath[:-1])[:-1]   ### prefix path normalized

    fname = urlpath[-1]  ## filaneme
    # assert "." in fname, f"No filename in the url {urlx}"

    dirout2 = dirout
    os.makedirs(dirout2, exist_ok= True)
    fileout_fullname = os.path.abspath( dirout2 + "/" + fname )
    log('#### Download saving in ', fileout_fullname)

    with requests.Session() as s:
        res = s.get(urlx)
        if res.ok:
            print(res.ok)
            with open(fileout_fullname, "wb") as f:
                f.write(res.content)
        else:
            raise res.raise_for_status()
    return fileout_fullname



def download_google(url_or_id="https://drive.google.com/file/d/1iFrhCPWRITarabHfBZvR-V9B2yTlbVhH/view?usp=sharing" , 
                    fileout="./ztmp/", unzip=True ):
      """Download  file from google drive on disk + unzip

      Parameters
      ----------
      url_or_id: "https://drive.google.com/file/d/1iFrhCPWRITarabHfBZvR-V9B2yTlbVhH/view?usp=sharing"



      Examples
      --------
      File:
      download_google(url_or_id="https://drive.google.com/file/d/1iFrhCPWRITarabHfBZvR-V9B2yTlbVhH/view?usp=sharing" ,
                        fileout="./ztmp/", unzip=True )

      download_google(url_or_id="16MIleqoIr1vYxlGk4GKnGmrsCPuWkkpT",
                        fileout="./ztmp/", unzip=True )

      Folder:
      download_google(url_or_id="https://drive.google.com/drive/folders/15uNXeRBIhVvZJIhL4yTw4IsStMhUaaxl",
                        fileout="./ztmp/", unzip=True )

      """
      import gdown, shutil, os, glob
      fileout = os.path.abspath(fileout)
      fileout = fileout.replace("\\","/")

      tag = url_or_id
      if "https:" in  url_or_id:
        tag = str(hash(url_or_id))

      dirout2 = fileout + f"/gdown_{tag}/"
      os.makedirs(dirout2, exist_ok=True)
      dir_cur = os.getcwd()

      os.chdir(dirout2)

      isfuzzy = True if '?usp=sharing' in url_or_id else False

      try :
        if 'folder' in url_or_id:
            gdown.download_folder(url_or_id, quiet=False, use_cookies=False)
        else :
            gdown.download(url_or_id,  quiet=False, fuzzy=isfuzzy)
        flist = glob.glob(dirout2 + "/*")
        print('Files downloaded', flist)
        if unzip:
          for fi in flist :
            shutil.unpack_archive(fi, fileout)
      except Exception as e:
        print(e)
      os.chdir(dir_cur)
      return fileout



def download_custom_pageimage(query, fileout="query1", genre_en='', id0="", cat="", npage=1) :
    """
        python  "$utilmy/util_download.py" download_page_image   --query 'メンス+ポロシャツ'    --out_dir men_fs_blue


    """
    import time, os, json, csv, requests, sys, urllib
    from bs4 import BeautifulSoup as bs
    from urllib.request import Request, urlopen
    import urllib.parse


    path = os.path.abspath(fileout + "/")
    path = path.replace("\\", "/")
    os.makedirs(path, exist_ok=True)
    # os.chdir(path)

    query2     = urllib.parse.quote(query, encoding='utf-8')
    url_prefix = 'httpl/' + query2
    ### https://search.rakuten.co.jp/search/mall/%E3%83%A1%E3%8384+blue+/?p=2
    print(url_prefix)
    print(path)

    csv_file   = open( path + 'ameta.csv','w',encoding="utf-8")
    csv_writer = csv.writer(csv_file, delimiter='\t')
    csv_writer.writerow(['path', 'id0', 'cat', 'genre_en', 'image_name', 'price','shop','item_url','page_url',  ])

    page  = 1
    count = 0
    while page < npage+1 :
        try:
            url_page = url_prefix  + f"/?p=+{page}"
            req    = Request(url=url_page)
            source = urlopen(req).read()
            soup   = bs(source,'lxml')

            print('page', page, str(soup)[:5], str(url_page)[-20:],  )

            for individual_item in soup.find_all('div',class_='searchresultitem'):
                count += 1
                save = 0
                shopname     = 'nan'
                count_review = 'nan'

                for names in individual_item.find_all('div',class_='title'):
                    product_name = names.h2.a.text
                    break

                for price in individual_item.find_all('div',class_='price'):
                    product_price = price.span.text
                    product_price = product_price .replace("円", "").replace(",", "") 
                    break
                
                for url in individual_item.find_all('div',class_='image'):
                    product_url = url.a.get('href')
                    break

                for images in individual_item.find_all('div',class_='image'):
                    try:
                        product_image = images.a.img.get('src')
                        urllib.request.urlretrieve(product_image, path + str(count)+".jpg")
                        # upload_to_drive(str(count)+'.jpg')
                        count += 1
                        break
                    except:
                        save = 1
                        print(product_image + " Error Detected")
                    
                for simpleshop in individual_item.find_all('div',class_='merchant'):
                    shopname = simpleshop.a.text
                    break

                for review in individual_item.find_all('a',class_='dui-rating-filter'):
                    count_review = review.text

                if save == 0:
                    csv_writer.writerow([str(count)+'.jpg', id0, cat, genre_en,  
                        product_name, product_price, shopname, product_url, url_page, ])

        except Exception as e :
            print(e)
            time.sleep(2)
            continue

        page += 1

    print("Success", page-1, count)




################################################################################################################
def download_with_progress(url, fileout):
    """
    Downloads a file with a progress bar
    :param url: url from which to download from
    :fileout: file path for saving data
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    with tqdm.wrapattr(open(fileout, "wb"), "write",
                       miniters=1, desc=url.split('/')[-1],
                       total=int(response.headers.get('content-length', 0))) as fout:
        for chunk in response.iter_content(chunk_size=4096):
            fout.write(chunk)



###############################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()



