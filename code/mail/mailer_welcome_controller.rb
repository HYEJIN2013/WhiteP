class WelcomeController < ApplicationController
  def index
  	UserMailer.welcome_email('demas').deliver
  end
end
