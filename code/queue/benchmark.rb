require 'spec/spec_helper'
require 'logger'
require 'benchmark'

# Delayed::Worker.logger = Logger.new('/dev/null')

Benchmark.bm(10) do |x|
  Delayed::Job.delete_all
  n = 3000*3
  n.times { "foo".delay.length }

  x.report { Delayed::Worker.new(:quiet => true).work_off(n) }
end

# Working off just one queue
Benchmark.bm(10) do |x|
  Delayed::Job.delete_all
  n = 3000
  n.times { "foo".delay(:queue => 'one').length }
  n.times { "foo".delay(:queue => 'two').length }
  n.times { "foo".delay(:queue => 'three').length }

  x.report { Delayed::Worker.new(:queues => %w( one ), :quiet => true).work_off(n) }

  puts "Left jobs on queue one: #{Delayed::Job.where(:queue => 'one').count}"
  puts "Left jobs on queue two: #{Delayed::Job.where(:queue => 'two').count}"
  puts "Left jobs on queue three: #{Delayed::Job.where(:queue => 'three').count}"
end

# Working off two queues
Benchmark.bm(10) do |x|
  Delayed::Job.delete_all
  n = 3000
  n.times { "foo".delay(:queue => 'one').length }
  n.times { "foo".delay(:queue => 'two').length }
  n.times { "foo".delay(:queue => 'three').length }

  x.report { Delayed::Worker.new(:queues => %w( one two ), :quiet => true).work_off(n*2) }

  puts "Left jobs on queue one: #{Delayed::Job.where(:queue => 'one').count}"
  puts "Left jobs on queue two: #{Delayed::Job.where(:queue => 'two').count}"
  puts "Left jobs on queue three: #{Delayed::Job.where(:queue => 'three').count}"
end

# Working off all queues
Benchmark.bm(10) do |x|
 Delayed::Job.delete_all
 n = 3000
 n.times { "foo".delay(:queue => 'one').length }
 n.times { "foo".delay(:queue => 'two').length }
 n.times { "foo".delay(:queue => 'three').length }

 x.report { Delayed::Worker.new(:quiet => true).work_off(n*4) }

 puts "Left jobs on queue one: #{Delayed::Job.where(:queue => 'one').count}"
 puts "Left jobs on queue two: #{Delayed::Job.where(:queue => 'two').count}"
 puts "Left jobs on queue three: #{Delayed::Job.where(:queue => 'three').count}"
end
