#!/bin/bash

# /var/www/html  must have www-data ownership
# VITE_API_URL=http://127.0.0.1:8000/core
# VITE_API_URL_PROD=http://194.135.81.27/core

# Visudo
# www-data ALL=(ALL) NOPASSWD: /bin/rm -r /var/www/html/Blog.rayan.sh
# www-data ALL=(ALL) NOPASSWD: /bin/rm -r /var/www/html/blog_latest
# www-data ALL=(ALL) NOPASSWD: /usr/sbin/service apache2 restart
# www-data ALL=(ALL) NOPASSWD: /bin/rm -r /var/www/html/blog/backend/static
# www-data ALL=(ALL) NOPASSWD: /usr/bin/npm install
# www-data ALL=(ALL) NOPASSWD: /usr/bin/npm run build


# Stop if an error occurs
set -e

cd /var/www/html/
echo "Current pwd: $(pwd)"

# First delete blog_latest and Blog.rayan.sh folders if they exists
blog_latest="/var/www/html/blog_latest"
git_cloned="/var/www/html/Blog.rayan.sh"

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
    echo "git_cloned= does not exist."
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


# Trailing slash after source directory to copy the content of the folder
# and not the folder itself
echo "> Copying folder to /var/www/html"
rsync -av --exclude='.git/' ./blog_latest/ ./blog/
echo "> Folder copy ok"

## Do not forget we are already in /var/www/html folder
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



static_folder="/var/www/html/blog/backend/static"

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


cd /var/www/html/blog/frontend

echo '> Installing NodeJS dependancies ...'
sudo npm install

echo '> Building Project'
sudo npm run build


# Restart Apache
echo "Restarting Apache service ..."
#sudo service apache2 restart

echo "Done, build successful."

source /var/www/html/blog/telegram_message.sh