# **************************************************************************** #
#                                                                              #
#                                                             |\               #
#    dependency_installer.sh                            ------| \----          #
#                                                       |    \`  \  |  p       #
#    By: cshepard6055 <cshepard6055@floridapoly.edu>    |  \`-\   \ |  o       #
#                                                       |---\  \   `|  l       #
#    Created: 2018/05/16 14:51:03 by cshepard6055       | ` .\  \   |  y       #
#    Updated: 2018/05/16 14:51:08 by cshepard6055       -------------          #
#                                                                              #
# **************************************************************************** #

if (whoami != root)
  then echo "Please run as root. Try `sudo bash dependency_installer.sh`"
  exit
fi

# You may need Chromium or Google Chrome if you haven't already installed them
# Python3 and chrome/chromium can be installed on some systems in the following lines

# Uncomment on Ubuntu and some Debian based Linux distributions
# sudo apt-get -y install chromium-browser python3 python3-pip

# Uncomment on Mac OS
# brew cask install google-chrome
# brew install python3

# installs selenium for python3 and chromedriver for selenium
sudo -H pip3 install selenium
wget https://chromedriver.storage.googleapis.com/2.38/chromedriver_linux64.zip -O /tmp/chromedriver.zip
sudo unzip /tmp/chromedriver.zip -d /usr/local/bin
