config.action_mailer.delivery_method = :smtp
  config.action_mailer.smtp_settings = {
    address: 'smtp.gmail.com',
    port: 587,
    user_name: 'demas',
    password: 'pass',
    authentication: 'plain',
    enable_starttls_auto: true 
  }   
