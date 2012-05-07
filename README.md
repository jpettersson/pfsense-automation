pfSense automation
==================

Automating the pfsense web panel using [Ghost.py](http://jeanphix.me/Ghost.py/)

Add a single PPTP VPN user:<br />
``./vpn_add_user.py pfsense_admin_password vpn_user vpn_user_password``

Add multiple PPTP VPN users from a file and automatically email them setup instructions:<br />
``./create_vpn_users_from_file.rb you@your-domain.com:email_password pfsense_admin_password vpn/users.txt``