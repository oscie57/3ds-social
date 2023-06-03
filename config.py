# If you're adding a new config option, please update WiiLink24/production-deployment's
# copy of config.py to match the new options once committed to master.

# Primary config for room-server
db_url = "postgresql://postgres:postgres@localhost/3dssocial"

# Used as the base domain within first.bin.
# To resolve to 127.0.0.1, feel free to use "dev.wiilink24.com".
root_domain = "192.168.0.69"
root_https_enabled = False

# Used to secure the web panel.
secret_key = "please_change_thank_you"
