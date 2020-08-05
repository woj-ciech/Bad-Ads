# Bad Ads
Monitor advertisements on Bedpage


Details & Usage & Methodology & Findings described in below article

https://www.offensiveosint.io/offensive-osint-s02e02-human-trafficking-investigation-part-2-monitoring-bedpage/

![](https://www.offensiveosint.io/content/images/size/w1600/2020/07/dashboard.png)

![](https://www.offensiveosint.io/content/images/size/w1600/2020/08/search.png)

![](https://www.offensiveosint.io/content/images/size/w1600/2020/08/people.png)

```buildoutcfg
sudo pip3 install -r requirements.txt
```

In root directory
```buildoutcfg
sudo python3 manage.py makemigrations
sudo python3 manage.py migrate
sudo python3 manage.py runserver
```

In root directory
```buildoutcfg
sudo celery worker -A bpscanner --loglevel=debug
```

In new window
```
sudo apt-get install redis
sudo redis-server
```

## Additional
- copy cookie and paste it in tasks.py
- keep bedpage tab open
- Template by Creative Tim - https://www.creative-tim.com/product/material-dashboard-dark
