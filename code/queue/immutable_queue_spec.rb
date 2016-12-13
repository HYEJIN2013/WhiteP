describe ImmutableQueue do
  let(:queue) { ImmutableQueue.new }

  it 'is empty when created' do
    expect(queue).to be_empty
  end

  describe 'adding values' do
    it 'returns a queue with the added value' do
      combined = queue << 1
      expect(combined).to be_a ImmutableQueue
      expect(combined.first.object).to be 1
    end

    it 'does not modify the existing queue' do
      queue << 1
      expect(queue).to be_empty
    end

    it 'does not let modified values go through to the queue' do
      string = 'foo'
      queue_with_string = queue << string
      string << 'bar'
      queue_with_string.peek.should == 'foo'
    end
  end

  describe 'removing values' do
    let(:queue) { ImmutableQueue.new << 1 << 2 << 3 }

    it 'returns an array of the popped value and the modified queue' do
      expect(queue.pop).to eq [1, (ImmutableQueue.new << 2 << 3)]
    end

    it 'does not modify the existing queue' do
      original = queue.dup
      queue.pop
      expect(queue).to eq original
    end
  end
end
