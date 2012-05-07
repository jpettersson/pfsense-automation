#!/usr/bin/python

#
# Use the pfSense web panel to create a new VPN user.
#

import sys

from ghost import Ghost
ghost = Ghost()

if (len(sys.argv) == 4):
	
	URL = "http://172.16.0.1"
	ADMIN_USER = "admin"
	
	admin_password = sys.argv[1]
	username = sys.argv[2]
	password = sys.argv[3]

	page, extra_resources = ghost.open(URL)
	# At the login page?
	if page.http_status==200:
	
		# Fill out login form
		result, resources = ghost.fill("form[name=login_iform]", {
		    "usernamefld": ADMIN_USER,
		    "passwordfld": admin_password
		})
	
		# Trigger click on submit button using it's CSS class as selector.
		# Simply submitting the form does not work because of their JS implementation.
		page, resources = ghost.fire_on(".formbtn", "click", expect_loading=True)
	
		if page.http_status == 200:
			
			# Make sure we are logged in.
			result, resources = ghost.wait_for_selector("title")
			if "moat.ym - Status: Dashboard" in ghost.content:

				# Let's go to the VPN add user page
				ghost.open(URL + "/vpn_pptp_users_edit.php")
				result, resources = ghost.wait_for_selector("title")
				if "moat.ym - VPN: VPN PPTP: User: Edit" in ghost.content:
					
					# At the vpn add user page
					# Fill out the new user form
					result, resources = ghost.fill("form[name=iform]", {
					    "username": username,
					    "password": password,
						"password2": password
					})
					
					# Submit the form
					page, resources = ghost.fire_on("form", "submit", expect_loading=True)
					if page.http_status == 200:
						sys.exit(0)
					else:
						print "ERROR: The vpn user could not be created."
				
				else:
					print "ERROR: Could not get to the vpn add user page."
			else:
				print "ERROR: Could not log in."
				print ghost.content
		
		else:
			print "ERROR: Could not submit login form."
	else:
		print "ERROR: Could not get the login page."

else:
	print "ERROR: Invalid arguments. Example: python create_vpn_user.py admin_password vpn_user vpn_user_password"