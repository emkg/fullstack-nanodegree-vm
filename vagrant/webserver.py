from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

# import CRUD operations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

# make sure we can access the database
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# handler class
class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/restaurants'):
                restaurants = session.query(Restaurant).all()

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                output += "<a href='/restaurants/new'>Add</a>"
                output += "<br/><br/>"

                for r in restaurants:
                    output += "%s" % r.name
                    output += "<br/><a href='/restaurants/%s" % r.id
                    output += "/edit'>Edit</a>"
                    output += "<br/>"
                    output += "<a href='/restaurants/%s" % r.id
                    output += "/are-you-sure'>Delete</a><br/> <br/><br/>"

                output += "</body></html>"

                self.wfile.write(output)
                print output
                return

            if self.path.endswith('/restaurants/new'):
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()

                output = "<html><body>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<h2> What is the name of the restaurant? </h2>"
                output += "<input name='restaurant' type ='text'> <input type='submit' value='Submit'>"
                output += "</form></body></html>"

                self.wfile.write(output)
                print output
                return

            if self.path.endswith('/edit'):
                restaurantIDPath = self.path.split('/')[2];
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('content-type', 'text/html')
                    self.end_headers()

                    output = "<html><body>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurantIDPath
                    output += "<h2> What is the new name of the restaurant? </h2>"
                    output += "<input name='restaurant' type ='text' placeholder='%s'> <input type='submit' value='Submit'>" % myRestaurantQuery.name
                    output += "</form></body></html>"

                    self.wfile.write(output)
                    print output
                    return

            if self.path.endswith('/are-you-sure'):
                restaurantIDPath = self.path.split('/')[2];
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()

                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('content-type', 'text/html')
                    self.end_headers()

                    output = "<html><body>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/are-you-sure'>" % restaurantIDPath
                    output += "<h2> Are you sure you want to delete %s </h2>" % myRestaurantQuery.name
                    output += "<input type='submit' value='Yes'>"
                    output += "</form></body></html>"

                    self.wfile.write(output)
                    print output
                    return


        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith('/restaurants/new'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messageContent = fields.get('restaurant')

                    # create new Restaurant class
                    restaurant = Restaurant(name=messageContent[0])
                    session.add(restaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

                    return
            if self.path.endswith('/edit'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messageContent = fields.get('restaurant')
                    restaurantIDPath = self.path.split('/')[2];
                    myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()

                    myRestaurantQuery.name = messageContent[0]

                    session.add(myRestaurantQuery)
                    session.commit()

                    self.send_response(301)
                    self.send_header('content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

                    return
            if self.path.endswith('/are-you-sure'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messageContent = fields.get('restaurant')
                    restaurantIDPath = self.path.split('/')[2];
                    myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                    session.delete(myRestaurantQuery)
                    session.commit()

                    self.send_response(301)
                    self.send_header('content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

                    return

        except:
            pass

# main method where we will instantiate the handler
def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping web server"
        server.socket.close()

if __name__ == '__main__':
    main()
