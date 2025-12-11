# https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
# https://stackoverflow.com/questions/31804799/how-to-get-pdf-filename-with-python-requests
# https://stackoverflow.com/questions/43259717/progress-bar-for-a-for-loop-in-python-script
# https://stackoverflow.com/questions/14270698/get-file-size-using-python-requests-while-only-getting-the-header
# https://github.com/sivel/speedtest-cli/wiki
# https://stackoverflow.com/questions/1517616/stream-large-binary-files-with-urllib2-to-file/1517728#1517728
# https://docs.python.org/zh-tw/3/library/urllib.request.html

import re, sys
from tqdm import tqdm
from urllib.request import urlopen,Request # Python 3

response = urlopen(sys.argv[1])
headers = dict(response.headers)

print(headers)

local_filename = re.findall("filename=(.+)", headers['Content-Disposition'])[0]
local_filename = local_filename.replace("\"","").replace("'","").replace(";","")
print(local_filename)

size = int(headers['Content-Length'])

a = [0,int(size/2)-1,int(size/2)-1+1,size-1]
b = [a[1]-a[0]+1,a[3]-a[2]+1]

CHUNK = 600000 #bytes

times = [b[0]/CHUNK,b[1]]

if (times[0]-(b[0]//CHUNK))>0:
    times[0]+=1
        
if (times[1]-(b[1]//CHUNK))>0:
    times[1]+=1

times = [int(i) for i in times]

def f1():
    req = Request(sys.argv[1])
    req.add_header("Range", "bytes=%d-%d"%(a[0],a[1]))
    response = urlopen(req)
    with open("1", 'wb') as f:
        for t in tqdm(range(times[0]),leave=0):
            chunk = response.read(CHUNK)
            if not chunk:
                break
            f.write(chunk)

def f2():
    req = Request(sys.argv[1])
    req.add_header("Range", "bytes=%d-%d"%(a[2],a[3]))
    response = urlopen(req)
    with open("2", 'wb') as f:
        for t in tqdm(range(times[1]),leave=0):
            chunk = response.read(CHUNK)
            if not chunk:
                break
            f.write(chunk)

import threading
t1 = threading.Thread(target=f1)
t2 = threading.Thread(target=f2)

t1.start()
t2.start()

t1.join()
t2.join()

with open(local_filename, 'wb') as f:
    with open("1", 'rb') as f1:
        f.write(f1.read())
    with open("2", 'rb') as f1:
        f.write(f1.read())