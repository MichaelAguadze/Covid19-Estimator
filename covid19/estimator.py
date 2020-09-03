from xml.etree.ElementTree import Element, tostring

class covid19assessment:
    
    def __init__(self, currently_infected, days):
        self.days = days
        self.currently_infected = currently_infected
        self.infections_by_requested_time = int(self.currently_infected*(2**(self.days//3)))
        

    def severe_cases_by_requested_time(self):
        self.severe_cases_by_requested_time = int(self.infections_by_requested_time*0.15)
        return self.severe_cases_by_requested_time

    def hospital_beds_by_requested_time(self, total_hospital_beds):
        percentage = 65
        self.available_hospital_beds = int(total_hospital_beds*((100-percentage)/100))
        return self.available_hospital_beds
    
    def cases_for_icu__by_requested_time(self):
        self.cases_for_icu_by_requested_time = int(self.infections_by_requested_time*0.05)
        return self.cases_for_icu_by_requested_time
    
    def cases_for_ventilators_by_requested_time(self):
        self.cases_for_ventilators_by_requested_time = int(self.infections_by_requested_time*0.02)
        return self.cases_for_ventilators_by_requested_time
    
    def dollars_in_flight(self, avg_daily_income_population, avg_daily_income_in_usd):
        self.dollars_in_flight = self.infections_by_requested_time*avg_daily_income_population*avg_daily_income_in_usd*self.days
        return self.dollars_in_flight

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




     
