# URL-Shortener
  A simple URL - Shortening web app written in Python and Flask, also comes with a simple [API](https://min-me.herokuapp.com/api).\
  
  <img src="https://github.com/Vivek-Kolhe/URL-Shortener/blob/main/resources/GIF-210413_183835.gif" alt="gif" width=1000px height=562px />

# Dependencies
  - Flask\
  ```pip install flask```

  - Flask-SQLAlchemy\
  ```pip install Flask-SQLAlchemy```
  
  - Gunicorn\
  ```pip install gunicorn```
  
  <b><i>or use: </b></i> ```pip install -r requirements.txt```

# Deploying on Heroku
Change ```APP_URL``` in ```__init__.py``` (```https://{your_heroku_app_name}.herokuapp.com/```).\
Clone and download the repository and run the following commands.\
<b><i>Note:</b></i> Requires HerokuCLI. Install from [here](https://devcenter.heroku.com/articles/heroku-cli#download-and-install).
```
cd ./{PROJECT_DIR}
heroku create app_name
git init
heroku git:remote -a app_name
git add .
git commit -am "deploying"
git push heroku master
```
