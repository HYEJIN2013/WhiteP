# General Settings
  config.app_domain = 'youtee.io'

  config.action_mailer.default_url_options = { host: config.app_domain }
  config.action_mailer.perform_deliveries = true
  config.action_mailer.delivery_method = :smtp
  config.action_mailer.smtp_settings = {
    :address              => "smtp.chrisrjones.com",
    :port                 => 587,
    :domain               => 'youtee.io',
    :user_name            => ENV['MAIL_ADDRESS'],
    :password             => ENV['MAIL_PASSWORD'],
    :authentication       => 'plain',
    :enable_starttls_auto => true,
    openssl_verify_mode: 'none'
  }
