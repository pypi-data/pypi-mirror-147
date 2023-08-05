# 2022.4.16  nohup uvicorn uvirun:app --host 0.0.0.0 --port 16379 --reload & 
# 2022.4.11  | docker run -p 6379:6379 redislabs/redisearch:latest | https://github.com/RediSearch/redisearch-py
import json,requests,hashlib,os,time,redis,fastapi, uvicorn 
from collections import Counter
from redisearch import Client,Query
import en

app	 = fastapi.FastAPI() 
rhost		= os.getenv("rhost", "172.17.0.1")
rport		= int(os.getenv('rport', 6379))
rdb			= int(os.getenv('rdb', 0))
redis.r		= redis.Redis(host=rhost, port=rport, db=rdb, decode_responses=True) 
redis.bs	= redis.Redis(host=rhost, port=rport, db=rdb, decode_responses=False) 
redis.ttl	= int (os.getenv("ttl", 7200) )
redis.timeout= int (os.getenv("timeout", 3) )
redis.dskhost= os.getenv("dskhost", "172.17.0.1:7095")
now			= lambda: time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))
md5text		= lambda text: hashlib.md5(text.strip().encode("utf-8")).hexdigest()
getdocs		= lambda snts:  [ ( bs := redis.bs.get(f"bs:{snt}"), doc := spacy.frombs(bs) if bs else spacy.nlp(snt))[1] for snt in snts ]
ftsnt		= Client("ftsnt") #__init__(self, index_name, host='localhost', port=6379, conn=None, password=None, decode_responses=True)
ftessay		= Client("ftessay")
md5text		= lambda text: hashlib.md5(text.strip().encode("utf-8")).hexdigest()

@app.get('/stream/init_ft')
def stream_init_ft():
	''' snt=0:rid=100876:uid=1001 tags: simple, compound, complex, ...  to show the first compound sentence on the screen  '''
	redis.r.execute_command("FT.CREATE ftsnt ON HASH PREFIX 1 snt: SCHEMA snt TEXT lems TAG trps TAG kps TAG cates TAG score NUMERIC cola NUMERIC rid TAG uid TAG latest TAG tags TAG borntm NUMERIC SORTABLE") #snt:rid-{rid}:uid-{uid}={snt}
	redis.r.execute_command("FT.CREATE ftessay ON HASH PREFIX 1 essay: SCHEMA rid TAG uid TAG tags TAG latest TAG score NUMERIC borntm NUMERIC SORTABLE") # essay:{xid}
	redis.r.execute_command("FT.CREATE ftitem ON HASH PREFIX 1 item: SCHEMA rid TAG uid TAG tags TAG latest TAG score NUMERIC tid NUMERIC borntm NUMERIC SORTABLE label TAG type TAG") # item:{xid}
	return 'ft index inited'

@app.get('/stream/mock/essay')
def stream_mock_essay(xname:str='xessay', rid:str="230537", span:int=5, loop:int=15, refresh:bool=True):
	''' span is the sleeping time  '''
	from dic import essays 
	if refresh: clear_db(rid) 
	sntslist = [ spacy.snts(d['essay']) for d in essays.essays ]
	for i in range(loop): 
		for d, snts in zip(essays.essays, sntslist):
			d['essay'] =" ".join( snts[0:i+1])
			id = redis.r.xadd(xname, d)
		time.sleep(span)
	return f"finished submitting {loop} times, in every {span} seconds"

@app.get('/stream/clear')
def clear_db(rid:str="230537"):
	''' '''
	[redis.r.delete(k) for k in redis.r.keys(f"snt:rid-{rid}:*")]
	[redis.r.delete(k) for k in redis.r.keys(f"essay:rid-{rid}:*")]
	[redis.r.delete(k) for k in redis.r.keys(f"item:rid-{rid}:*")]
	[redis.r.delete(k) for k in redis.r.keys(f"rid-{rid}:*")]
	[redis.r.xtrim(name,0, False) for name in ('xsnt','xsnts','xessay','xsntgec','xitem')]

@app.get('/stream/mock/fill_score')
def stream_mock_fillscore(xname:str='xitem', rid:str="230537", tid:int=7, loop:int=35):
	'''   '''
	import random
	for i in range(loop): 
		arr={"rid":rid, "uid":int (1000 * random.random()), "tid":tid, "type":"fill", "label": int (100 * random.random())}
		id = redis.r.xadd(xname, arr)
		time.sleep(10 * random.random())
	return f"finished submitting {loop} times"

@app.get('/stream/cmd')
def redis_cmd(cmd:str='zrevrange rid-230537:snt_cola 0 10 withscores'):
	''' FT.SEARCH ftsnt "@rid:{230537} @borntm:[0,2649759864]" limit 0 2 return 1 trps '''
	return redis.r.execute_command(cmd)

@app.get('/')
def home(): return fastapi.responses.HTMLResponse(content=f"<h2>realtime essay api</h2><a href='/docs'> docs </a> | <a href='/redoc'> redoc </a><br>uvicorn uvirun:app --port 80 --host 0.0.0.0 --reload <br><br>last update:2022.4.11")

@app.get('/stream/flushdb')
def stream_flushdb():
	''' snt=0:rid=100876:uid=1001 tags: simple, compound, complex, ...  to show the first compound sentence on the screen  '''
	redis.r.flushdb()
	stream_init_ft()
	#redis.r.execute_command('config set save ""')
	# restart the consumers  http://werror.com:9001/index.html?action=restartall
	return 'flushed'

@app.post('/stream/essay/xadd')
def stream_essay_xadd(arr:dict={"rid":100876, "uid":1001, "tid":0, "type":"essay", "essay":"She has ready. It are ok."}, xname:str="xessay"):  
	''' xadd   {label = text, rid, uid,  tm , snts(json.dumps), tid, type='essay' }   -- xid | xname: xessay/xitem ''' 
	rid,uid,essay	= arr.get('rid', '0'), arr.get('uid', '0'),arr.get('essay','')
	essaymd5		= md5text(essay) 
	latest			= redis.r.hget(f"rid-{rid}:uid_latest", uid) 
	if latest is None or not latest.startswith(essaymd5):  # unless unchanged
		return redis.r.xadd(xname, arr ) #f"xrid-{rid}"

@app.post('/stream/item/xadd')
def stream_item_xadd(arr:dict={"rid":"230537", "uid":"1001", "tid":0, "type":"fill", "label":"open the door"}, xname:str="xitem"):  
	''' 2022.4.14 ''' 
	return redis.r.xadd(xname, arr )

@app.get('/stream/log')
def realtime_log(rid:str="100876", topk:int=20):
	''' snt=0:rid=100876:uid=1001  '''
	return redis.r.zrevrange(f"rid={rid}:zlogs",0, topk, True) 	#arr = redis.r.xinfo_stream(f"xrid-{rid}") 	#lastid = arr['last-generated-id'] 	# got last 10 items , and output 

@app.get('/stream/wordlist')
def realtime_wordlist(rid:str="230537", pos:str='VERB', topk:int=10, maxtm:int=None, maxrow:int=10000):
	''' FT.SEARCH ftsnt '@rid:{100876}'  | snt:rid-100876:uid-1001=Hello world  '''
	if maxtm is None : maxtm = int(time.time())
	#arr = redis.r.execute_command("FT.AGGREGATE ftsnt '@rid:{"+rid+"}' LOAD 1 @lems  APPLY split(@lems) as term GROUPBY 1 @term REDUCE COUNT 0 AS freq")
	si = Counter() 
	q = Query(f"@rid:{{{rid}}} @borntm:[0,{maxtm}]").paging(0, maxrow).return_fields("lems")
	res = ftsnt.search(q)
	[ si.update({ lem.split('_')[-1] : 1}) for doc in res.docs for lem in doc.lems.split(',') if lem.startswith( f"{pos}_") ]
	return si.most_common(topk) 
	#[si.update({tup[1].split('_')[-1]: int(tup[3])}) for tup in arr[1:] if tup[1].startswith(pos) ]

@app.get('/stream/essay/score')
def essay_score(rid:str="230537", maxtm:int=None, maxrow:int=10000):
	''' FT.SEARCH ftessay "@rid:{230537} @borntm:[0,2649759864] @latest:{1}" limit 0 1 return 2 uid score  '''
	if maxtm is None : maxtm = int(time.time())
	#sql = 'FT.SEARCH ftessay "@rid:{230537} @borntm:[0,1649759864]" limit 0 200 return 2 uid score'
	#arr = redis.r.execute_command(sql)
	q = Query(f"@rid:{{{rid}}} @borntm:[0,{maxtm}] @latest:{1}").paging(0, maxrow).return_fields("uid","score")
	res = ftessay.search(q)
	return {doc.uid : float(doc.score) for doc in res.docs} # uid, 1001, score, 76.5 return {tup[1] : float(tup[3]) for tup in arr[1:][1::2]} # uid, 1001, score, 76.5

@app.get('/stream/catelist')
def stream_catelist(rid:str="230537", topk:int=10, maxtm:int=None, maxrow:int=10000, topcate:bool=True):
	''' FT.SEARCH ftsnt "@rid:{230537} @borntm:[0,1649759864]" limit 0 10 return 1 cates  '''
	if maxtm is None : maxtm = int(time.time())
	si = Counter() 
	q = Query(f"@rid:{{{rid}}} @borntm:[0,{maxtm}]").paging(0, maxrow).return_fields("cates")
	res = ftsnt.search(q)
	for doc in res.docs:
		if hasattr(doc,'cates'): # when 'cates' = '' , not in the doc attribute 
			[ si.update({ cate.split('.')[0] if topcate else cate:1}) for cate in doc.cates.split(',') if cate ]
	return si.most_common(topk) 

@app.get('/stream/trplist')
def realtime_trplist(rid:str="230537", rel:str='dobj_VERB_NOUN', topk:int=10, maxtm:int=None, maxrow:int=10000):
	''' FT.SEARCH ftsnt "@borntm:[0,1649759864]" limit 0 10 return 1 trps  '''
	if maxtm is None : maxtm = int(time.time())
	#arr = redis.r.execute_command(f"FT.SEARCH ftsnt '@rid:230537 @borntm:[0,{maxtm}]' limit 0 {maxsnt} return 1 trps ")
	si = Counter() 
	q = Query(f"@rid:{{{rid}}} @borntm:[0,{maxtm}]").paging(0, maxrow).return_fields("trps")
	res = ftsnt.search(q)
	#[ si.update({ trp.split(':')[-1]:1}) for pair in arr[1:][1::2]  for trp in pair[-1].split(',') if trp.startswith(rel) ]
	[ si.update({ trp.split(':')[-1]:1}) for doc in res.docs for trp in doc.trps.split(',') if trp.startswith(rel) ]
	return si.most_common(topk) 

def uvirun(port) : 
	''' python -m uvirun 16379 '''
	uvicorn.run(app, host='0.0.0.0', port=port)

if __name__ == '__main__':
	import fire
	fire.Fire(uvirun)

'''
>> "FT.SEARCH ftsnt '@borntm:[0,{maxtm}]' limit 0 {maxsnt} return 1 trps "
 6588,
  "snt:rid-230537:uid-617925=Last Sunday,the weather was extremely unfavorable and freezing.",
  [
    "trps",
    "amod_PROPN_ADJ:Sunday last,npadvmod_AUX_PROPN:be Sunday,det_NOUN_DET:weather the,nsubj_AUX_NOUN:be weather,ROOT_AUX_AUX:be be,advmod_ADJ_ADV:unfavorable extremely,acomp_AUX_ADJ:be unfavorable,cc_ADJ_CCONJ:unfavorable and,conj_ADJ_ADJ:unfavorable freezing"
  ],
  "snt:rid-230537:uid-617925=I went to my student's home to teach him math in the morning.",
  [
    "trps",
    "nsubj_VERB_PRON:go I,ROOT_VERB_VERB:go go,prep_VERB_ADP:go to,poss_NOUN_PRON:student my,poss_NOUN_NOUN:home student,case_NOUN_PART:student 's,pobj_ADP_NOUN:to home,aux_VERB_PART:teach to,advcl_VERB_VERB:go teach,dative_VERB_PRON:teach he,dobj_VERB_NOUN:teach math,prep_VERB_ADP:teach in,det_NOUN_DET:morning the,pobj_ADP_NOUN:in morning"
  ],

127.0.0.1:6379> dbsize
(integer) 22266

FT.SEARCH ftsnt '@rid:230537 @borntm:[0,2649759864]' limit 0 2 return 1 trps

127.0.0.1:6379> FT.SEARCH ftsnt "@lems:{NOUN_noise} @borntm:[0,1649759864]" limit 0 1
1) (integer) 4

127.0.0.1:6379> FT.SEARCH ftsnt "@rid:{230537} @borntm:[0,1649759864]" limit 0 1
1) (integer) 6588

Searching for books with semantically similar "title" to "Planet Earth", Return top 10 results sorted by distance.
FT.SEARCH books-idx "*=>[KNN 10 @title_embedding $query_vec AS title_score]" PARAMS 2 query_vec <"Planet Earth" embedding BLOB> SORTBY title_score

>>> r.execute_command("FT.AGGREGATE ftsnt '@rid:{100876}' LOAD 1 @lems  APPLY split(@lems) as term GROUPBY 1 @term REDUCE COUNT 0 AS freq")
[4, ['term', 'two', 'freq', '2'], ['term', 'one', 'freq', '2'], ['term', 'three', 'freq', '1'], ['term', 'four', 'freq', '1']]

>>> r.xinfo_stream('xessay')
{'length': 356, 'radix-tree-keys': 203, 'radix-tree-nodes': 401, 'last-generated-id': '1649556821869-1', 'groups': 0, 'first-entry': ('1649556821752-0',

>>> r.execute_command("FT.SEARCH ftsnt '@rid:{100876}'")
[1, 'snt=0', ['rid', '100876', 'snt', 'hello']]

>>> r.execute_command("FT.SEARCH ftsnt '@rid:{100876}'")
[2, 'snt=0', ['rid', '100876', 'snt', 'hello'], 'snt=1', ['rid', '100876', 'snt', 'good']]

redis.r.xrange(f"xrid-{rid}", min=latest_xid, max=latest_xid, count=1).get('label',''):

127.0.0.1:6379> FT.SEARCH ftsnt '@rid:{100876}'
1) (integer) 1
2) "snt=0"
3) 1) "rid"
   2) "100876"
   3) "snt"
   4) "hello"

>>> l = range(10)
>>> l[::2]         # even  - start at the beginning at take every second item
[0, 2, 4, 6, 8]
>>> l[1::2]        # odd - start at second item and take every second item
[1, 3, 5, 7, 9]

FT.AGGREGATE ftsnt '@rid:{230537}' LOAD 1 @lems  APPLY split(@lems) as term GROUPBY 1 @term REDUCE COUNT 0 AS freq
FT.AGGREGATE ftsnt '@rid:{230537}' LOAD 1 @trps  APPLY split(@trps) as term GROUPBY 1 @term REDUCE COUNT 0 AS freq

FT.AGGREGATE ftsnt '@rid:{230537}' LOAD 1 @trps  APPLY split(@trps) as term GROUPBY 1 @term REDUCE COUNT 0 AS freq
startswith(@field, "company")  Return 1 if s2 is the prefix of s1, 0 otherwise.

FT.AGGREGATE ftsnt '@rid:{230537}' LOAD 1 @cates  APPLY split(@cates) as term GROUPBY 1 @term REDUCE COUNT 0 AS freq

https://redis.io/commands/ft.aggregate/
https://redis.io/docs/stack/search/reference/aggregations/
https://redis.com/blog/the-case-for-ephemeral-search/

127.0.0.1:6379> FT.SEARCH ftsnt "@borntm:[0,1649759864]" limit 1 1
1) (integer) 6588

Searching for books with "space" in the title that have "science" in the TAG attribute "categories":
FT.SEARCH books-idx "@title:space @categories:{science}"


FT.search ftsnt '@trps:{dobj_VERB_NOUN\:open door}'
FT.SEARCH idx "@tags:{ hell* }"
FT.SEARCH idx "@tags:{ hello\\ w* }"
FT.SEARCH ftsnt "@trps:{dobj_VERB_NOUN\:open *}"

FT.AGGREGATE ftsnt '@rid:{230537}' LOAD 1 @lems  APPLY startswith(@lems, "VERB_") as ispos GROUPBY 1 @ispos REDUCE COUNT 0 AS freq

FT.CREATE idx SCHEMA name TEXT SORTABLE docid TAG SORTABLE NOINDEX
FT.AGGREGATE idx * GROUPBY 1 @name REDUCE TOLIST 1 @docid as docids
FT.AGGREGATE ftessay * GROUPBY 1 @uid REDUCE TOLIST 1 @rid as docids

FT.AGGREGATE idx * LOAD 1 @__key GROUPBY 1 @type REDUCE TOLIST 1 @__key as keys
FT.AGGREGATE ftessay * LOAD 1 @__key GROUPBY 1 @uid REDUCE TOLIST 1 @__key as keys

FT.AGGREGATE ftsnt * LOAD 1 @__key APPLY split(@lems) as term GROUPBY 1 @term REDUCE TOLIST 1 @__key as keys

FILTER "@name=='foo' && @age < 20"

FT.AGGREGATE ftsnt '@rid:{230537}' LOAD 1 @lems  APPLY split(@lems) as term GROUPBY 1 @term REDUCE COUNT 0 AS freq FILTER "@freq >  2"

FT.AGGREGATE ftsnt '@rid:{230537}' LOAD 1 @lems APPLY split(@lems) as term, startswith(@term, "VERB_") as ispos GROUPBY 2 @term @ispos REDUCE COUNT 0 AS freq

REDUCE FIRST_VALUE {nargs} {property} [BY {property} [ASC|DESC]]

FT.AGGREGATE idx "*" LOAD 1 @location FILTER "exists(@location)" APPLY "geodistance(@location,-117.824722,33.68590)" AS dist SORTBY 2 @dist DESC

https://pypi.org/project/redisearch/

RediSearch 2.4 introduces a new capability, Vector Similarity Search (VSS), which allows indexing and querying vector data stored (as BLOBs) in Redis hashes.
https://github.com/RediSearch/RediSearch/releases?after=v1.99.5

SORTABLE 
NUMERIC
ft.info ftsnt
ft._list
module list 
JSON.SET myDoc $ '{"user":{"name":"John Smith","tag":"foo,bar","hp":1000, "dmg":150}}'
JSON.STRAPPEND myDoc $.user.name '" TOM"'
#kvdic = lambda tup=['term', 'three', 'freq', '1']: dict(zip(tup[::2], tup[1::2])) # {'term': 'three', 'freq': '1'}

127.0.0.1:6379> FT.SEARCH ftessay '@borntm:[0,1649759864]' limit 0 0 return 2 uid score
1) (integer) 356

https://github.com/RediSearch/redisearch-py

>>> ftsnt = Client("ftsnt")

>>> ftsnt.search("@rid:230537 @borntm:[0,2649759864]").total
5076

>>> ftsnt.search("@rid:{230537} @borntm:[0,2649759864]").docs[1].lems
'PRON_there,AUX_be,ADV_so,ADJ_many,ADJ_unforgettable,NOUN_day,ADP_in,PRON_my,NOUN_life'

q = Query("@rid:{230537} @borntm:[0,2649759864]").verbatim().no_content().with_scores().paging(0, 5)
q = Query("@rid:{230537} @borntm:[0,2649759864]").paging(0, 5).return_fields("trps")
res = client.search(q)

paging(offset, num) method of redisearch.query.Query instance
    Set the paging for the query (defaults to 0..10).

return_fields

ftsnt.search("@rid:{230537} @borntm:[0,2649759864]")

127.0.0.1:6379> ft.search ftessay "@uid:{913292}" limit 0 0
1) (integer) 15
127.0.0.1:6379> ft.search ftessay "@uid:{913292} @latest:{1}" limit 0 0
1) (integer) 1


127.0.0.1:6379> ft.search ftessay "@uid:{913292} @latest:{1}" limit 0 0
1) (integer) 1
127.0.0.1:6379> ft.search ftessay "@rid:{230537} @latest:{1}" limit 0 0
1) (integer) 356

127.0.0.1:6379> ft.search ftessay "@rid:{230537} @latest:{1} @score:[80,100]" limit 0 1 return 2 uid score
1) (integer) 0


'''