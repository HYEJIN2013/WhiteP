class User
  include Mongoid::Document
  authenticates_with_sorcery!
  has_one :user_details

  field :email , type: String
  field :id_number , type: String
  field :crypted_password , type: String
  field :salt , type: String
  field :fname , type: String
  field :lname , type: String
  field :mname , type: String
  field :avatar
  field :gender , type: Boolean
  field :role , type: String
  field :reset_password_token , type: String
  field :reset_password_token_expires_at, type: DateTime
  field :reset_password_email_sent_at, type: DateTime
  field :remember_me_token, type: String
  field :remember_me_token_expires_at, type: DateTime
  field :deactivated , type: String


end
