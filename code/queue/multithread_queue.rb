# --- FILL

sqs  = AWS::SQS.new(S3)
queue = sqs.queues.create('holiday')
i = 0

send = lambda { |start, finish|
  HolidayCampaign.even.unsent.find_in_batches(batch_size: 10, start: start) do |batch|
    users = batch.collect { |hc| "#{hc.id.to_s}||#{hc.user_id.to_s}||#{hc.name}" }
    queue.batch_send(users)
    i += 10
    break if i >= finish
  end
}

Thread.new { send.call(0, 100000) }; Thread.new { send.call(100000, 200000) }; Thread.new { send.call(200000, 300000) }; Thread.new { send.call(300000, 400000) }; Thread.new { send.call(400000, 500000) }; Thread.new { send.call(500000, 600000) }; Thread.new { send.call(600000, 700000) }

# --- DRAIN
sqs  = AWS::SQS.new(S3)
queue = sqs.queues.create('holiday')

receive = lambda {
  while (m = queue.receive_message)
    hcid, uid, name = m.body.split('||')
    HolidayCredit.create(:user_id => uid, :amount => 5.0)
    HolidayCampaign.find(hcid).update_column :sent, true
    m.delete
  end
}

30.times { Thread.new { receive.call() } }

# --- FORK PROCESS APPROACH
jobs_per_process = 100
process_count = 20

HolidayCampaign.even.unsent.find_in_batches(batch_size: jobs_per_process * process_count) do |group|
  batches = group.in_groups(process_count)

  batches.each do |batch|
    Process.fork do
      ActiveRecord::Base.establish_connection
      batch.each do |hcampaign|
        HolidayCredit.create(:user_id => hcampaign.user_id, :amount => 5.0)
        hcampaign.update_column :sent, true
      end
    end
  end
end
