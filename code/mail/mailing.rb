
# config/environments/development.rb


  config.action_mailer.raise_delivery_errors = true
  config.action_mailer.delivery_method = :smtp
  config.action_mailer.smtp_settings = {
    :address              => "smtp.gmail.com",
    :port                 => 587,
    :domain               => 'baci.lindsaar.net',
    :user_name            => 'rafaelb.site',
    :password             => 'samplepass',
    :authentication       => 'plain',
    :enable_starttls_auto => true  }


# apps/mailers/email_mailer.rb


class EmailMailer < ActionMailer::Base

  default :to => "rafaelb.site@gmail.com"

  def send_email(email)
    @email = email
    #@url  = "http://example.com/login"
    mail(
      :from => email.address,
      :subject => "[RafaelB.net] #{email.subject}"
    )
  end

end


# apps/views/email_mailer/send_email.html.erb


Name: <%= @email.name %>
<hr/>
Email: <%= @email.address %>
<hr/>
Subject: <%= @email.subject %>
<hr/>
<%= @email.message %>
# apps/controllers/emails_controller.rb
  def create
    @email = Email.new(params[:email])
    respond_to do |format|
      if @email.save 
        EmailMailer.send_email( @email ).deliver
        format.html { redirect_to(@email, :notice => 'Email was successfully created.') }
        format.xml  { render :xml => @email, :status => :created, :location => @email }
      else
        if @email.invalid_security
          @email.security_answer = ''
          @email.question_id = rand(Email::QUESTIONS.size)
        end
        @security_question = Email::QUESTIONS[@email.question_id.to_i]
        format.html { render :action => "new" }
        format.xml  { render :xml => @email.errors, :status => :unprocessable_entity }
      end
    end
  end
