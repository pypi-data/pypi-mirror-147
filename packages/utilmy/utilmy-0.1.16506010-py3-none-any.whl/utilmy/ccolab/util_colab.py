



HELP1= """
#### Increase the RAMDISK space
! mount -o remount,size=16G /var/colab 

#### Stored as RAM DISK
! mkdir /var/colab/dataram/


### If you copy data here, loading is RAM Speed:
ls /var/colab/dataram/



#### 
from google.colab import drive
drive.mount('/content/drive')



#### In Batch mode (ie you can close Chrome and go sleep )
! cd  /content/drive/yourfolder/
! nohup  python3 run_1.py  &



"""


def help():
    print(HELP1)







