# !/bin/bash

# /var/www/html  must have www-data ownership

# Visudo
# www-data ALL=(ALL) NOPASSWD: /bin/rm -r /var/www/html/Blog.rayan.sh
# www-data ALL=(ALL) NOPASSWD: /bin/rm -r /var/www/html/blog_latest

# Stop if an error occurs
set -e

cd /var/www/html/

echo "Current pwd: $(pwd)"

# First delete blog_latest and Blog.rayan.sh folders if they exists
blog_latest="/var/www/blog_latest"
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
    rm -r "$git_cloned"
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
echo 'migrations ok'
