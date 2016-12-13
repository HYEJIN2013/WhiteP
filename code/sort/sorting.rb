class Peripheral < ActiveRecord::Base
  has_many :quotes, :order=>"peripheral_id"
end

class Quote < ActiveRecord::Base
  belongs_to :peripheral
end

def admin
 session[:item]=params[:val]
 @quotes = Quote.find(:all,:conditions => ['unit_id=?',session[:item]])		
end

<% @quotes.each do |quote| %>
  <tr>
    <td><%=h quote.part_number %></td>
    <td><%=h quote.description %></td>
    <td><%=h quote.unit_id %></td>
    <td><%=h quote.peripheral.name %></td> <!--Sort by this column-->
    <td><%= link_to 'Show', quote %></td>
    <td><%= link_to 'Edit', edit_quote_path(quote) %></td>
    <td><%= link_to 'Delete', quote, :confirm => 'Are you sure?', :method => :delete %></td>
  </tr>
<% end %>
