#2022.4.16  xstream consumers 
# docker run --name redis --restart=always -d -p 172.17.0.1:6379:6379 -v $PWD/redis-data:/data redis redis-server --notify-keyspace-events KEA --save ""  --appendonly no
# docker run -d --name redis -p 172.17.0.1:6379:6379 redislabs/redisearch:2.4.3
# docker run -d --name redis -p 172.17.0.1:6379:6379 redislabs/redismod
# docker run -d --restart=always --name=webdis --env=REDIS_HOST=172.17.0.1 --env=REDIS_PORT=6379 -e VIRTUAL_PORT=7379 -p 7379:7379 wrask/webdis
# docker run -d --rm --name redisUI -e REDIS_1_HOST=172.17.0.1 -e REDIS_1_NAME=rft -e REDIS_1_PORT=6379 -p 26379:80 erikdubbelboer/phpredisadmin:v1.13.2
# cola, move redis consumer insider
# docker swarm , start multiple instance, without using supervisor
# python -m stream 
import json,os,time,redis, socket,requests,en, hashlib,traceback,sys
md5text	= lambda text: hashlib.md5(text.strip().encode("utf-8")).hexdigest()
getdoc	= lambda snt:  ( bs := redis.bs.get(f"bs:{snt}"), doc := spacy.frombs(bs) if bs else spacy.nlp(snt), redis.bs.setex(f"bs:{snt}", redis.ttl, spacy.tobs(doc)) if bs is None else None )[1]

def init(): # for debug only 
	import platform
	redis.ttl	= 7200
	redis.debug = True
	redis.dskhost= "gpu120.wrask.com:7095"

	if platform.system().lower() == 'windows':
		redis.r		= redis.Redis(decode_responses=True) 
		redis.bs	= redis.Redis(decode_responses=False) 
	else: 
		redis.r		= redis.Redis("172.17.0.1", decode_responses=True) 
		redis.bs	= redis.Redis("172.17.0.1", decode_responses=False) 

if __name__ == '__main__':
	init()