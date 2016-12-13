require 'pg'


class Task
  def initialize(name, list_id)
    @name = name
    @list_id = list_id
  end

  def name
    @name
  end

  def list_id
    @list_id
  end
  
  def self.all
    # database = PG.connect(:dbname => 'to_do')
    results = DB.exec("SELECT *FROM tasks;")
    tasks = []
    results.each do |result|
      name = result['name']
      list_id = result['list_id'].to_i
      tasks << Task.new(name, list_id)
    end
    tasks  
  end  

  def save
    # database = PG.connect(:dbname => 'to_do')
    DB.exec("INSERT INTO tasks (name, list_id) VALUES ('#{@name}', #{@list_id});")  
  end 

  def ==(another_task)
    self.name == another_task.name  && self.list_id == another_task.list_id
  end 
end   
