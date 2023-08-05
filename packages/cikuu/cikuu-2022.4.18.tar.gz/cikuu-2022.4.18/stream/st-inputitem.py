# 2022.4.14
import streamlit as st
import time,redis  

now	= lambda: time.strftime('%Y.%m.%d %H:%M:%S',time.localtime(time.time()))
r	= redis.Redis(host='127.0.0.1', port=6379, decode_responses=True) 

st.sidebar.write( "essay input" + now()) 
rid = st.sidebar.text_input('rid', '230537')
uid = st.sidebar.text_input('uid', '牛魔王')
tid = st.sidebar.slider('itemid/tid', 0, 25, 7) 
label = st.sidebar.text_input('label/score', 'open the door')

if st.sidebar.button('submit'): 
	id = r.xadd("xitem", {"rid": rid, "uid": uid, "tid": int(tid), "label": label, "type":"fill"})
	st.sidebar.subheader( id ) 

xid = st.text_input('xadded xid', '')
if st.button('search xid'): 	
	st.write(f"item:{xid}  | {now()}")
	st.write( r.hgetall(f"item:{xid}") ) 
	st.write(f"rid-{rid}:uid-{uid}:tid_label")
	st.write( r.hgetall(f"rid-{rid}:uid-{uid}:tid_label") ) 
	st.write(f"rid-{rid}:tid-{tid}:uid_label")
	st.write( r.hgetall(f"rid-{rid}:tid-{tid}:uid_label") ) 