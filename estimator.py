import time
from flask import Flask, Response, request, jsonify, g, redirect, render_template
from xml.etree.ElementTree import Element, tostring
from covid19 import covid19assessment

app = Flask(__name__)

def estimator(data):
    """
    This function computes the estimation for impact and severeImpact
    """
    
    reported_cases = data["reportedCases"]
    total_hospital_beds = data["totalHospitalBeds"]
    avg_daily_income_in_usd = data["region"]["avgDailyIncomeInUSD"]
    avg_daily_income_population = data["region"]["avgDailyIncomePopulation"]
    if data["periodType"] == "weeks":
       days = data["timeToElapse"] * 4
    elif data["periodType"] == "month":
      days = data["timeToElapse"] * 30
    else:
        days = data["timeToElapse"]

    
    impact_currently_infected = reported_cases*10
    severe_currently_infected = reported_cases*50
    

    impact = {}
    severeImpact = {}
    result = {}
    
    estimate = covid19assessment(impact_currently_infected, days)
    impact["currentlyInfected"] = impact_currently_infected
    impact["severeCasesByRequestedTime"] = estimate.severe_cases_by_requested_time()
    impact["totalHospitalBeds"] = estimate.hospital_beds_by_requested_time(total_hospital_beds)
    impact["casesForICUByRequestedTime"] = estimate.cases_for_icu__by_requested_time()
    impact["casesForVentilatorsByRequestedTime"] = estimate.cases_for_ventilators_by_requested_time()
    impact["dollarsInFlight"] = estimate.dollars_in_flight(avg_daily_income_population, avg_daily_income_in_usd)

    severe_estimate = covid19assessment(severe_currently_infected, days)
    severeImpact["currentlyInfected"] = severe_currently_infected
    severeImpact["severeCasesByRequestedTime"] = severe_estimate.severe_cases_by_requested_time()
    severeImpact["totalHospitalBeds"] = severe_estimate.hospital_beds_by_requested_time(total_hospital_beds)
    severeImpact["casesForICUByRequestedTime"] = severe_estimate.cases_for_icu__by_requested_time()
    severeImpact["casesForVentilatorsByRequestedTime"] = severe_estimate.cases_for_ventilators_by_requested_time()
    severeImpact["dollarsInFlight"] = severe_estimate.dollars_in_flight(avg_daily_income_population, avg_daily_income_in_usd)

    result["data"] = data
    result["impact"] = impact
    result["severImpact"] = severeImpact
    return result

    
def dict_to_xml(tag, d):
    """
    Turn a simple dict of key/value pairs into XML
    """
    elem = Element(tag)
    for key, val in d.items():
        child = Element(key)
        child.text = str(val)
        elem.append(child)
    return elem

@app.before_request
def before_request():
    g.start_time = time.time()
    g.logs = open("log_book.txt", "a+")

@app.route('/')
def index():
  return "Welcome"
    
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


     
