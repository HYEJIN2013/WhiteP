class TestClass
  @queue = :test_class

  def self.perform(arg_a, arg_b)
  end
end

Resque.enqueue(TestClass, 1, 2)
