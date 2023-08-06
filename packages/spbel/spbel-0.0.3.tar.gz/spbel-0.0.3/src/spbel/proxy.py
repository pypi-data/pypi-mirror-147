import socketserver
from http import server
from urllib import request
import json
import base64
import os
import glob

class MyProxy(server.SimpleHTTPRequestHandler):

    def get_next_seq(self):
        al = [int(x.split(".")[0].split("/")[-1]) for x in glob.glob(self.datapath + "/*.json")]
        print(al)
        if len(al) == 0:
            return "1"
        else:
            al.sort()
            return str(al[-1] + 1)

    def do_GET(self):
        url=self.path
        self.send_response(200)
        self.end_headers()
        self.copyfile(request.urlopen(url), self.wfile)
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        body = base64.b64encode(post_data).decode('ascii') 
        data = {
                "path": self.path,
                "headers": dict(self.headers),
                "body": body
        }
        flname = self.datapath + "/%s.json" % self.get_next_seq()
        with open(flname, 'w') as target:
            target.write(json.dumps(data))
        self.send_response(200)
        self.end_headers()

def run_proxy(port,datapath):
    if not os.path.isdir(datapath):
        os.mkdir(datapath)
    for fl in glob.glob(datapath + "/*"):
        os.remove(fl)
    proxyclass = MyProxy
    proxyclass.datapath = datapath
    with socketserver.TCPServer(('', port), proxyclass) as httpd:
        try:
            httpd.allow_reuse_address = True
            httpd.serve_forever()
        except KeyboardInterrupt:
            httpd.shutdown()
            httpd.server_close()
