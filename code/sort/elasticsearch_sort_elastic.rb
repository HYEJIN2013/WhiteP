# encoding: utf-8
require "tire"

users = [
  { :id => '1', :type => 'user', :name => 'Jesus Lopes',  :email => 'jl@zigotto.com' },
  { :id => '2', :type => 'user', :name => 'Alfredo',      :email => 'alfredo@email.com' },
  { :id => '3', :type => 'user', :name => 'Éder Costa',   :email => 'ec@zigotto.com' }
]

Tire.index("users") do
  delete

  create :mappings => {
    :user => {
      :properties => {
        :id     => { :type => "string", :index => "not_analyzed", :include_in_all => false },
        :name   => { :type => "string", :analyzer => "snowball" },
        :email  => { :type => "string" }
      }
    }
  }

  import users
  refresh
end

search = Tire.search("users") do
  query { string "zigotto.com" }
  sort { by :name, 'asc' }
end

search.results.each do |doc|
  puts "* #{doc.name}"
end

# The results:
#
# nothing...



# lasticsearch.log
#
# Caused by: java.io.IOException: Can't sort on string types with more than one value per doc, or more than one token per field
# at org.elasticsearch.index.field.data.strings.StringOrdValFieldDataComparator.setNextReader(StringOrdValFieldDataComparator.java:119)
# at org.apache.lucene.search.TopFieldCollector$OneComparatorNonScoringCollector.setNextReader(TopFieldCollector.java:95)
# at org.apache.lucene.search.IndexSearcher.search(IndexSearcher.java:523)
# at org.elasticsearch.search.internal.ContextIndexSearcher.search(ContextIndexSearcher.java:198)
# at org.elasticsearch.search.internal.ContextIndexSearcher.search(ContextIndexSearcher.java:153)
# at org.apache.lucene.search.IndexSearcher.search(IndexSearcher.java:433)
# at org.apache.lucene.search.IndexSearcher.search(IndexSearcher.java:356)
# at org.elasticsearch.search.query.QueryPhase.execute(QueryPhase.java:215)
# ... 9 more
