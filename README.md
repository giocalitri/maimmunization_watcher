# MA Immunization COVID-19 Vaccines sites watcher

### Why?

The MA Immunization website is simply horrible. 

The other websites that aggregate infos are OK, but they need to be refreshed.

This project uses command line 🚀, makes a request every few seconds ⏰ and prints direct links in the terminal 🐚.

Right now it supports the few locations closer to Boston: others can be added in `urls.py`. 

### How to use 🔧
```shell
> git clone https://github.com/giocalitri/maimmunization_watcher.git
> cd maimmunization_watcher
> pip install -r requirements.txt
> python watch_site.py
```

#### Note ⚠️
Remember to stop the script when not using it. 
There is throttling implemented, but you do not want your IP to get banned for running it for days straight!