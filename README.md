# Auto-Registrar
*Auto-Registrar* is designed to help university students with the unofficial registration process. <br />

# Installation and Excecution (*NIX systems)
1) Install prerequisites (per client system)
```
# Debian based distributions
sudo apt-get -y install python3 python3-pip chromium-browser
# Homebrew
brew cask install google-chrome
brew install python3
brew cask install chromedriver
```
2) Download repository
```
git clone https://github.com/Caleb-Shepard/auto-registrar
```
3) Run dependency_installer.sh
```
# Installs selenium and chromedriver
cd auto-registrar
chmod +x dependency_installer.sh
sudo bash dependency_installer.sh
```
4) Run the program
```
# starts chromedriver and begins execution of the program
python3 auto_registrar.py
```

# Prerequisites
* [Python3](https://www.python.org/downloads/) <br />
* [Google Chrome](https://www.python.org/downloads/) <br />
* [Chromium Browser](https://download-chromium.appspot.com/) (A suitable open source alternative to Google Chrome) <br />

# Authors
[Caleb Shepard](https://github.com/Caleb-Shepard) <br />
[Matt Giallourakis](https://github.com/foldsters) <br />
[Elijah Luckey](https://github.com/Luckey-Elijah) <br />
[Jeremy Eudy](https://github.com/JeremyEudy) <br />
[Mihir Lad](https://github.com/mihirlad55) <br />
[Jason Chua](https://github.com/rebel1804) <br />
[Tiger Sachse](https://github.com/tgsachse)

# License
[MIT License](LICENSE)
