#!ruby
require 'rake'
require 'json'
require 'colorize'

@db = File.expand_path '~/task.txt'
@stop = File.expand_path '~/stop.txt'

def load_task
  File.readlines(@db).map { |t| JSON.parse(t.chomp, :symbolize_names => true) }
end
def save_task tasks
  File.open(@db, 'w') do |io|
    io.write(tasks.map{|t| JSON.generate(t)}.join("\n"))
  end
end

FORMAT = "%-10s%-10s%-30s%-30s".cyan
HEADER = FORMAT % %w(ID Status Directory Command)


dir = Dir.pwd
action = ARGV.shift || 'list'
argv = ARGV.join ' '
id = ARGV.shift.to_i || 0
touch @db unless File.exists? @db
tasks = load_task
case action
when 'add'
  tasks << {:status => 'new', :pwd => dir, :cmd => argv}
when 'reset'
  tasks[id][:status] = 'new'
when 'del', 'delete'
  tasks.delete_at id
when 'clean'
  tasks.delete_if { |t| t[:status] == 'done' }
when 'stop'
  touch @stop
when 'go'
  rm @stop if File.exists? @stop
when 'start', 'run'
  catch :done do
    task = {}
    trap("SIGINT") { throw :ctrl_c }
    catch :ctrl_c do
      while !File.exists? @stop
        task = tasks.find { |t| t[:status] == 'new' }
        break if task.nil?
        task[:status] = 'wip'
        save_task tasks
        # Execute the task
        puts HEADER
        puts FORMAT % ['-', task[:status], task[:pwd], task[:cmd]]
        pwd = dir
        begin
          Dir.chdir task[:pwd]
          sh task[:cmd]
          Dir.chdir pwd
          tasks = load_task # reload
          task = tasks.find { |t| t[:pwd] == task[:pwd] && t[:cmd] == task[:cmd] }
          task[:status] = 'done'
        rescue Exception
          tasks = load_task # reload
          task = tasks.find { |t| t[:pwd] == task[:pwd] && t[:cmd] == task[:cmd] }
          task[:status] = 'error'
        end
        save_task tasks
      end
      rm @stop if File.exists? @stop
      throw :done
    end
    tasks = load_task # reload
    task = tasks.find { |t| t[:pwd] == task[:pwd] && t[:cmd] == task[:cmd] }
    task[:status] = 'abort'
  end
end
puts HEADER
tasks.each_with_index do |t, i|
  puts FORMAT % [i, t[:status], t[:pwd], t[:cmd]]
end

save_task tasks if action != 'list'
