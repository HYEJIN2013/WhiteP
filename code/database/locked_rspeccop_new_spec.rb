require 'spec_helper'
require 'ruby-debug'

feature "the new cop page", :type => feature, :js => true do
	let(:cop) { attributes_for(:cop) }
	let(:precinct) { create(:precinct) }

  before do
   visit '/cops/new'
  end

  scenario "creates a new cop with valid inputs", :focus => true do
  	expect(page).to have_css('h2', text: 'Enter a New Cop')

		fill_in 'name', with: cop[:name]
		fill_in 'badge-number', with: cop[:badge_number]

    expect { click_button 'Submit' }.to change{Cop.count}.by(1)
  end
end
