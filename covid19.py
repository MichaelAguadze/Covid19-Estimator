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
