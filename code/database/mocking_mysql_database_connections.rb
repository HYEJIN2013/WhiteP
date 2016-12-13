#!/usr/bin/env rspec

require 'mocha'
require 'mysql'

describe "foo" do
  it "should mock mysql query" do
    mock_mysql = mock("Mysql")
    Mysql.expects(:new).returns(mock_mysql)
    mock_mysql.expects(:query).with("create database foo")

    db = Mysql.new("localhost", "root", "this is not the password")
    db.query("create database foo")
  end
end
