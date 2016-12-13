require "mail"

class TrialMailer
  def self.execute(params)
    #initialize email settings  
    set_mail_defaults
    #get params
    recordId = params['record_uuid']
    status= params['statusName']
    #get the trial user
    trial_user = Dm::Dev::TrialUser.get(recordId)
    #Get the trial
    trial = trial_user.dev_trial.id
    #Get all the communications that are related to this trial and that have the status name as the current user status
    communications = Dm::Dev::TrialCommunication.all(:dev_trial => trial_user.dev_trial, :dev_status_name => status)
    #Iterate the communications
    communications.each do |communication|
      #Get the email body. As this is a code field, it is represented as an array so we are looking for the value in position 1
      body = communication.dev_email_body[1]
      #substitute each key with the appropiate value
      body = body.gsub(/{io_uuid}/,trial_user.id) 
      body = body.gsub(/{dev_name}/,trial_user.dev_name) unless trial_user.dev_name.nil?
      body = body.gsub(/{dev_username}/,trial_user.dev_username) unless trial_user.dev_username.nil?
      body = body.gsub(/{dev_password}/,trial_user.dev_password)unless trial_user.dev_password.nil?
      body = body.gsub(/{dev_requested_date}/,trial_user.dev_requested_date.to_s) unless trial_user.dev_requested_date.nil?
      body = body.gsub(/{dev_email}/,trial_user.dev_email) unless trial_user.dev_email.nil?
      body = body.gsub(/{dev_expiration_date}/,trial_user.dev_expiration_date.to_s) unless trial_user.dev_expiration_date.nil?
      body = body.gsub(/{dev_sales_group}/,trial_user.dev_sales_group.dev_name) unless trial_user.dev_sales_group.nil?
      body = body.gsub(/{dev_last_name}/,trial_user.dev_last_name) unless trial_user.dev_last_name.nil?
      body = body.gsub(/{dev_first_name}/,trial_user.dev_first_name) unless trial_user.dev_first_name.nil?
      body = body.gsub(/{dev_instance}/,trial_user.dev_instance) unless trial_user.dev_instance.nil?
      body = body.gsub(/{dev_organization}/,trial_user.dev_organization) unless trial_user.dev_organization.nil?
      body = body.gsub(/{dev_country}/,trial_user.dev_country.io_name) unless trial_user.dev_country.nil?
      #Lets assume this email go to the user
      to= trial_user.dev_email
      #Lets set the cc value, if that is defined in the trial
      cc = trial.dev_cc_email.nil? ? '' : trial.dev_cc_email
      #Check if communication is set to be internal internal
      if !communication.dev_internal.nil? and communication.dev_internal == true
        # Yes it is internal. clear the cc and set the To field to all users in the group  
        to = trial.dev_notify_group.io_users.related_records.map{|u| u.io_email}
        cc = ''
      end
      #Send the email!
      send_mail({"mail_to" => to,"mail_cc" => cc, "mail_from" => communication.dev_from,"mail_subject" => communication.dev_subject,"mail_body" => { "html_part" => body}})
    end
  end
  def self.send_mail(mail_message)
    mail = Mail.new({
      :to => mail_message["mail_to"],
      :from => mail_message["mail_from"],
      :subject => mail_message["mail_subject"]
    })
    cc = mail_message["mail_cc"]
    mail.cc = cc if !cc.nil? and !cc.empty?
    mail_body = mail_message["mail_body"]
    text_part = mail_body["text_part"].to_s if !mail_body.nil?
    if text_part != "" && !text_part.nil?
      mail.text_part = Mail::Part.new do
        body text_part
      end
    end
    html_part = mail_body["html_part"].to_s if !mail_body.nil?
    if html_part != "" && !html_part.nil?
      mail.html_part = Mail::Part.new do
        content_type 'text/html; charset=UTF-8'
        body html_part
      end
    end
    # deliver the mail
    mail.deliver
  end

  # Sets the Mail default settings for delivering emails
  # Settings are retrieved from the System Settings object.
  def self.set_mail_defaults
    smtp_host = Io::Intalio.get_system_setting("io_outgoing_mail_server_hostname")
    smtp_port = Io::Intalio.get_system_setting("io_outgoing_mail_server_port")
    smtp_helo_domain = Io::Intalio.get_system_setting("io_outgoing_mail_server_domain")
    smtp_password = Io::Intalio.get_system_setting("io_outgoing_mail_server_password")
    smtp_user_name = Io::Intalio.get_system_setting("io_outgoing_mail_server_username")
    smtp_encryption_enabled = Io::Intalio.get_system_setting("io_outgoing_mail_server_encryption")
    smtp_tls_enabled = (smtp_port.to_s == "587") ? false : true
    Mail.defaults do
      delivery_method :smtp, {
        :address => smtp_host, 
        :port => smtp_port,
        :domain => smtp_helo_domain,
        :user_name => smtp_user_name,
        :password => smtp_password[0],
        :authentication => 'login',
        :enable_tls => smtp_encryption_enabled,
        :tls => smtp_tls_enabled,
        :openssl_verify_mode => "NONE"
      }
    end
  end

end
