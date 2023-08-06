from urllib import request
import os
import glob
import shutil
import json
import base64
import tarfile

def run_reply(source, path, collector_path):
    request.urlretrieve(source, path)

    tr = tarfile.open(path)
    tr.extractall(path=collector_path)
    tr.close()

    def sending(path):
        with open(path, 'r') as payload:
            data = json.loads(payload.read())
            url = data['path']
            headers = data['headers']
            body = data['body']

            req = request.Request(url, method="POST")
            for hd in headers.keys():
               req.add_header(hd, headers[hd])
            data = base64.b64decode(body.encode("ascii"))
            resp = request.urlopen(req, data=data)
            ct = resp.read()

    for ln in glob.glob("%s/**/*.json" % collector_path, recursive=True):
        try:
            sending(ln)
        except ValueError:
            print("Format Error, we can't send this request")
    if os.path.isdir(collector_path):
        shutil.rmtree(collector_path)


