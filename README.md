# barrage
Some quick and dirty barrage tool
1. This thing run on mac and linux (only due to docker mount in docker-compose)
2. you need to have docker and docker-compose installed
3. pull k6 to have it `docker pull grafana/k6` it used to generate load
4. Clone repo and run `docker-compose up -d` it will build all required things
5. open http://127.0.0.1:8000 and go to settings (gear icon)
6. There are 2 weird fields to be filled: 
   1. IP - which is whatever your IP on host (like 192.168.x.x)
   2. location - which is absolute path to reports folder in git repo (whenever you put in on your machine) 

Everything else in quite intuitive (i guess) at the end of the day it is only 3 containers with python UI (it is not uwsgi) Grafana and Influx.

UI sends url to barrage into python back, it launches k6 with required params, then k6 reports to influx, grafana in iframes show the results on UI.

Recurring jobs (like health stans for URL and constant barrage of healthy URLs) done in browser with JS and setInterval, so while browser is open it will barrage

When recurring job for barraging executed you can change vUsers with no harm, but Time to run is better not be touched w/o stopping of that job, it used to set internal for barraging (just click on spinning gear)
