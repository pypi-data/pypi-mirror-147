# 2022.4.9
import json, time, sys, redis, socket, spacy, os

if not hasattr(spacy, 'nlp'): 
	spacy.nlp		= spacy.load('en_core_web_sm')
	spacy.frombs	= lambda bs: list(spacy.tokens.DocBin().from_bytes(bs).get_docs(spacy.nlp.vocab))[0] if bs else None
	spacy.tobs		= lambda doc: ( doc_bin:= spacy.tokens.DocBin(), doc_bin.add(doc), doc_bin.to_bytes())[-1]

def process(xid, arr): #[['xsnt', [('1583928357124-0', {'snt': 'hello worlds'})]]]
	''' '''
	try:
		snt = arr.get('snt','') 
		bs  = redis.bs.get(f"bs:{snt}")
		if bs is None: redis.bs.set(f"bs:{snt}", spacy.tobs(spacy.nlp(snt)))
		redis.r.expire(f"bs:{snt}", redis.ttl) 
		redis.r.publish('sntbs-is-ready', json.dumps(arr)) # notify bs is parsed ready 
	except Exception as e:
		print ("parse err:", e, arr) 

if __name__ == '__main__':
	init()
	process('101.0', {'snt': 'hello worlds'})
