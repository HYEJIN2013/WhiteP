class User < ActiveRecord::Base
  has_many :invite_recipients
  has_many :invite, through: :invite_recipients, class_name: Invite
  has_many :sent_invites, class_name: 'Invite', foreign_key: 'sender_id'
end

class UserGroup < ApplicationRecord
  has_many :invites
end

class Membership < ApplicationRecord
  belongs_to :user
  belongs_to :user_group
end

class Invite < ApplicationRecord
  belongs_to :user_group
  belongs_to :sender, class_name: 'User'
  has_many   :invite_recipients
  has_many   :recipients, through: :invite_recipients, class_name: 'User'
end

class InviteRecipient < ApplicationRecord
  belongs_to :invite
  belongs_to :user, class_name: 'User', foreign_key: :user_id
end

# Schema

ActiveRecord::Schema.define(version: 20161010194628) do

  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"

  create_table "authentication_providers", force: :cascade do |t|
    t.string   "name"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["name"], name: "index_name_on_authentication_providers", using: :btree
  end

  create_table "invite_recipients", force: :cascade do |t|
    t.integer  "invite_id"
    t.integer  "user_id"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["invite_id"], name: "index_invite_recipients_on_invite_id", using: :btree
    t.index ["user_id"], name: "index_invite_recipients_on_user_id", using: :btree
  end

  create_table "invites", force: :cascade do |t|
    t.string   "email"
    t.integer  "user_group_id"
    t.integer  "sender_id"
    t.string   "token"
    t.datetime "created_at",    null: false
    t.datetime "updated_at",    null: false
    t.index ["user_group_id"], name: "index_invites_on_user_group_id", using: :btree
  end

  create_table "memberships", force: :cascade do |t|
    t.boolean  "active"
    t.integer  "user_id"
    t.integer  "user_group_id"
    t.datetime "created_at",    null: false
    t.datetime "updated_at",    null: false
    t.index ["user_group_id"], name: "index_memberships_on_user_group_id", using: :btree
    t.index ["user_id"], name: "index_memberships_on_user_id", using: :btree
  end

  create_table "roles", force: :cascade do |t|
    t.string   "name"
    t.string   "resource_type"
    t.integer  "resource_id"
    t.datetime "created_at"
    t.datetime "updated_at"
    t.index ["name", "resource_type", "resource_id"], name: "index_roles_on_name_and_resource_type_and_resource_id", using: :btree
    t.index ["name"], name: "index_roles_on_name", using: :btree
  end

  create_table "user_authentications", force: :cascade do |t|
    t.integer  "user_id"
    t.integer  "authentication_provider_id"
    t.string   "uid"
    t.string   "token"
    t.datetime "token_expires_at"
    t.text     "params"
    t.datetime "created_at",                 null: false
    t.datetime "updated_at",                 null: false
    t.index ["authentication_provider_id"], name: "index_user_authentications_on_authentication_provider_id", using: :btree
    t.index ["user_id"], name: "index_user_authentications_on_user_id", using: :btree
  end

  create_table "user_groups", force: :cascade do |t|
    t.string   "name"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "users", force: :cascade do |t|
    t.string   "email",                  default: "", null: false
    t.string   "encrypted_password",     default: "", null: false
    t.string   "reset_password_token"
    t.datetime "reset_password_sent_at"
    t.datetime "remember_created_at"
    t.integer  "sign_in_count",          default: 0,  null: false
    t.datetime "current_sign_in_at"
    t.datetime "last_sign_in_at"
    t.inet     "current_sign_in_ip"
    t.inet     "last_sign_in_ip"
    t.datetime "created_at",                          null: false
    t.datetime "updated_at",                          null: false
    t.index ["email"], name: "index_users_on_email", unique: true, using: :btree
    t.index ["reset_password_token"], name: "index_users_on_reset_password_token", unique: true, using: :btree
  end

  create_table "users_roles", id: false, force: :cascade do |t|
    t.integer "user_id"
    t.integer "role_id"
    t.index ["user_id", "role_id"], name: "index_users_roles_on_user_id_and_role_id", using: :btree
  end

  add_foreign_key "invite_recipients", "invites"
  add_foreign_key "invite_recipients", "users"
  add_foreign_key "invites", "user_groups"
  add_foreign_key "memberships", "user_groups"
  add_foreign_key "memberships", "users"
end
