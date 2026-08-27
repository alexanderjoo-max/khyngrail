import http.server, os, socketserver, functools
ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=ROOT)
class S(socketserver.TCPServer):
    allow_reuse_address = True
with S(("127.0.0.1", 4321), H) as httpd:
    print("serving", ROOT, "on http://localhost:4321")
    httpd.serve_forever()
