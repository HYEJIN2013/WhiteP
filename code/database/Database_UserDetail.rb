class UserDetail
  include Mongoid::Document
  belongs_to :user
  accepts_nested_attributes_for :user

  #fields
  field :term , type: String
  field :block , type: String
  field :course , type: String
  field :alumni , type: Boolean
end
