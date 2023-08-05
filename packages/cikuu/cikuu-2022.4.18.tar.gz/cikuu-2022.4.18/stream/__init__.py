#2022.4.16  xstream consumers 
# docker run --name redis --restart=always -d -p 172.17.0.1:6379:6379 -v $PWD/redis-data:/data redis redis-server --notify-keyspace-events KEA --save ""  --appendonly no
# docker run -d --name redis -p 172.17.0.1:6379:6379 redislabs/redisearch:2.4.3
# docker run -d --restart=always --name=webdis --env=REDIS_HOST=172.17.0.1 --env=REDIS_PORT=6379 -e VIRTUAL_PORT=7379 -p 7379:7379 wrask/webdis
# docker run -d --rm --name redisUI -e REDIS_1_HOST=172.17.0.1 -e REDIS_1_NAME=rft -e REDIS_1_PORT=6379 -p 26379:80 erikdubbelboer/phpredisadmin:v1.13.2
# cola, move redis consumer insider
# docker swarm , start multiple instance, without using supervisor
# python -m stream 

def xconsume(streams:tuple, group:str='group1',  host='172.17.0.1', port=6379, db=0, waitms=3600000, ttl=7200, precount=1,debug=False
			, dskhost:str="172.17.0.1:7095" ): #, func=lambda item: print(item)
	''' python -m stream xsnt,xsnts --group gecv1 '''
	import json,os,time,redis, socket
	now	= lambda: time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))

	assert hasattr(redis, 'func') 
	redis.r		= redis.Redis(host=host, port=port, db=db, decode_responses=True) 
	redis.bs	= redis.Redis(host=host, port=port, db=db, decode_responses=False) 
	redis.ttl	= ttl 
	redis.debug = debug
	redis.dskhost= dskhost	
	redis.funcs	= [eval(code) for fname, code in redis.r.hgetall(f"config:code:{group}")]  # lambda: xid, xarr = 

	if isinstance(streams, str) : streams = [streams.strip()] #	streams = [stream_name for stream_name in streams if isinstance(streams, tuple) else [streams.strip()] ]
	for stream_name in streams:
		try:
			redis.r.xgroup_create(stream_name, group,  mkstream=True)
		except Exception as e:
			print(e)

	consumer_name = f'consumer_{socket.gethostname()}_{os.getpid()}'
	print(f"Started: {consumer_name}|{streams}|{group}| ", redis.r, now(), flush=True)
	while True:
		item = redis.r.xreadgroup(group, consumer_name, {stream_name: '>' for stream_name in streams}, count=precount, noack=True, block= waitms )
		try:
			if not item: break
			if redis.debug: print("xmessage:\t", item, "\t", now(), flush=True) 
			redis.func(item)  #[['_new_snt', [('1583928357124-0', {'snt': 'hello worlds'})]]]
		except Exception as e:
			print(">>[stream]", e, "\t|", item)

	[redis.r.xgroup_delconsumer(stream_name, group, consumer_name) for stream_name in streams ]
	redis.r.close()
	print ("Quitted:", consumer_name, "\t",now())

if __name__ == '__main__':
	import fire
	fire.Fire(xconsume)