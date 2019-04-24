# fresh-air-cis467

### To Run
Navigate to `/fresh_air/`
Run `python manage.py runserver` from command line


### Overview
The basic layout is a series of "apps". The main app in this case is the `/fresh_air/fresh_air` directory. This handles the majority of the web app, but other functionalities have been sectioned off into other apps. For example, the `data_visualize` app has views and models we will use inside the `/fresh_air` app (more on that later). 

## URLs
When you hit a URL on the site (`/contact` for example), that is read in by the `urls.py` file in the `fresh_air` app. The file looks for a matching path, and then forwards the request onto the view associated with that path. So for this example, `/contact` matches the line 
`path('contact/', views.contact, name="Contact")`
So it will direct the request to a `view` called `contact` whose name is `Contact`. 
## Views
The app then looks through `/fresh_air/views.py` for a matching view. In this example, the program will look for `def contact(request):`.At this point you can make any necessary requests or permissions checks that you need before rendering the actual content. In this view (and many others) we check the name of the URL that sent us, to know whether to render an English template or a Spanish template. `/contact/` and `/es/contact` will render English and Spanish templates respectively. 
# Templates
The final line of the view will always be `return render(request, contact.html)` to tell the web app which page we're trying to pull up. The variable `templatePath` in `/fresh_air/settings.py` will tell us where to look for a folder called `templates` where all our html is stored.

That's the meat and potatoes, now where things get a LITTLE tricky. 

For the `/about` and `/report` pages, we need to run some code to generate those super cool maps you see. This code just needs to be included somewhere in a view or URL for the template to be able to call it. If you use the template tag `{%plotly_app name="neighborhood_map"%}` without loading the plotly map code, you will get an error. We chose to do this in the views. Forgive us, but we just pasted the code directly into the view. I'm sure there's a way to keep it in a separate file and include it into the view (thus making the code look cleaner) but I was struggling to find the right python syntax to do this. So in the `/about` and `/report` views, you'll see the code that builds the maps. The name required by the template tag is defined in the `app = DjangoDash(....` variable. Those names must match to load the correct map. 

If we rewind back to `/fresh_air/urls.py` you can see that for the `/report` url things look a little different. Instead of specifying a view, we instead include `data_visualize.urls` which will go grab the `urls.py` file from the `data_visualize` app. We could have avoided this and kept everything in one app, but we wanted to experiment a little with Django, so feel free to change this later to simplify things. The `data_visualize.urls` has only one view, and that view contains content very similar to the `/about` view, except with a different block of code. 

# Models
`data_visualize` also has some functions we will need to run our code. In both chunks of map code in the respective views, you'll see an import like `from data_visualize import models as dataPull`, which pulls in these functions that live in `/data_visualize/models.py`

We do something similar for the home page. The home page form requires a `push_signup` function. When the form is submitted it POSTs to URL whose name is `signup`. This URL directs to a view called `signup` in `fresh_air/views.py`. The `signup` view does a little bit of data management, and then calls a function `pushSignup`. This function is included by way of `from data_push.data_push import pushSignup`, and the function lives in `/data_push/data_push.py`, but could also live in `/data_push/models.py` or as mentioned previously, somewhere inside the `/fresh_air` app. As of now, I believe this is the SOLE purpose of the `/data_push` app. 

## Other apps
This leaves `/send_alert` and `/data_manage` as the only apps not yet discussed. These apps were used/edited by Megan and Tressa respectively, so I have little-to-no input on their contents. I know they have functions/scripts that work in those folders, but I do not believe they have been properly hooked up to a lambda function or chron job. 


### Live Deployment
So for deploying live I spent the majority of my time tinkering with Elastic Beanstalk, which is supposed to use EC2 instances to launch scalable web apps via Flask or Django or other frameworks. There may be a better solution for deployment, but this one seemed familiar to me being that we had already been working with AWS, and seemed to boast about Django app deployment explicitly. 

The 3 important things when deploying to EB are 
1. `.elasticbeanstalk` directory with `config.yml` file. 
2. `.ebextensions` directory with `config.django` file. 
3. `requirements.txt` file with `pip freeze` contents inside. 

You won't see these files in the master branch, but INSIDE the master branch in a zip called `freshair_19.zip` you can see a previous version of the app that I deployed (unsuccessfully). One major problem I consistently ran into was an inability to run or find the `wsgi.py` file. This file is located in `/fresh_air` and the path to it is specified in the aforementioned `config.django`. 

Otherwise I was pretty much just following directions. There are plenty of guides online for deploying a django app on EB but I just couldn't get it to work. I started with using the `ebcli` for the linux command line, running `eb init` and going from there. Best of luck!



