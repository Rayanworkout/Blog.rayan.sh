#!/bin/bash

# /var/www/html  must have www-data ownership
# VITE_API_URL=http://127.0.0.1:8000/core
# VITE_API_URL_PROD=http://194.135.81.27/core

# Apache2 error logs
# sudo cat /var/log/apache2/error.log

# Check apache config
# sudo apache2ctl configtest

# Stop if an error occurs
set -e

apache_folder="/var/www/html/"
project_folder="/home/rayan/dev/rayan.sh/"

cd "$project_folder"

# First delete blog_latest and Blog.rayan.sh folders if they exists
blog_latest="$project_folder/blog_latest"
git_cloned="$project_folder/Blog.rayan.sh"

if [ -d "$blog_latest" ]; then
    echo "blog_latest exists. Removing..."
    sudo rm -r "$blog_latest"
    echo "blog_latest removed."
else
    echo "blog_latest does not exist."
fi


if [ -d "$git_cloned" ]; then
    echo "git_cloned exists. Removing..."
    sudo rm -r "$git_cloned"
    echo "git_cloned removed."
else
    echo "git_cloned does not exist."
fi

# Creating blog folder if it doesn't exist
# in apache_folder
if [ ! -d "$apache_folder/blog" ]; then
    echo "Creating blog folder ..."
    sudo mkdir "$apache_folder/blog"
    echo "Folder created."
fi


echo "> Cloning repository ..."
git clone https://github.com/Rayanworkout/Blog.rayan.sh.git
echo "> ok"


echo "> Renaming folder to blog"
mv ./Blog.rayan.sh/ ./blog_latest/
echo "> ok"


# I check if DEBUG = TRUE, if so I stop the build
settings_file="blog_latest/backend/blog/settings.py"

if grep -q "DEBUG = True" "$settings_file"; then
    echo "DEBUG is set to True in Django settings. Aborting build ..."
    exit 1
else
    echo "DEBUG is False, continuing with the build."
fi

# Creating blog folder if it doesn't exist
# in project_folder
if [ ! -d "./blog" ]; then
    echo "Creating blog folder ..."
    sudo mkdir "./blog"
    echo "Folder created."
fi

# Trailing slash after source directory to copy the content of the folder
# and not the folder itself
echo "> Copying folder to Project directory"
sudo rsync -av --exclude='.git/' ./blog_latest/ ./blog/
echo "> Folder copy ok"

cd ./blog/backend
echo '> Creating venv ...'
python3 -m venv .venv
echo '> venv ok'

echo '> Activate venv and install requirements'
source .venv/bin/activate
pip install -r requirements.txt
echo '> Requirements ok'

echo '> Starting migrations'
python3 ./manage.py makemigrations
python3 ./manage.py migrate
echo '> Migrations ok'



static_folder="$project_folder/blog/backend/static"

# Check if the folder exists
if [ -d "$static_folder" ]; then
    echo "Static folder exists. Deleting it ..."
    # Remove the folder and its contents
    rm -r "$static_folder"
    echo "Folder deleted."
fi


echo '> Collecting static'
python3 ./manage.py collectstatic
echo '> Static ok'

echo '> Changing db permission'
chmod 664 ./db.sqlite3
echo '> ok'


# Deleting temp folder
echo '> Deleting temp folder'
sudo rm -r "$blog_latest"
echo '> Done'


###### FRONTEND ######


cd "$project_folder/blog/frontend"

# Copy .env into the build folder
echo "> Copying .env file to project folder"
sudo cp "$project_folder/.env" ./

echo '> Installing NodeJS dependancies ...'
sudo npm install

echo '> Building Project'
sudo npm run build


# Copying the build folder to the apache folder
echo "> Copying build folder to $apache_folder"
sudo cp -r ./dist/ "$apache_folder/blog/"
echo "> Folder copy ok"

sudo chown -R www-data:www-data "$project_folder/blog"
sudo chown -R www-data:www-data "$apache_folder/blog"

# Restart Apache
echo "Restarting Apache service ..."
sudo service apache2 restart

echo "Done, build successful."

source "$project_folder/telegram.sh"

echo "Access your blog at http://blog.rayan.sh"