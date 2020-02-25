# Monster

It's not a game, it's a lifestyle.


## Running via docker

Game db is currently expected at /opt/evmonsterdata.

```
$ docker pull mattmcglincy/evmonster
$ docker run -it --rm -d -p 80:4001 -p 443:4003 -p 4000:4000 -p 4001:4001 -p 4002:4002 -v /opt/evmonsterdata:/opt/evmonsterdata --user $UID:$GID mattmcglincy/evmonster 
```