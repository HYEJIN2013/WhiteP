require 'net/imap'
require 'kconv'
# 文字エンコードgem

imap_ssl = true

imap_host = 'imap.gmail.com'
imap_port = 993

imap_user = ''
imap_pass = ''

imap = Net::IMAP.new(imap_host, imap_port, imap_ssl)
imap_login(imap_user, imap_pass)
imap.examine('INBOX')

imap.search(['UNSEEN']).each do |msg_id|
    msg = imap.fetch(msg_id, []).first

    subject = msg.attr['BODY[HEADER.FIELDS (SUBJECT)]']
    sender  = msg.attr['ENVELOPE'].from.first
    puts "#{sender.mailbox}@{mail.host}"
end
