# This file can be placed in the /lib folder
# 
# Class will over write the subject and receivers information,
# register this interceptor in each environment you don't want
# to send emails to your customers
#
class MailInterceptor
  def self.delivering_email(message)
    message.subject = "#{message.to} #{message.subject}"
    message.to = "info@example.com"
  end
end
