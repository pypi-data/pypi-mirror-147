# https://ron.sh/creating-real-time-charts-with-fastapi/ 
# client: https://ron.sh/creating-real-time-charts-with-flask/
import json,sys
from datetime import datetime
from typing import Iterator
import asyncio, uvicorn, redis
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates

application = FastAPI()
templates = Jinja2Templates(directory="templates")
application.mount("/static", StaticFiles(directory="static"), name="static")

@application.get("/", response_class=HTMLResponse)
async def index(request: Request) -> templates.TemplateResponse:
    return templates.TemplateResponse("index.html", {"request": request})

redis.r = redis.Redis(host='172.17.0.1', port=6379, db=0, decode_responses=True)
zsum	= lambda key='rid-230537:essay_wordnum',ibeg=0, iend=-1: sum([v for k,v in redis.r.zrevrange(key, ibeg, iend, True)])
print (redis.r) 

async def generate_score(request: Request) -> Iterator[str]:
    rid = int(request.query_params.get('rid','230537'))
    while True:
        scores  = [ score for uid, score in redis.r.zrevrange(f"rid-{rid}:essay_score", 0, -1, True) ]
        json_data = json.dumps(
            {
                "time": datetime.now().strftime("%H:%M:%S"),
				"value": sum(scores) / len(scores),
				"max": scores[0],
                "min": scores[-1],
            }
        )
        yield f"data:{json_data}\n\n"
        await asyncio.sleep(2)

@application.get("/chart-data")
async def chart_data(request: Request) -> StreamingResponse:
    response = StreamingResponse(generate_score(request), media_type="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response

@application.get("/essay-score")
async def essay_score(request: Request) -> StreamingResponse:
	async def generate_score(request: Request) -> Iterator[str]:
		rid = int(request.query_params.get('rid','230537'))
		while True:
			scores  = [ score for uid, score in redis.r.zrevrange(f"rid-{rid}:essay_score", 0, -1, True) ]
			json_data = json.dumps(
				{
					"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), #%Y-%m-%d 
					"value": sum(scores) / len(scores),
					"max": scores[0],
					"min": scores[-1],
				}
			)
			yield f"data:{json_data}\n\n"
			await asyncio.sleep(2)

	return StreamingResponse(generate_score(request), media_type="text/event-stream", headers={"Cache-Control": "no-cache","X-Accel-Buffering": "no"})

@application.get("/rid-stats")
async def rid_stats(request: Request) -> StreamingResponse:
	async def generate_rid_stats(request: Request) -> Iterator[str]:
		rid = int(request.query_params.get('rid','230537'))
		span = int(request.query_params.get('span','3'))
		while True:
			scores  = [ score for uid, score in redis.r.zrevrange(f"rid-{rid}:essay_score", 0, -1, True) ]
			json_data = json.dumps(
				{
					"time": datetime.now().strftime("%H:%M:%S"),
					"errorsum": zsum(f"rid-{rid}:cate"), 
					"wordsum":  zsum(f"rid-{rid}:essay_wordnum"), 
					"essaysum": redis.r.zcard(f"rid-{rid}:essay_score"), 
					"sntsum": redis.r.zcard(f"rid-{rid}:snt_cola"),
				}
			)
			yield f"data:{json_data}\n\n"
			await asyncio.sleep(span)

	return StreamingResponse(generate_rid_stats(request), media_type="text/event-stream", headers={"Cache-Control": "no-cache","X-Accel-Buffering": "no"})

@application.get("/zrevrange")
async def sse_zrevrange(request: Request) -> StreamingResponse:
	async def zget(request: Request) -> Iterator[str]:
		rid = int(request.query_params.get('rid','230537'))
		name = request.query_params.get('name','catetop').strip('"')
		ibeg = int(request.query_params.get('ibeg','0'))
		iend = int(request.query_params.get('iend','-1'))
		span = int(request.query_params.get('span','3'))
		while True:
			data  =  redis.r.zrevrange(f"rid-{rid}:{name}", ibeg, iend, True) 
			json_data = json.dumps({"rid": rid, "name": name, "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "data": data})
			yield f"data:{json_data}\n\n"
			await asyncio.sleep(span)
	return StreamingResponse(zget(request), media_type="text/event-stream", headers={"Cache-Control": "no-cache","X-Accel-Buffering": "no"})

if __name__ == '__main__':
    uvicorn.run(application, host='0.0.0.0', port=8000)
