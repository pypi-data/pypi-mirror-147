#2022.4.17  python -m stream xitem item
from stream import * 

def process(xid, arr:dict={"rid":"230537", "uid":'1001', "tid":0, "type":"fill", "label":"open the door"}): 
	'''  ''' 
	rid,uid,tid,label	= arr.get('rid', '0'), arr.get('uid', '0'),arr.get('tid','0'),arr.get('label','')
	borntm			= float( int(xid.split('-')[0])/1000 )
	xidlatest		= redis.r.hget(f"rid-{rid}:xid_latest", f"{uid},{tid}") 
	if xidlatest: redis.r.hset(f"item:{xidlatest}", "latest", 0) # only one is marked as 'latest' 
	redis.r.hset(f"rid-{rid}:xid_latest", f"{uid},{tid}", xid)

	score = redis.r.hget(f"rid-{rid}:tid-{tid}", label)
	if score is None: score = 0

	arr.update({'borntm':borntm, 'latest':1, "score": float(score)})
	redis.r.hset(f"item:{xid}", "borntm", borntm, arr )  # mirror data of the xitem 
	redis.r.zadd(f"rid-{rid}:zlogs", {json.dumps(arr): borntm}) 
	# cache , for a quicker show 
	redis.r.hset(f"rid-{rid}:uid-{uid}:tid_label", tid,  label )
	redis.r.hset(f"rid-{rid}:tid-{tid}:uid_label", uid,  label )

def test():
	init()
	process('1583928357124-0')
	assert redis.r.hgetall("rid-230537:uid-1001:tid_label")
	assert redis.r.hgetall("rid-230537:tid-0:uid_label")

if __name__ == '__main__':
	init()
	process('1583928357124-0')
	print(redis.r.hgetall("rid-230537:uid-1001:tid_label"))
	print(redis.r.hgetall("rid-230537:tid-0:uid_label"))
