import requests
from pathlib import Path
import zipfile

try:
    from lxml import etree
except ImportError:
    import xml.etree.ElementTree as etree

def get_file(url, filename, path=Path('downloads'), force=False):
    if not path.is_dir():
        path.mkdir()
    if (not (path / filename).is_file()) or force:
        print(f'Downloading {filename}')
        r = requests.get(url + filename)
        open(path / filename, "wb").write(r.content)

def unzip_file(filename, path=Path('unzipped'), force=False):
    if not path.is_dir():
        path.mkdir()
    if (not (path / (filename.name[:-3] + 'csv')).is_file()) or force:
        print(f'Unzipping {filename}')
        with zipfile.ZipFile(filename, 'r') as zip:
            if len(zip.infolist()) > 0:
                files = [f for f in zip.namelist() if not f.startswith('__MACOSX') and f.endswith('.csv')]
                if len(files) == 1:
                    zip.extract(files[0], path)
                if len(files) > 1:
                    for f in files:
                        zip.extract(f, path)

def get_files_list(url = 'https://s3.amazonaws.com/capitalbikeshare-data/', namespace='{http://s3.amazonaws.com/doc/2006-03-01/}'):
    r = requests.get(url)
    root = etree.fromstring(r.content)
    return [t.text for t in root.findall(f'.//{namespace}Key') if t.text.endswith('.zip')]