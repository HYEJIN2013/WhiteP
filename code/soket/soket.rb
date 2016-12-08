require 'socket'

class Client
  def initialize(ip='127.0.0.1',port=3333)
    @ip, @port = ip, port
  end

  def send_message(msg)
    connection do |socket|
      socket.puts(msg)
      socket.gets
    end
  end

  def receive_message
    connection do |socket|
      soket.gets
    end
  end

  private

  def connection
    socket = TCPSocket.new(@ip,@port)
    yield(socket)
  ensure
    socket.close
  end
end
