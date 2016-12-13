# Gemfile
group :test do
  gem "database_cleaner"
end

# spec/support/database_cleaner.rb
RSpec.configure do |config|
  DatabaseCleaner.strategy = :truncation

  config.before(:each) do
    DatabaseCleaner.start
  end

  config.after(:each) do
    DatabaseCleaner.clean
  end
end
