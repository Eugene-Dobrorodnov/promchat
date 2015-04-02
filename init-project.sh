# set up the Procfile
touch Procfile
echo "web: python run.py" >> Procfile

# --------------------------

echo "Creating Heroku app & pushing"

heroku create --stack cedar
git push heroku master

echo "All Done!"