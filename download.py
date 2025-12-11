# https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
# https://stackoverflow.com/questions/31804799/how-to-get-pdf-filename-with-python-requests
# https://stackoverflow.com/questions/43259717/progress-bar-for-a-for-loop-in-python-script
# https://stackoverflow.com/questions/14270698/get-file-size-using-python-requests-while-only-getting-the-header
# https://github.com/sivel/speedtest-cli/wiki
# https://stackoverflow.com/questions/1517616/stream-large-binary-files-with-urllib2-to-file/1517728#1517728
# https://docs.python.org/zh-tw/3/library/urllib.request.html

import re, sys
from tqdm import tqdm
from urllib.request import urlopen # Python 3

response = urlopen(sys.argv[1])
headers = dict(response.headers)

print(headers)

local_filename = re.findall("filename=(.+)", headers['Content-Disposition'])[0]
local_filename = local_filename.replace("\"","").replace("'","").replace(";","")
print(local_filename)

size = int(headers['Content-Length'])

CHUNK = 600000 #bytes

times = size/CHUNK
        
if (times-(size//CHUNK))>0:
    times+=1
        
times = int(times)

with open(local_filename, 'wb') as f:
    for t in tqdm(range(times)):
        chunk = response.read(CHUNK)
        if not chunk:
            break
        f.write(chunk)
