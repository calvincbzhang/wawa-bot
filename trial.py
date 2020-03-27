import requests

def wawa_info_message(confirmed, deaths, recov, total_conf, country):
    wawa_info_builder = " Today in {}, we recorded {} new confirmed cases, we have the pleasure of announcing that {} recovered, welcome back to them! We mourn the passing of {} people. There are now {} cases.".format(country, confirmed, recov, deaths, total_conf)
    
    return wawa_info_builder

def test_covid_api():
  """
    Simple test
  """
  response = requests.get("https://api.covid19api.com/summary")

  #Ensure connection with API
  if (response.status_code != 200):
    return "Failed to connect with API"
  
  response_json = response.json()
  count = 0

  while(True):
    if response_json['Countries'][count]['Country'] == 'Belgium':
      new_confirmed = response_json['Countries'][count]['NewConfirmed']
      new_deaths =  response_json['Countries'][count]['TotalDeaths']
      new_recovered = response_json['Countries'][count]['NewRecovered']
      total_confirmed = response_json['Countries'][count]['TotalConfirmed']
      return wawa_info_message(new_confirmed, new_deaths, new_recovered, total_confirmed, "Belgium")
    count += 1

if __name__ == "__main__":
    print(test_covid_api())
