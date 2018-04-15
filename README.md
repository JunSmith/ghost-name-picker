Notes
	To run:
	>dev_appserver.py [--clean_datastore=true] .

Used standard environment for python in google appengine since it's targeted to a small amount of users, and doesn't need to scale

Principally, each endpoint should return a single view?
Nothing against that design

There's an obvious shortcoming/ improvement that's possible to scrape the google sheet of ghosts
  Issue as I have to sign with my gmail account/mail and access the third party list
  Restrictions may change and access may exclude me

Django template resource
	http://webapp2.readthedocs.io/en/latest/tutorials/gettingstarted/templates.html

Objective checklist
- assign a user to a random ghost - v
-  Persist the user within the session, going back home will display their
 name and their ghost
- templates
- authentication (user service)

should account for no more ghosts available

Resource for authentication/security
