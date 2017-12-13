Accessing the site:

Remotely: 
  http://vcm-2370.vm.duke.edu/ for the main site and http://vcm-2370.vm.duke.edu/admin for the admin.

  You can register your own account, or access the main site and the admin site using our credentials:
  Usernames: nhb8, amd112, kne3, sas118, su26
  Password: testing123

Locally:

  To run the site locally, there are a few steps. 
  Make sure django is installed (you can use pip).
  First, download the source code and navigate to the "convos" directory (site/convos)
  Run the following command with python:
  python manage.py makemigrations
  python manage.py migrate
  python manage.py loaddata production_data.json

  Then, open the file ./mysite/settings.py and set DEBUG=True.

  Finally:
  python manage.py runserver

  Then, the site is accessible at 127.0.0.1:8000 for the main site and 127.0.0.1:8000/admin for the admin.

  You can register your own account, or access the main site and the admin site using our credentials:
  Usernames: nhb8, amd112, kne3, sas118, su26
  Password: testing123

Note of Caution:
  The site automatically sends emails to users when they are selected for a dinner, and notifies applicants to the same dinner when they were not selected, so if you change this information for past dinners, real emails will be sent to real students. So, if you want to test out this functionality, please create a new dinner that only you applied to.
