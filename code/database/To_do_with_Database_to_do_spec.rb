require 'rspec'
require 'to_do'
require 'pg'

DB = PG.connect(:dbname => 'to_do_test')

RSpec.configure do |config|
  config.after(:each) do
    DB.exec("DELETE FROM tasks *;")
  end
end    

describe Task do
  it 'is initialized with a name and list id' do
    task = Task.new('learn sql', 1)
    task.should be_an_instance_of Task
  end

  it 'tells you its list id' do
    task = Task.new('learn sql', 1)
    task.list_id.should eq 1
  end

  it 'starts off with no tasks' do
    Task.all.should eq []
  end

  it 'lets you save tasks to the database' do 
    task = Task.new('learn SQL', 1 )
    task.save
    Task.all.should eq [task]
  end  

  it 'is the same task if it has the same name and list id' do
    task1 = Task.new('learn SQL', 1)
    task2 = Task.new('learn SQL', 1)
    task1.should eq task2
  end
end    
