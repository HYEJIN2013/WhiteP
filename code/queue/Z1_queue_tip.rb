def queue_tip(*args)

  queue = ["A","B","C","D","E","F","G","H"]

  return queue if args.size == 0
  raise "odd number of arguments" unless args.size.even?

  slots = {}
  letters = {}

  args.each do |a|
    # process slot
    if a =~ /^[0-9]+$/
      a = a.to_i
      raise "slot '#{a}' does not exist" if a >= queue.length
      raise "slot '#{a}' is not unique" if slots.key?(a)
      slots[a] = 1

    # process letter
    elsif a =~ /^[a-zA-Z]{1}$/
      a = a.capitalize
      raise "letter '#{a}' doesn't exist in the queue" unless queue.include?(a)
      raise "letter '#{a}' is not unique" if letters.key?(a)
      letters[a] = 1
    end
  end

  raise "number of letters is not equal to number of slots" unless letters.size == slots.size

  q = []
  offset = 0

  # TODO improve merging

  # prefill new queue with given letters in specific slots
  slots.each_with_index { |slot, index| q[slot[0]] = letters.keys[index] }

  # fill the rest
  queue.each_with_index do |l, i|
    next if letters.key?(l)
    (offset..q.size).each do |j|
      if q[j].nil?
        q[j] = l
        offset+=1
        break
      end
    end
  end
  q
end

# specs


describe "#queue_tip" do
  it "should output original queue for no arguments" do
    queue_tip().should == ["A","B","C","D","E","F","G","H"]
  end

  it "should raise odd number of arguments error" do
    expect{ queue_tip("1", "C", "2") }.to raise_error RuntimeError, "odd number of arguments"
  end

  it "should raise error about missing slot" do
    expect{ queue_tip("9", "C") }.to raise_error RuntimeError, "slot '9' does not exist"
  end

  it "should raise error about slot uniqueness" do
    expect{ queue_tip("1", "C", "1", "D") }.to raise_error RuntimeError, "slot '1' is not unique"
  end

  it "should raise error about letter missing from the queue" do
    expect{ queue_tip("1", "Z", "2", "D") }.to raise_error RuntimeError, "letter 'Z' doesn't exist in the queue"
  end

  it "should raise error about letter uniqueness" do
    expect{ queue_tip("1", "D", "2", "D") }.to raise_error RuntimeError, "letter 'D' is not unique"
  end

  it "should raise error when number of slots != number of letters" do
    expect{ queue_tip("1", "D", "2", "H", "E", "F") }.to raise_error RuntimeError, "number of letters is not equal to number of slots"
  end

  it "should output CDEAFBGH" do
    queue_tip("3", "A", "B", "5").should == ["C", "D", "E", "A", "F", "B", "G", "H"]
  end

  it "should output BACDFGHE" do
    queue_tip("A", "H", "1", "6", "7", "E").should == ["B", "A","C","D","F","G","H","E"]
  end
end
