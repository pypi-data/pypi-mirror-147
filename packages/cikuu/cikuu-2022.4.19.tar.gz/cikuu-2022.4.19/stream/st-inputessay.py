# 2022.4.14
import streamlit as st
import pandas as pd
import time,redis  

now	= lambda: time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))
r	= redis.Redis(host='127.0.0.1', port=6379, decode_responses=True) 

st.sidebar.write( "essay input" + now()) 
rid = st.sidebar.text_input('rid', '230537')
uid = st.sidebar.text_input('uid', '1001')
span = st.sidebar.slider('sleeping seconds', 1, 10, 5)

tid = st.sidebar.text_input('itemid/tid', '7')
label = st.sidebar.text_input('label', 'open the window')
if st.sidebar.button('submit label'): 
	id = r.xadd("xitem", {"rid": rid, "uid": uid, "tid": int(tid), "label": label, "type":"fill"})
	st.sidebar.write( f'submitted score: {id}' ) 

essay = st.text_area('Essay text to submit', "The quick fox jumped over the lazy dog. Justice delayed is justice denied.")
if st.button("submit essay"):
	id = r.xadd("xessay", {"rid": rid, "uid": uid, "essay": essay})
	st.write( f"essay submitted {id}" ) 