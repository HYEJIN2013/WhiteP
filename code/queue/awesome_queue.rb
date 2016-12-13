class GuitarStore::AwesomeQueue

  def initialize
    @queue = []
  end

  def push(job)
    write_to_file(job)
  end

  def pop
    if job = read_from_file
      clear_file
      job
    else
      Struct.new(:run).new(true)
    end
  end
  
  private

    JOBS_FILE = '.jobs'

    def write_to_file(job)
      File.open(JOBS_FILE,'w') do |file|
        Marshal.dump(job, file)
      end        
    end

    def read_from_file
      begin
        File.open(JOBS_FILE, 'r') do |file|
          Marshal.load(file)
        end
      rescue EOFError
      end
    end

    def clear_file
      File.truncate(JOBS_FILE, 0)
    end
end
