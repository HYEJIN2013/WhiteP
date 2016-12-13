def welcome_email(user)
    @user = user
    @url = 'http://example.com/login'
    mail(to: 'andrey.demidov@gmail.com', subject: 'Welcome')
  end
