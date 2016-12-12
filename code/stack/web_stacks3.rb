require 'rack'
 
app = Proc.new do |env|
    ['200', {'Content-Type' => 'text/html'}, ['A barebones rack app.']]
end

class Middleware
  def initialize(app)
    @app = app       
  end                

  def call(env)
    # transform request
    new_env = cond? ? transform(env) : env
    # intercept
    return [status, headers, res] if cond?
    
    # transform responce 
    status, headers, response = @app.call(new_env)
    new_responce cond? ? transform(response) : response
    [status, headers, new_response]   
  end                
end              

use Middleware
Rack::Handler::WEBrick.run app
