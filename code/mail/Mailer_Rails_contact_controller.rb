#app/controllers/contact_controller.rb

class ContactController < ApplicationController

  def new
    @message = Message.new
  end

  def create
    @message = Message.new(params[:message])

    if @message.valid?
      NotificationsMailer.new_message(@message).deliver
      redirect_to(root_path, :notice => "El mensaje fue enviado correctamente. Te contactaremos a la brevedad (:")
    else
      redirect_to(contact_path, :notice => "Hay campos incompletos, intenta nuevamente.")
    end
  end

end
