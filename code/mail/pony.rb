def place
    Pony.mail(:to => StoreApplication::Admin.email,
      :from => "My Store <admin@edubegu.ru>",
      :via => :smtp, :via_options => {
        :address              => 'smtp.gmail.com',
        :port                 => '587',
        :user_name            => 'admin@edubegu.ru',
        :password             => 'GlobalOne',
        :authentication       => :plain,
        :domain               => "mail.gmail.com" },
      subject: "New order has been plased", body: "Please check back your admin page to see it!")
  end
