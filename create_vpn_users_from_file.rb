#!/usr/bin/ruby

#
# Create multiple pfSense VPN users from a list and automatically send them a setup email with instructions.
# Depends on vpn_add_user.py, sendemail and a Gmail account.
#

DOMAIN = "@your-domain.com" # Change this to your organizations domain

require 'erb'

if ARGV.length != 3
  puts "ERROR: Invalid arguments. Example: ./create_vpn_users.rb gmail_address:password pfsense_admin_password vpn/users.txt"
  exit
end

gmail_username = ARGV[0].split(":")[0]
gmail_password = ARGV[0].split(":")[1]
pfsense_password = ARGV[1]

file = File.new(ARGV[2], "r")

PASSWORD_CHARS = ("a".."z").to_a + ("A".."Z").to_a + ("0".."9").to_a

while (line = file.gets)
    user = line.strip
    user_email = user + DOMAIN
    password = Array.new(8, '').collect{PASSWORD_CHARS[rand(PASSWORD_CHARS.size)]}.join
    
    # Try and create the user with the python script
    output = `./vpn_add_user.py #{pfsense_password} #{user} #{password}`; result=$?.success?
    
    if result == true      
      # The user has been created
      # Fetch the template instructions
      message = ERB.new(File.open("vpn/message.txt", "rb").read).result
      
      # Attempt to send an instruction email to the new user using sendemail and Gmail.
      output = `sendemail -f #{gmail_username} -t #{user_email} -u VPN Account Created -m "#{message}" -s smtp.gmail.com -o tls=yes -xu #{gmail_username} -xp #{gmail_password}`; result=$?.success?
      
      if result == true
        puts "Created user: #{user} #{user_email} #{password}"        
      else
        puts "ERROR: Could not send email to #{user_email}"
      end
      
    else
      puts "ERROR: Could not create user #{user}"
    end
end

file.close