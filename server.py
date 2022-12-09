# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "localhost"
serverPort = 80

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            try:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(bytes("<html><head><title>IDPay Receiver Get Method Data</title></head>", "utf-8"))
                var_main = self.path.split("&")
                var1 = var_main[0].replace('/?', '').replace('=', '').replace('status', '')
                var2 = var_main[1].replace('=', '').replace('track_id', '')
                var3 = var_main[2].replace('=', '').replace('id', '')
                var4 = var_main[3].replace('=', '').replace('order_id', '')
                self.wfile.write(bytes("<p>status : \n<b>{path}</b></p>".format(path=var1), "utf-8"))
                self.wfile.write(bytes("<p>track_id : \n<b>{path}</b></p>".format(path=var2), "utf-8"))
                self.wfile.write(bytes("<p>id :\n<b>{path}</b></p>".format(path=var3), "utf-8"))
                self.wfile.write(bytes("<p>order_id : \n<b>{path}</b></p>".format(path=var4), "utf-8"))
                self.wfile.write(bytes("<p><b><i>The information was received successfully.</i></b></p>", "utf-8"))
                self.wfile.write(bytes("<body>", "utf-8"))
                print("The information was received successfully.")
            except:
                self.wfile.write(bytes("<p><b>Error Data For Query.</b></p>".format(path=var1), "utf-8"))
                print("Error Data For Query.")

        except IndexError:
            self.wfile.write(bytes("<p><b>Error Data For Query.</b></p>".format(path=var1), "utf-8"))
            print("Error Data For Query.")

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")