#config/application.rb

module RailsApp
  class Application < Rails::Application

    config.action_mailer.smtp_settings = {
      :address              => "smtp.live.com",
      :port                 => 587,
      :domain               => "squape.com",
      :user_name            => "noreply@squape.com",
      :password             => "squapeco",
      :authentication       => :plain,
      :enable_starttls_auto => true
    }

    config.action_mailer.default_url_options = {
      :host => "squape.com"
    }

  end
end
