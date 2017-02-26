# item-catalog
This is a python module that creates a website and JSON API for a list of items grouped into a category. Users can edit or delete items they've creating. Adding items, deleteing items and editing items requiring logging in with Google+ or Facebook.

## Instructions to run Project:

## Set up a Google Plus auth application.
1. go to https://console.developers.google.com/project and login with Google.
2. Create a new project
3. Name the project
4. Select "API's and Auth-> Credentials-> Create a new OAuth client ID" from the project menu
5. Select Web Application
6. On the consent screen, type in a product name and save.
7. In Authorized javascript origins add: http://0.0.0.0:8080 http://localhost:8080
8. Click create client ID
9. Click download JSON and save it into the root director of this project.
10. Rename the JSON file "client_secret.json"
 
## Set Up facebook auth application:
1. go to https://developers.facebook.com/ and login with Facebook2. .
2. In the drop down menu at far right click on add new application.
3. Make your own fb_client_secrets.json file and add client_id and secret to it
4. click on add product and add Facebook Login and add  http://0.0.0.0:8080 http://localhost:8080 in javascript origins.

## Setup The database and starting the server:
1. In the root director, use the command vagrant up
2. The vagrant machine will install.
3. Once it's complete, type vagrant ssh to login to the VM.
4. In the vm, cd /vagrant
5. type "pyhon database_setup.py" this will create the database with the categories defined in that script.
6. Populate the database using "python lotsofitems.py"
6. type "python project.py" to start the server.

## Start using the website by typing http://localhost:8000/ in browser
