import  tarfile
import glob
import os
import http.server
import socketserver

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/x-tar')
        self.send_header('Content-Disposition', 'attachment; filename="cicilan.tar"')
        self.end_headers()
        tarpath = self.datapath + "/data.tar"
        tar = tarfile.open(tarpath, "w")
        for js in glob.glob(self.datapath + "/*.json"):
            tar.add(js)
        tar.close()
        with open(tarpath, 'rb') as file: 
            self.wfile.write(file.read()) 
        os.remove(tarpath)
        for root, dirs, files in os.walk(self.datapath):
            for name in files:
                os.remove(os.path.join(root, name))


def run_rapel(port, datapath):
    # Create an object of the above class
    handler_object = MyHttpRequestHandler
    handler_object.datapath = datapath

    my_server = socketserver.TCPServer(("", port), handler_object)
    my_server.allow_reuse_address = True
    # Star the server
    my_server.serve_forever()

