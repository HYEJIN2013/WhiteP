class PoliteMailer

  def send(to)
		message = %Q[message for #{to}
		Hello,
		How are you today?
		I just had a great idea:
		#{yield}
		Hope to hear from you soon
		Best regards
		Evgeny]
		puts message
		# dispatch(message)
	end

end

mail = {
	"rob@makersacademy.com" => "Let's hire a new teacher",
	"ana@makersacademy.com" => "Let's buy a new fridge",
	"enrique@makersacademy.com" => "Can you please stay late tonight?"
}

mailer = PoliteMailer.new

mail.each do |email, body|
	puts
	mailer.send(email) do
		body
	end
	puts
end
