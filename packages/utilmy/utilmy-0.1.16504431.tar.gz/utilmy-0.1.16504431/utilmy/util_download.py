



COVEO_INTERACTION_DATASET_S3_URL = 'https://reclist-datasets-6d3c836d-6djh887d.s3.us-west-2.amazonaws.com/coveo_sigir.zip'
SPOTIFY_PLAYLIST_DATASET_S3_URL = 'https://reclist-datasets-6d3c836d-6djh887d.s3.us-west-2.amazonaws.com/small_spotify_playlist.zip'
MOVIELENS_DATASET_S3_URL = "https://reclist-datasets-6d3c836d-6djh887d.s3.us-west-2.amazonaws.com/movielens_25m.zip"




def google_download(url_or_id="https://drive.google.com/file/d/1iFrhCPWRITarabHfBZvR-V9B2yTlbVhH/view?usp=sharing" , 
                    dirout="./ztmp/", unzip=True ):
  """Download  file from google drive on disk + unzip

  Parameters
  ----------
     url_or_id: "https://drive.google.com/file/d/1iFrhCPWRITarabHfBZvR-V9B2yTlbVhH/view?usp=sharing" 



  Example
  -------
  import gdown
  url_or_id = "16MIleqoIr1vYxlGk4GKnGmrsCPuWkkpT"  
  dirout="./ztmp/"
      # a file
      url = "https://drive.google.com/uc?id=1l_5RK28JRL19wpT22B-DY9We3TVXnnQQ"
      output = "fcn8s_from_caffe.npz"
      gdown.download(url, output, quiet=False)

      # same as the above, but with the file ID
      id = "0B9P1L--7Wd2vNm9zMTJWOGxobkU"
      gdown.download(id=id, output=output, quiet=False)

      # same as the above, and you can copy-and-paste a URL from Google Drive with fuzzy=True
      url = "https://drive.google.com/file/d/0B9P1L--7Wd2vNm9zMTJWOGxobkU/view?usp=sharing"
      gdown.download(url=url, output=output, quiet=False, fuzzy=True)


      # a folder
      url = "https://drive.google.com/drive/folders/15uNXeRBIhVvZJIhL4yTw4IsStMhUaaxl"
      gdown.download_folder(url, quiet=True, use_cookies=False)

      # same as the above, but with the folder ID
      id = "15uNXeRBIhVvZJIhL4yTw4IsStMhUaaxl"
      gdown.download_folder(id=id, quiet=True, use_cookies=False)

  """
  import gdown, shutil, os, glob
  dirout = os.path.abspath(dirout)
  dirout = dirout.replace("\\","/")

  tag = url_or_id
  if "https:"in  url_or_id:
    tag = str(hash(url_or_id))

  dirout2 = dirout + f"/gdown_{tag}/"
  os.makedirs(dirout2, exist_ok=True)
  dir_cur = os.getcwd()

  os.chdir(dirout2)

  isfuzzy = True if '?usp=sharing' in url_or_id else False

  try :
    gdown.download(url_or_id,  quiet=False, fuzzy=isfuzzy)
    flist = glob.glob(dirout2 + "/*")
    print('Files downloaded', flist)
    if unzip:
      for fi in flist :
        shutil.unpack_archive(fi, dirout)
  except Exception as e:
    print(e)
  os.chdir(dir_cur) 
  return dirout 




def download_with_progress(url, destination):
    """
    Downloads a file with a progress bar
    :param url: url from which to download from
    :destination: file path for saving data
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    with tqdm.wrapattr(open(destination, "wb"), "write",
                       miniters=1, desc=url.split('/')[-1],
                       total=int(response.headers.get('content-length', 0))) as fout:
        for chunk in response.iter_content(chunk_size=4096):
            fout.write(chunk)


def get_cache_directory():
    """
    Returns the cache directory on the system
    """
    appname = "reclist"
    appauthor = "reclist"
    cache_dir = user_cache_dir(appname, appauthor)

    Path(cache_dir).mkdir(parents=True, exist_ok=True)

    return cache_dir





def download_page_image(query, out_dir="query1", genre_en='', id0="", cat="", npage=1) :
    """
        python prepro.py down_page  'メンス+ポロシャツ'    --out_dir men_fs_blue  


    """
    import time, os, json, csv, requests, sys, urllib
    from bs4 import BeautifulSoup as bs
    from urllib.request import Request, urlopen
    import urllib.parse


    path = "/datrakuten/" + out_dir + "/"
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
            rakuten_url = url_prefix  + f"/?p=+{page}"
            req    = Request(url=rakuten_url)
            source = urlopen(req).read()
            soup   = bs(source,'lxml')

            print('page', page, str(soup)[:5], str(rakuten_url)[-20:],  )

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
                        print(product_url + " Error Detected")
                    
                for simpleshop in individual_item.find_all('div',class_='merchant'):
                    shopname = simpleshop.a.text
                    break

                for review in individual_item.find_all('a',class_='dui-rating-filter'):
                    count_review = review.text

                if save == 0:
                    csv_writer.writerow([str(count)+'.jpg', id0, cat, genre_en,  product_name, product_price, shopname, product_url, rakuten_url, ])

        except Exception as e :
            print(e)
            time.sleep(2)
            continue

        page += 1

    print("Success", page-1, count)
