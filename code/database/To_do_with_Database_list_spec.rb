require 'rspec'
require 'list'
require 'pg'

DB = PG.connect(:dbname => 'to_do_test')

RSpec.configure do |config|
  config.after(:each) do
    DB.exec("DELETE FROM lists *;")
  end
end    

describe List do
  it 'is initialized with a name' do 
    list = List.new('Epicodus stuff')
    list.should be_an_instance_of List
  end

  it "tells you it's name" do
    list = List.new('Epicodus stuff')
    list.name.should eq 'Epicodus stuff'
  end  

  it 'is the same list if it has the same name' do
    list1 = List.new('Epicodus')
    list2 = List.new('Epicodus')
    list1.should eq list2
  end  

  it 'starts off with no lists' do
    List.all.should eq []
  end
  
  it 'lets you save lists to the database' do
    list1 = List.new("Epicodus stuff")
    list1.save
    List.all.should eq [list1]
  end  

  it 'sets its ID when you save it' do
    list = List.new('Epicodus')
    list.save
    list.id.should be_an_instance_of Fixnum
  end  
end  
