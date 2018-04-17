# Ghost Name Picker

A simple API to let you choose one of three randomly selected unique ghosts from a list of available ghosts.

## Design
On startup of the application, the ghosts entities are stored in the database taken from a Python script used for storage. This only occurs once, given there are no ghost entities in the database.
This API contains four pages
- Home
- Create account
- Login
- Logout
The home page displays all the ghosts as a table, displaying their name, description and their availability. Should there be any users that have signed up, a table will display of users with their ghost name. The page uses a session based service and will display the currently signed in user at the top of the page if there is one as well as a button to sign out, otherwise, account creation and account sign in forms will show leading to their respective pages. All pages aside from the home page primarily serve to indicate the forms leading to their pages have been correctly filled out and submitted.
The Create account page is displayed when the user fills out and submits the form to create an account. All fields are required to successfully submit the form. The email is checked to see if one of the same name has already been submitted, the request to create an account if rejected if true. Should the user be successful, a page will be served to show the user and their selected ghost.
The Login page serves a similair purpose to the Create account page - namely only for confirmation of form submission. The server will check and compare the password to the SHA-12 encrypted passwords stored in the database along with the emails submitted and emails stored in the database. In the case of a match, a user session is created to persist the user as being logged in until they are logged out or when the session expires.
The Logout page is served on pressing the "logout" button, removing the current user session.
## Technology
Uses Google App Engine to build and deploy (more specifically Google Cloud Engine for deployment).
Written fully in Python 2.
Uses Datastore as database engine to store the users and ghosts assigned to the users.  
[Bootstrap](https://getbootstrap.com/) is used to supplement the views visible to the user and is the toolkit to supplement the HTML with CSS classes along with Django-esque notation to handle conditional logic such as:
```
{% if something_to_be_true %}
{% endif %}
```
## Further Notes
### Improvability/Limitations
This project could use a better framework to request data from the API; as of date, HTML form requests are sent directly to the Python backend to fulfill the client's request.

Ideally in the future, a better front end web framework such as [AngularJS](https://docs.angularjs.org/api) would be implemented to serve the front end HTML and would use a proper [Model-View-Controller](https://blog.codinghorror.com/understanding-model-view-controller/) pattern to serve the solution.

Currently, the ghosts are stored in a Python file, sourced from a Google Sheets file. In the case that the list of ghosts would expand, a solution could be considered to scrape the sheets periodically to update the list, however there may be a limitation in which the source of the list may become a private, which would render the source inaccessible unless the request to scrape the list would include the credentials of an authorized user. For this I would consider the [Python Google Sheets API](https://developers.google.com/sheets/api/quickstart/python)

Should the database need to scale to handle more users/tables, I would consider [PostgreSQL](https://www.postgresql.org/) as a suitable candidate as Webapp2 strongly supports its implementation.

The ability to remove a user and to 'release' a ghost from a user or to assign another ghost could be considered as an improvement for the future as there is no current ability to delete a user or to reassign a ghost right now.

In the case that user submitted data is sensitive (and in reality they are) all details of a user would be stored using encryption, similairly to the currently encrypted password.
