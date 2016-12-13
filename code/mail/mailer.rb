# Setup ActionMailer to work with SendGrid on Heroku Cedar Stack
## Add sendgrid keys heroku config environment
##	heroku config:add SENDGRID_USERNAME=<YOUR_KEY>
ActionMailer::Base.smtp_settings = {
  :address        => 'smtp.sendgrid.net',
  :port           => '587',
  :authentication => :plain,
  :user_name      => ENV['SENDGRID_USERNAME'],
  :password       => ENV['SENDGRID_PASSWORD'],
  :domain         => 'pickgrapevine.com'
}
ActionMailer::Base.delivery_method = :smtp
