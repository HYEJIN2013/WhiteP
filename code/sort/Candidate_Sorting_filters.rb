# In this file we define the methods to help filter out candidates

def find(id)
	@candidates.select { |candidate| candidate[:id] == id}		
end

def experienced(candidate)
	candidate[:years_of_experience] >= 2
end

def git_points(candidate)
	candidate[:github_points] >= 100
end

def language(candidate)
	candidate[:languages].include?("Ruby") && candidate[:languages].include?("Python")
end

def apply_date(candidate)
	(0.days.ago.to_date - candidate[:date_applied])<= 15
end

def age(candidate)
	candidate[:age] >= 18
end

#creates sorted list of candidates

def qualified_candidates(candidates)
	candidate_list =[]
	candidates.each do |candidate|
		if experienced(candidate) && git_points(candidate) && apply_date(candidate) && language(candidate) && age(candidate)
			candidate_list.push(candidate)
		end
	end
	candidate_list
end

#Method that orders candidates by qualification and if qual is equal, orders candidates by github points
def ordered_by_qualifications(candidates)
	@candidates.sort do |a,b|
		if b[:years_of_experience]  == a[:years_of_experience]
			b[:github_points] <=> a[:github_points]
		else
			b[:years_of_experience] <=> a[:years_of_experience]
		end
	end
end

 # Create a REPL that presents the user with a menu where they can type in one of the following commands:

def find_candidates
  running = true
  while running
    puts "Menu - Please select a candidate using the menu below
          - Please use 'find + id' number to find your candidate
          - Use 'all' to list all candidates
          - Use 'qualified' to list just quilified candidates
          - use 'quit' to finished"
 # find 1: This will display candidate with id 1
    answer = gets.chomp
    id_number = anser.slice(/\d/).to_i
    answer = anser.slice(/\w*/)
     case answer
       when "find"
          if qualified_candidate?(find(id_number)[0])
            puts find(id_number).to_s.green
          else
            puts find(id_number).to_s.red
          end
# all: This will print them all out to the screen (one per line)
       when "all"
          puts ordered_by_qualifications(@candidates)
# qualified: This will print only qualified candidates, ordered by experience and points (one per line)
       when "qualified"
          puts qualified_candidates(@candidates)
# quit: Exit the REPL / program
       when "quit"
          running = false
       else
         puts "invalid input"
     end
  end
end 
