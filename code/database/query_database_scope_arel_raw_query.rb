targets = Transfer.where("user_id not NULL")
          .where("amount > ? AND amount < ? AND service_type = ?",3000, 9000,"代買")
          .order("updated_at DESC")

# reset sqlite database          
Transfer.destroy_all
ActiveRecord::Base.connection.execute("DELETE from sqlite_sequence where name = 'transfers'")

# time interval

Chekin.where(created_at: Time.parse("12pm")..Time.parse("4:30pm"))

start_time = Date.parse(params["start_time"])
end_time = Date.parse(params["end_time"]) + 1.day
if params.has_key?"start_time" and params.has_key? "end_time"
@weather_logs = WeatherLog.all.order(datetime: :asc)
.where('datetime BETWEEN ? AND ?', start_time, end_time)
elsif params.has_key? "start_time"
elsif params.has_key? "end_time"
end
