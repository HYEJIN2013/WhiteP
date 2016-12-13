require './my_queue'
require 'rspec'

describe MyQueue do
  it "initializes with a size of zero" do
    MyQueue.new.size.should eq 0
  end

  it "is empty after initialization" do
    MyQueue.new.is_empty?.should eq true
  end  

  describe "#enqueue" do
    before do
      @queue = MyQueue.new
    end

    it "enqueues and item" do
      @queue.enqueue("a").should =~ ["a"]
    end

    it "increments the size by 1" do
      @queue.enqueue("a")
      @queue.enqueue("b")
      @queue.size.should eq 2
    end

    it "is no longer empty" do
      @queue.enqueue("a")
      @queue.is_empty?.should eq false
    end
  end

    describe "#peek" do
      before do
        @queue = MyQueue.new
      end
      
      it "shows the item that is at the head" do
        @queue.enqueue("a")
        @queue.enqueue("b")
        @queue.enqueue("c")
        @queue.peek.should eq "a"
      end

      it "returns nil if the queue is empty" do
        @queue.peek.should be_nil
      end
    end

    describe "#dequeue" do
      before do
        @queue = MyQueue.new
      end

      it "removes the item at the head" do
        @queue.enqueue("a")
        @queue.enqueue("b")
        @queue.enqueue("c")
        @queue.dequeue.should eq "a"
      end

      it "decrements the size by one" do
        @queue.enqueue("a")
        @queue.enqueue("b")
        @queue.enqueue("c")
        @queue.dequeue
        @queue.size.should eq 2
      end

      it "doesn't decrement the size if the queue is empty" do
        @queue.dequeue
        @queue.size.should eq 0
      end
    end

end
