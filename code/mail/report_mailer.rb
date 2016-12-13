class ReportMailer < ApplicationMailer
  def new_report_email recipient, report_builder
    attachments['report.pdf'] = { mime_type: 'application/pdf', content: report_builder.generate_stream }
    mail(to: recipient, subject: report_builder.title)
  end
end
