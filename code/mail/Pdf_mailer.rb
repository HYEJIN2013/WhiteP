# Orders controller

pdf = render_to_string :template => "/admin/orders/show.pdf.erb", :pdf => "file_name", 
:footer => { :spacing => -20, :html => { :template => "/admin/orders/footer.pdf.erb" }}

StoreMailer.order_confirmation(@order,pdf).deliver

#Store mailer

def order_confirmation(order,pdf=nil)
  @order = order
  attachments['faktura.pdf'] = pdf if pdf.present?
  mail(:to => "#{order.name} <#{order.email}>", :subject => 'Din beställning')
end
