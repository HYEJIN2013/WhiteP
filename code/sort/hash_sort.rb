def sort_hash(hash)
  sorted_hash = {}
  hash.keys.sort.each do |k|
    if hash[k].is_a?(Hash)
     sorted_hash[k] = sort_hash(hash[k])
    elsif hash[k].is_a?(Array) && hash[k].first.is_a?(Hash)
      sorted_hash[k] = hash[k].collect{ |h| sort_hash(h) }
    else
     sorted_hash[k] = hash[k]
    end
  end
  sorted_hash
end

# 1.9.3p392 :034 > sort_keys(h)
# => {:y=>{:u=>{:t=>4}, :w=>3, :x=>2}, :z=>1}
# 1.9.3p392 :035 > h
# => {:z=>1, :y=>{:x=>2, :w=>3, :u=>{:t=>4}}}

ordered_actual_response = sort_hash(JSON.parse(response_body)).to_json
ordered_expected_response = sort_hash(JSON.parse(expected_response)).to_json
ordered_actual_response.should eq ordered_expected_response
