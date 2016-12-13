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

        # Using property
        #
        #   :name   => { :type => "string", :analyzer => "snowball" },
        #
        # Get elasticsearch log 
        # Caused by: java.io.IOException: Can't sort on string types with more than one value per doc, or more than one token per field
        #
        # I found this thread, about multi-field:
        #
        # http://elasticsearch-users.115913.n3.nabble.com/Sorting-failing-in-latest-master-td967979.html
        # http://www.elasticsearch.org/guide/reference/mapping/multi-field-type.html
        
        # Nothing error, but is not ordered correctly
        :name   => { 
          :type => 'multi_field', :fields => { 
            'name'          => { :type => 'string', :index => :analyzed, :analyzer => "snowball" }, 
            'name_sortable' => { :type => 'string', :index => :not_analyzed } 
          }
        },
        :email  => { :type => "string" }
      }
    }
  }

  import users
  refresh
end

search = Tire.search("users") do
  query { string "zigotto.com" }
  sort { by :name_sortable, 'asc' }
end

search.results.each do |doc|
  puts "* #{doc.name}"
end

# The results:
#
#     * Jesus Lopes
#     * Éder Costa
#
# The correct results:
#
#     * Éder Costa
#     * Jesus Lopes
