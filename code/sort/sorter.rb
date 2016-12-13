#!/usr/bin/env ruby

# sorter.rb
#
# Run with ruby, either by making this file executable or by prepending the
# command with 'ruby', for example 'ruby sorter.rb dryrun'.
# 
# Ruby should be pre-installed on most Unix-like operating systems, including
# GNU/Linux and Mac OSX
#
# Most of the functionality in this script is provided by the regular expression
# MATCH_PATTERN. This regex is simply used to extract the vendor name from the
# filename by capturing it in a capture group (the set of parenthesis). The 
# exact pattern to match and portion to extract can easily be changed by
# modifying the MATCH_PATTERN regular expression
#
#
#
#           License (3-clause BSD)   
#
#
# Copyright (c) 2013, Jake Drahos <drahos.jake@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without 
# modification, are permitted provided that the following conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this 
# list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, 
# this list of conditions and the following disclaimer in the documentation and/or 
# other materials provided with the distribution.
# 
# 3. Neither the name of the copyright holder nor the names of its contributors 
# may be used to endorse or promote products derived from this software without 
# specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR 
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; 
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON 
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS 
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Match pattern
MATCH_PATTERN = /[[:digit:]]{8} - ([[:alnum:]_&\$\(\)'",!? ]*) - [[:alnum:]_&\$\(\)'",!? ]*\.[PpDdFf]{3}/

# Regular expression breakdown:
#
# [[:digit:]]{8}	: 8 digits, datestamp[[:alnum:]_ ]*
#  - 				: Literal space hyphen space
# ([[:alnum:]_& ]*)	: Arbitrary length vendor, captured
#  - [[:alnum:]_& ]* : Type of file, not used
# \.pdf				: Literal .pdf file extension
#
# The vendor name is captured in capture group 1

# Usage
USAGE = <<EOF
sorter.rb {run|dryrun} [directory]
    Sort all files in the current or provided directory into the appropriate
directories based on the captured portion of the match regex. Specify either
a run or a dry run, a dry run will simply print the files to be moved without
touching anything. A full run will actually move the files into the appropriate
directories. The second argument is optional. If it is not provided, the 
sorter will run on the current directory. If it is provided, the sorter will cd
into the provided directory before beginning the sort process. The parent directory
of the input directory will be searched for output directories. If no output
directory is found, the file will not be moved.
EOF

# Sorter

if ARGV.size < 1 or ARGV[0] !~ /run|dryrun/
  puts USAGE
  exit
end

# cd to target directory if present

if ARGV.size > 1
  puts "Changed to directory '#{ARGV[1]}'"
  Dir.chdir(ARGV[1])
end

if ARGV[0] == 'dryrun'
  puts 'Dry run, nothing will be touched.'
end

# Iterate through entries

Dir.foreach('.') do |file|
  # Skip if it is a directory
  next if Dir.exist? file 

  # Match against pattern to extract vendor name
  next unless MATCH_PATTERN =~ file
  vendor = MATCH_PATTERN.match(file)[1]
  
  # Search parent directory for destination directory
  dest_dir = Dir.glob("../**/#{vendor}").first
  
  # Handle situation if destination does not exist
  dest_dir = '.' if dest_dir.nil? or dest_dir.empty?

  puts "Moving '#{file}' to '#{dest_dir}/'"

  # Move file
  if ARGV[0] == 'run'
    File.rename file, "#{dest_dir}/#{file}"
  end
end

if ARGV[0] == 'dryrun'
  puts 'This was a dry run, no files have been moved.'
else
  puts 'Done!'
end
