class LogConnection < ActiveRecord::Base
  self.abstract_class = true
  establish_connection "other_#{Rails.env}"
  # connection data is loaded from database.yml
end

class Logs < LogConnection
  # Logs.create connects to LogConnection
end
