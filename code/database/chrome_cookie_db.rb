require 'rubygems'
require 'sqlite3'

class ChromeCookiesDatabase
  COOKIES_LOCATION = "~/Library/Application\ Support/Google/Chrome/Profile\ 2/Cookies"
  
  def new(path=nil)
    @db = SQLite3::Database.new((path or COOKIES_LOCATION))
  end
  
  def clear_cookies_host_key(host_key)
    @db.execute2('delete from cookies where host_key = ?', host_key) 
    @db.commit
  end
  
  def insert_cookies(host_key, cookies)
    now = Time.now.utc.tv_sec
    @db.transaction
    cookies.each_pair do |name, value|
      @db.execute2("INSERT INTO cookies VALUES(?,?,?,?,?,?,?,?,?)", now, host_key, name, value, '/', now+3600, 0, 0, now)
    end
    @db.commit
  end
  
  def print_cookies_host_key(host_key)
    columns = nil
    @db.execute2('select * from cookies order by host_key, name') do |row|
      if not columns
        columns = row
      else
        creation_utc, host_key, name, value, path, expires_utc, secure, httponly, last_access_utc = row
        puts "#{host_key}: #{name} => #{value}"
      end
    end
  end
end
