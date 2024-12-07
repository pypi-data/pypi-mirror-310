from fsspec import url_to_fs
import time

if __name__ == '__main__':
    bucket = 'aind-open-data'
    fs, path = url_to_fs(f's3://{bucket}')
    start = time.time()    
    exaspims = fs.glob(f'{bucket}/exaSPIM_*')
    elapsed = time.time() - start
    print(len(exaspims))
    print(elapsed)