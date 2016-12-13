# 1. Require the gem sqlite3.  You must `gem install sqlite3` if you get an error
# stating `cannot load such file -- sqlite3`
# This will add the gem to your local gemset
require 'firebase'
require 'faker'

# 2. Sign up for a firebase account and set the uri here
base_uri="https://luminous-fire-2162.firebaseio.com/"

# 3. Set up a connection to the database you have created
firebase = Firebase.new(base_uri)

# Ruby some JSON to the cloud... sorta kinda like SQL
firebase.push("students",
{
  lastname:   "Lubaway",
  firstname:  "Topher",
  cohort:     "Fence Lizard",
  phase:      "14"
  })
15.times do
  firebase.push("students",
  {
    lastname:   Faker::Name.last_name,
    firstname:  Faker::Name.first_name,
    cohort:     Faker::Company.bs,
    phase:      rand(10)
    })
end
