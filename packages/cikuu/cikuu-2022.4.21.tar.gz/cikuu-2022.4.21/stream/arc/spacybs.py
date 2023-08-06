# 2022.4.9
import json, time, sys, redis, socket, spacy, os

if not hasattr(spacy, 'nlp'): 
	spacy.nlp		= spacy.load('en_core_web_sm')
	spacy.frombs	= lambda bs: list(spacy.tokens.DocBin().from_bytes(bs).get_docs(spacy.nlp.vocab))[0] if bs else None
	spacy.tobs		= lambda doc: ( doc_bin:= spacy.tokens.DocBin(), doc_bin.add(doc), doc_bin.to_bytes())[-1]

def process(item): #[['xsnt', [('1583928357124-0', {'snt': 'hello worlds'})]]]
	''' '''
	for stm_arr in item : #[['xsnt', [('1583928357124-0', {'snt': 'hello worlds'})]]]
		if stm_arr[0].startswith('xsnt'): # xsnt, xsntspacy
			for id,arr in stm_arr[1]: 
				try:
					snt = arr.get('snt','') 
					bs  = redis.bs.get(f"bs:{snt}")
					if bs is None: redis.bs.set(f"bs:{snt}", spacy.tobs(spacy.nlp(snt)))
					redis.r.expire(f"bs:{snt}", redis.ttl) 
				except Exception as e:
					print ("parse err:", e, arr) 

if __name__ == '__main__':
	redis.r		= redis.Redis(decode_responses=True) 
	redis.bs	= redis.Redis(decode_responses=False) 
	redis.ttl	= 7200
	process([['xsnt', [('1583928357124-0', {'snt': 'hello worlds'})]]])
