#app/controllers/notifications_mailer.rb

class NotificationsMailer < ActionMailer::Base

  default :from => "noreply@squape.com"
  default :to => "contacto@squape.com"

  def new_message(message)
    @message = message
    mail(:subject => "[SQUAPE.com] #{message.subject}")
  end

end
