# 2022.4.13
import streamlit as st
import pandas as pd
import time,redis, requests  

now	= lambda: time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))
r	= redis.Redis(host='172.17.0.1', port=6379, decode_responses=True) 

st.set_page_config(layout="wide")
st.sidebar.write( "dashboard started:" + now()) 
rid = st.sidebar.text_input('rid', '230537')
span = st.sidebar.slider('sleeping seconds', 1, 10, 5)
col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)
area_1 = col1.empty()
area_2 = col2.empty()  
area_3 = col3.empty()
area_4 = col4.empty()  
area_5 = col5.empty()  
area_6 = col6.empty()  

while True:  #pd.read_csv("my_data.csv") # load csv
	area_1.write( {"now":now(),  "snt_num": r.zcard('rid-230537:snt_cola')
	, "word_num":r.zcard('rid-230537:word_idf') 
	, "user_cnt": r.hlen(f"rid-{rid}:uid_latest")
	, 'xessay_len':r.xlen('xessay')
	, 'essay_score':r.zcard(f'rid-{rid}:essay_score')
	, 'xsnt_len':r.xlen('xsnt')
	, 'xsnts_len':r.xlen('xsnts')
	, 'cate':r.zcard(f'rid-{rid}:cate')
	, 'catetop':r.zcard(f'rid-{rid}:catetop')
	})
	
	area_2.write( dict(r.zrevrange(f'rid-{rid}:essay_score',0,10, True))  ) 
	area_3.write( dict(r.zrevrange(f'rid-{rid}:cate',0,10, True))  ) 
	area_4.write( dict(r.zrevrange(f'rid-{rid}:word_idf',0,10, True)) )  # VERB,ADJ
	area_5.write( {uact: time.strftime('%H:%M:%S',time.localtime(tm/1000)) for uact,tm in r.zrevrange(f'rid-{rid}:zlogs',0,10, True) } ) 
	area_6.write( dict(r.zrevrange(f'rid-{rid}:snt_cola',0,3, True))  ) 
	time.sleep(span) 