#2022.4.17  python -m stream xsnts todsk 
from stream import * 

def getgecs(snts, host="gpu120.wrask.com", port=6379, timeout=5): # put into the ufw white ip list 
	''' '''
	if not hasattr(getgecs, 'r'): getgecs.r = redis.Redis(host=host,port=port, decode_responses=True)
	if not snts : return {}
	id  = getgecs.r.xadd("xsnts", {"snts":json.dumps(snts)})
	res	= getgecs.r.blpop([f"suc:{id}",f"err:{id}"], timeout=timeout)
	return {} if res is None else json.loads(res[1])

def process(xid, arr:dict={"rid":100876, "uid":1001, "tid":0, "snts":'["She has ready.", "It are ok."]'}): 
	''' 2022.4.11 '''
	from dsk import mkf
	snts	= json.loads(arr['snts']) if 'snts' in arr else spacy.snts(arr.get('essay','')) # latter is reserved for penly (direct submit)
	gecs	= redis.r.mget( [f"gec:{snt}" for snt in snts])
	newsnts = [snt for snt, gec in zip(snts, gecs) if gec is None ]
	sntdic  = getgecs(newsnts) 
	[ redis.r.setex(f"gec:{snt}", redis.ttl, gec) for snt, gec in sntdic.items()]

	rid,uid	= arr.get('rid','0'),  arr.get('uid','0')
	sntgecs = [ (snt,gec if gec else sntdic.get(snt,snt)) for snt, gec in zip(snts, gecs)]
	dsk	 = mkf.sntsmkf( sntgecs , dskhost=redis.dskhost, asdsk=True, getdoc= lambda snt: ( bs := redis.bs.get(f"bs:{snt}"), doc := spacy.frombs(bs) if bs else spacy.nlp(snt))[1] ) if sntgecs else {}
	redis.r.setex(f"dskstr:{xid}", redis.ttl, json.dumps(dsk)) 
	redis.r.lpush(f"dsk:{xid}", json.dumps(dsk))  # prepared for blpop
	redis.r.expire(f"dsk:{xid}", redis.ttl)

	score = float(dsk.get('info',{}).get("final_score",0))
	redis.r.hset(f"essay:rid-{rid}:{xid}", "score", score , dsk.get('doc',{}) ) # awl, ast, .. 
	redis.r.zadd(f"rid-{rid}:essay_score", {uid: score} ) # overwriting 
	redis.r.zadd(f"rid-{rid}:essay_wordnum", {uid: int(dsk.get('doc',{}).get("word_num",0))} ) # verbose data for chart , use ftessay.search later ? 
	# FT.SEARCH ftessay "@rid:{230537}  @latest:{1}" limit 0 2 return 3 uid borntm word_num
	mpubarr({"name": "essay_score", "rid":rid, "data": redis.r.zrevrange(f"rid-{rid}:essay_score", 0 , 20, True)})
	mpubarr({"name": "essay_wordnum","rid":rid, "data": redis.r.zrevrange(f"rid-{rid}:essay_wordnum", 0 , 20, True)})
	if redis.debug: print ( "dsk word_num:", int(dsk.get('doc',{}).get("word_num",0)), flush=True)

	for mkf in dsk.get('snt',[]):  #for snt, mkf in sntgec_mkfs(sntgec, arr):
		snt = mkf.get('meta',{}).get('snt','')
		redis.r.setex(f"mkf:{snt}", redis.ttl, json.dumps(mkf))
		if not redis.r.hexists(f"snt:rid-{rid}:uid-{uid}={snt}", "cates"):
			cates = [ v['cate'][2:] for k,v in mkf.get('feedback',{}).items() if v['cate'].startswith("e_") or v['cate'].startswith("w_") ]
			redis.r.hset(f"snt:rid-{rid}:uid-{uid}={snt}", "cates", ','.join(cates))
			for cate in cates: 
				redis.r.zincrby(f"rid-{rid}:cate", 1, cate) # snt.nv_agree
				redis.r.zincrby(f"rid-{rid}:catetop", 1, cate.split('.')[0]) # snt
				mpubarr({"name": "catetop", "rid":rid, "data": redis.r.zrevrange(f"rid-{rid}:catetop", 0 , 20, True)})

	#if redis.debug: print ( "dsk:", dsk, flush=True) 
	return dsk

if __name__ == '__main__':
	print ( "gpu120 result:", getgecs(["She has ready.", "It are ok."]))
	init()
	#print ( process('1583928357123-0') ) 
	dsk = process('1583928357124-0', {"rid":"100876", "uid":"penzz", "tid":0, "essay":"She has ready. It are ok."})
	print ('dsk:', dsk ) 