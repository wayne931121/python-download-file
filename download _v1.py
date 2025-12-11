# https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
# https://stackoverflow.com/questions/31804799/how-to-get-pdf-filename-with-python-requests
# https://stackoverflow.com/questions/43259717/progress-bar-for-a-for-loop-in-python-script
# https://stackoverflow.com/questions/14270698/get-file-size-using-python-requests-while-only-getting-the-header
# https://github.com/sivel/speedtest-cli/wiki

import re, requests, sys
from tqdm import tqdm
# import speedtest
# threads = None
# s = speedtest.Speedtest()
# speed = s.download(threads=threads)

def download_file(url):
    with requests.get(url, stream=True) as r:
        print(r.headers)
        local_filename = re.findall("filename=(.+)", r.headers['content-disposition'])[0]
        local_filename = local_filename.replace("\"","").replace("'","").replace(";","")
        print(local_filename)
        size = int(r.headers['Content-Length'])
        
        r.raise_for_status()
        
        #chunk_size = 3*1024*1024 #3MB, in bytes.
        
        #chunk_size = int(sys.argv[2]) #MB
        #chunk_size *= 1024*1024
        
        #chunk_size = ((speed/8)//1000)*1000
        chunk_size = 600000
        
        times = size/chunk_size
        
        if (times-(size//chunk_size))>0:
            times+=1
        
        times = int(times)
        
        with open(local_filename, "wb") as f:
            
            c = r.iter_content(chunk_size=chunk_size)
            
            for t in tqdm(range(times)):
                
                chunk = next(c)
                f.write(chunk)
            
    return 0

try:
    download_file(sys.argv[1])
except KeyboardInterrupt:
    pass
