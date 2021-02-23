# MA Immunization COVID-19 Vaccines sites watcher

### Why?

The MA Immunization website is simply horrible 🤦🏻‍♂️. 

The other websites that aggregate infos are OK, but they need to be refreshed 🤯.

This project uses command line 🚀, makes a request every few seconds ⏰ and prints direct links in the terminal 🐚.

Right now it supports the few locations closer to Boston: others can be added in `urls.py`. 

### Requirements 🛒
Python 3 (2 is dead) is the only requirement.
If you are not sure which python you are running, then try running 
```shell
> python --version
```
If it says something like `2.7` you are probably running the system python. 
In this case you will probably have also a `python3` and a `pip3` available, 
but you might need to run `pip3` them as superuser.

### How to use 🔧
```shell
> git clone https://github.com/giocalitri/maimmunization_watcher.git
> cd maimmunization_watcher
> pip install -r requirements.txt
> python watch_site.py
```

#### Notes ⚠️
- Remember to stop the script when not using it. There is throttling implemented, but you do not want your IP to get banned for running it for days straight!