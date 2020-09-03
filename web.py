import time
from flask import Flask, Response, request, jsonify, g, redirect, render_template
from estimator import *

app = Flask(__name__)

@app.route('/')
def index():
  return "Welcome"

@app.before_request
def before_request():
    g.start_time = time.time()
    g.logs = open("log_book.txt", "a+")

    
@app.route("/api/v1/on-covid-19/xml", methods = ["POST", "GET"])
def xml_request():
    """
    This function responds to request seeking XML format
    """
    
    req_data = request.get_json()
    result = estimator(req_data)
    data = tostring(dict_to_xml('estimate', result))
    g.log_info = "  /api/v1/on-covid-19/xml   "
    return Response(response = data, status = 200, mimetype="application/xml") 


@app.route("/api/v1/on-covid-19", methods=["POST", "GET"] )
@app.route("/api/v1/on-covid-19/json", methods=["POST", "GET"])
def json_request():
    """
    This function responds to request seeking JSON format
    """
    req_data = request.get_json()
    result = estimator(req_data)
    if request.path == "/api/v1/on-covid-19": 
        g.log_info = "  /api/v1/on-covid-19  "
    else:
        g.log_info = "  /api/v1/on-covid-19/json  "
    return jsonify(result)

@app.route("/api/v1/on-covid-19/logs", methods=["GET"])
def check_logs():
    g.logs = open("log_book.txt", "r")
    text_data = [lines for lines in g.logs]
    return render_template("index.html", content=text_data)
    

@app.after_request
def after_request(response):
    end_time = int((time.time() - g.start_time)*1000) 
    if request.path != "/api/v1/on-covid-19/logs":
        g.logs.write(request.method + g.log_info + str(end_time) + "ms" + "    " + str(response.status_code) + "\n" )
    g.logs.close()
    return response

if __name__ == "__main__":
    app.debug = True
    app.run()