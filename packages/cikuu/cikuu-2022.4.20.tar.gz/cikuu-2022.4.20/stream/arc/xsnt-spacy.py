# 2022.4.16 python -m stream.xsnt-spacy xsnt --group spacy
import json, time, sys, redis, spacy
if not hasattr(spacy, 'nlp'): 
	spacy.nlp		= spacy.load('en_core_web_sm') # 3.1.1
	spacy.frombs	= lambda bs: list(spacy.tokens.DocBin().from_bytes(bs).get_docs(spacy.nlp.vocab))[0] if bs else None
	spacy.tobs		= lambda doc: ( doc_bin:= spacy.tokens.DocBin(), doc_bin.add(doc), doc_bin.to_bytes())[-1]

def process(item): #[['xsnt', [('1583928357124-0', {'snt': 'hello worlds'})]]]
	''' 2022.4.10 '''
	for stm_arr in item : #[['xsnt', [('1583928357124-0', {'snt': 'hello worlds'})]]]
		if stm_arr[0].startswith('xsnt'): # xsnt, xsntspacy
			for id,arr in stm_arr[1]: 
				try:
					snt = arr.get('snt','') 
					bs  = redis.bs.get(f"bs:{snt}")
					if bs is None: 
						doc = spacy.nlp(snt)
						redis.bs.setex(f"bs:{snt}", redis.ttl, spacy.tobs(doc))

						if redis.funcs: # config:code:spacy  -> lambda: xid, xarr
							arr['doc'] = doc 
							for f in redis.funcs : 
								try: 
									f(id, arr) 
								except Exception as e0:
									print ('f ex:', e0)
					else:
						r.expire(f"bs:{snt}", redis.ttl) 
				except Exception as e:
					print ("xsnt-spacy err:", e, id, arr) 

from stream import xconsume 
redis.func = process

if __name__ == '__main__':
	import fire
	fire.Fire(xconsume)
