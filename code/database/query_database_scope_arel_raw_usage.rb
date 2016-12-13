#distinct value
WeatherLog.select(:datetime, :weather_station).uniq.count

# where clause
WeatherLog.where(:wban=> "99999").where(:weather_station => "076500")
