from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib #Only for parse.unquote and parse.unquote_plus.
import json
import base64
from typing import Union, Optional
import re
# If you need to add anything above here you should check with course staff first.
#globals for sale
sale_active= True
sale_message = "No sale at the moment"
#contact page globals
acceptableKeys = ["name","email","date","ship-condition","new-customer"]
next_id = 0
contact = {
    "name": "mr pirate",
    "email": "mpirate@gmail.com",
    "date": "2023-10-3",
    "ship-condition": "no repairs needed",
    "new-customer": "no",
    "id": next_id
}
contacts = [contact]
#user and password info
user = "admin"
password = "password"
#function for password
def login(method: str, url: str, body: Optional[str], headers: dict[str, str]):
    if("Authorization" not in headers):
        return "no lol",401, {"WWW-Authenticate":'Basic realm="User Visible Realm"', "Content-Type": "text/plain"}
    encoded = headers["WWW-Authenticate"][6:]
    decoded = base64.b64decode(encoded).decode("utf-8")
    if(decoded[0:decoded.find(":")] == user and decoded[decoded.find(":")+1:] == password):
        return
    return "no lol",403, {"WWW-Authenticate":'Basic realm="User Visible Realm"', "Content-Type": "text/plain"}


def contactsToHTML():
    text = ""
    for x in range(len(contacts)):
        text += "<tr id="+str(contacts[x]["id"])
        text += "><td>"+contacts[x]["name"] 
        text += "</td><td>"+contacts[x]["email"]
        text += "</td><td class='date-entry'>"+contacts[x]["date"]
        text += "<span class='time-until'></span></td><td>"+contacts[x]["ship-condition"]
        text +="</td><td>"+contacts[x]["new-customer"]+"</td>"
        text += "<td><button id='row-delete' onclick='deleteRow(this)'>delete row</button></td></tr>"
            
    return text       
def showContactLog():
     test = """
          <!doctype html>
<html lang="en">
    <head>
        <title>Contact Log</title>
        <meta charset="UTF-8">
        <link href="/main.css" rel="stylesheet" type="text/css" id="light">
        <script src="/js/main.js" async></script>
        <script src="/js/table.js" async></script>
    </head>
    <body>
        <nav>
            <p><a href="/">Main</a></p>
            <p><a href="/testimonies">Testimonials</a></p>
            <p><a href="/contact">Contact Us</a></p>
            <P><a href="/admin/contactlog">Contactlog</a></p>
            <p><button id="dark-mode" onclick="toggle_style()">Dark Mode</button></p>
        </nav>
        <h1>My contact and appointments</h1>

        <div id="sale-controller">
            <h2>Set Sale</h2>
            <label for="message-field">Sale message:</label>
            <input type="text" name="message" id="message-field">
            <button id="submit-sale" onclick="submitSale()">Set Sale</button>
            <button id="end_sale">End Sale</button>
        </div>

        <table id='contact-log'>
            <tr>
                <th>Name</th>
                <th>email</th>
                <th>Prefered appointment day</th>
                <th>Requested repairs</th>
                <th>New customer</th>
                <th>Delete entry</th>
            </tr>
            """
     # time to build contact
     test += contactsToHTML()
     test += """
        
        </table>

    </body>
</html>
          
          """
     return test, 200, {"Content-Type" : "text/html; charset=utf-8"}

def updateContacts(key,value):
    global next_id
    next_id = next_id + 1
    c = {"name": "mr pirate",
    "email": "",
    "date": "",
    "ship-condition": "no repairs needed",
    "new-customer": "no",
    "id": id}
    for x in range(len(value)):
        if key[x] in acceptableKeys:
            c[key[x]] = value[x]
        if c["new-customer"] == "on":
            c["new-customer"] = "yes"
    c["name"] = c["name"].replace("+"," ")
    c["ship-condition"] = c["ship-condition"].replace("+"," ")
    contacts.append(c)
    return


# The method signature is a bit "hairy", but don't stress it -- just check the documentation below.
def server(method: str, url: str, body: Optional[str], headers: dict[str, str]) -> tuple[Union[str, bytes], int, dict[str, str]]:    
    """
    method will be the HTTP method used, for our server that's GET, POST, DELETE
    url is the partial url, just like seen in previous assignments
    body will either be the python special None (if the body wouldn't be sent)
         or the body will be a string-parsed version of what data was sent.
    headers will be a python dictionary containing all sent headers.

    This function returns 3 things:
    The response body (a string containing text, or binary data)
    The response code (200 = ok, 404=not found, etc.)
    A _dictionary_ of headers. This should always contain Content-Type as seen in the example below.
    """
    # Parse URL -- this is probably the best way to do it. Delete if you want.
    url, *parameters = url.split("?", 1)

    # And another freebie -- the 404 page will probably look like this.
    # Notice how we have to be explicit that "text/html" should be the value for
    # header: "Content-Type" now?]
    # I am sorry that you're going to have to do a bunch of boring refactoring.
    if(method == "GET"):
        if(url == "/main.dark.css"):
            return open("static/css/main.dark.css","rb").read(),200,{"Content-Type": "text/css"}
        elif(url == "/main.css"):
            return open("static/css/main.css", "rb").read(),200,{"Content-Type": "text/css"}
        elif(url == "/main"):
            return  open("static/html/mainpage.html").read(),200, {"Content-Type": "text/html; charset=utf-8"}
        elif(url == "/"):
            return  open("static/html/mainpage.html").read(),200, {"Content-Type": "text/html; charset=utf-8"}
        elif(url == "/contact"):
                return open("static/html/contactform.html").read(),200, {"Content-Type": "text/html; charset=utf-8"}
        elif(url == "/testimonies"):
            return open("static/html/testimonies.html").read(), 200, {"Content-Type": "text/html; charset=utf-8"}
        elif(url == "/admin/contactlog"):
            login(method,url, body, headers)
            return showContactLog()
        elif(url == "/images/main"):
            return open("static/images/pirate.jpeg", "rb").read(),200, {"Content-Type": "image/jpeg; charset=utf-8"}
        elif(url == "/js/main.js"):
            return open("static/js/main.js","rb").read(),200, {"Content-Type": "text/javascript; charset=utf-8"}
        elif(url == "/js/contact.js"):
            return open("static/js/contact.js","rb").read(),200, {"Content-Type": "text/javascript; charset=utf-8"}
        elif(url == "/js/table.js"):
            return open("static/js/table.js","rb").read() ,200, {"Content-Type": "text/javascript; charset=utf-8"}
        elif(url == "/api/sale"):
            global sale_active
            if (sale_active):
                return '{"active": true, "message": '+sale_message+'}',200,{"Content-Type":"application/json"}
            return '{"active": false}',200, {"Content-Type": "application/json"}
        else:
            return open("static/html/404.html").read(), 404, {"Content-Type": "text/html; charset=utf-8"}
    elif(method == "POST"):
        #TODO: add post method
        if(url == "/contact"):

            if(body == None):
                return open("static/html/404.html").read(), 404, {"Content-Type": "text/html; charset=utf-8"}
            if("name=" in body and "email=" in body and "date=" in body): #("name=" and "email=" in info)
                info = urllib.parse.unquote(body, encoding='utf-8', errors='replace')
                temp = info.split("&")
                #ex temp = [name=nathan,email=zigmu004@umn.edu,date=2002-02-02,ship-condition=No+repairs+needed,new-customer=on,submit=Submit]
                
                temp = info.split("&")

                key = []
                value = []
                for p in temp:
                    key += [p[:p.find("=")]]
                    value += [p[p.find("=")+1:]]
                #ex value = [nathan,zigmu004%40umn.edu,2002-02-02,no+repairs+needed, on, submit]
                updateContacts(key, value)
                return open("static/html/contactsuccess.html").read(),201, {"Content-Type": "text/html; charset=utf-8"}
            else:
                return open("static/html/contactfail.html").read(), 400,{"Content-Type": "text/html; charset=utf-8"}
        elif(url == "/api/sale"):
            login(method,url, body, headers) 
            if(body == None):
                return 'no body',400,{"Content-Type":"text/plain"}
            elif("Content-Type" in headers and headers["Content-Type"] !="application/json"):
                return "send me a json",400,{"Content-Type": "text/plain"}
            else:
                b = json.loads(body)
                msg = b["message"]
                return '{"message": '+msg+'}',201,{"Content-Type":"application/json"}
        else:
            return open("static/html/404.html").read(), 404, {"Content-Type": "text/html; charset=utf-8"}
    #TODO add delete
    elif(method == "DELETE"):
        if(url == "/api/contact"):
            login(method,url, body, headers)
            if("Content-Type" in headers):
                if(headers["Content-Type"] =="application/json"):
                    #has content type header and its json, extract ID
                    b = json.loads(body)
                    str_id = b["id"]
                    id = int(str_id)
                    #parse through contacts, find the right id
                    for x in range(len(contacts)):
                        if(contacts[x]["id"] == id):
                            #matches, delete row
                            contacts.pop(x)
                            return showContactLog()
                        
                    return
                else:
                    return "Not the proper format", 400, {"Content-Type": "text/html; charset=utf-8"}
            else:
                return "Must include Content-Type header", 400, {"Content-Type": "text/html; charset=utf-8"}
        elif(url == "/api/sale"):
            login(method,url, body, headers)
            
            if(sale_active):
                sale_active = False
            else:
                sale_active = True

            if (sale_active):
                return '{"active": true, "message": '+sale_message+'}',200,{"Content-Type":"application/json"}
            return '{"active": false, "message": '+sale_message+'}',200, {"Content-Type": "application/json"}
        else:
            return open("static/html/404.html").read(),404,{"Content-Type": "text/html; charset=utf-8"}
    else:
        return open("static/html/404.html").read(),404,{"Content-Type": "text/html"}




# You shouldn't need to change content below this. It would be best if you just left it alone.


class RequestHandler(BaseHTTPRequestHandler):
    def c_read_body(self):
        # Read the content-length header sent by the BROWSER
        content_length = int(self.headers.get("Content-Length", 0))
        # read the data being uploaded by the BROWSER
        body = self.rfile.read(content_length)
        # we're making some assumptions here -- but decode to a string.
        body = str(body, encoding="utf-8")
        return body

    def c_send_response(self, message, response_code, headers):
        # Convert the return value into a byte string for network transmission
        if type(message) == str:
            message = bytes(message, "utf8")
        
        # Send the first line of response.
        self.protocol_version = "HTTP/1.1"
        self.send_response(response_code)
        
        # Send headers (plus a few we'll handle for you)
        for key, value in headers.items():
            self.send_header(key, value)
        self.send_header("Content-Length", len(message))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        # Send the file.
        self.wfile.write(message)
        

    def do_POST(self):
        # Step 1: read the last bit of the request
        try:
            body = self.c_read_body()
        except Exception as error:
            # Can't read it -- that's the client's fault 400
            self.c_send_response("Couldn't read body as text", 400, {'Content-Type':"text/plain"})
            raise
                
        try:
            # Step 2: handle it.
            message, response_code, headers = server("POST", self.path, body, self.headers)
            # Step 3: send the response
            self.c_send_response(message, response_code, headers)
        except Exception as error:
            # If your code crashes -- that's our fault 500
            self.c_send_response("The server function crashed.", 500, {'Content-Type':"text/plain"})
            raise
        

    def do_GET(self):
        try:
            # Step 1: handle it.
            message, response_code, headers = server("GET", self.path, None, self.headers)
            # Step 3: send the response
            self.c_send_response(message, response_code, headers)
        except Exception as error:
            # If your code crashes -- that's our fault 500
            self.c_send_response("The server function crashed.", 500, {'Content-Type':"text/plain"})
            raise


    def do_DELETE(self):
        # Step 1: read the last bit of the request
        try:
            body = self.c_read_body()
        except Exception as error:
            # Can't read it -- that's the client's fault 400
            self.c_send_response("Couldn't read body as text", 400, {'Content-Type':"text/plain"})
            raise
        
        try:
            # Step 2: handle it.
            message, response_code, headers = server("DELETE", self.path, body, self.headers)
            # Step 3: send the response
            self.c_send_response(message, response_code, headers)
        except Exception as error:
            # If your code crashes -- that's our fault 500
            self.c_send_response("The server function crashed.", 500, {'Content-Type':"text/plain"})
            raise



def run():
    PORT = 4131
    print(f"Starting server http://localhost:{PORT}/")
    server = ("", PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()


run()
