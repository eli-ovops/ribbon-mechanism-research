from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError
import json,hashlib,datetime
OUT=Path(__file__).resolve().parent
BASE='https://api.routescan.io/v2/network/mainnet/evm/1/etherscan/api'
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def read(name,params):
 p=OUT/(name+'.original.json');rp=OUT/(name+'.read-receipt.json');assert not p.exists() and not rp.exists()
 u=BASE+'?'+urlencode(params);rec={'url':u,'started_at_utc':now(),'method':'GET','anonymous':True,'cap_bytes':1048576,'timeout_seconds':25}
 try:
  with urlopen(Request(u,headers={'User-Agent':'readonly-public-research'}),timeout=25) as res:
   rec.update(status=res.status,headers=dict(res.headers));raw=res.read(1048577)
   p.write_bytes(raw);rec.update(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),over_cap=len(raw)>1048576)
 except HTTPError as e:
  raw=e.read(1048577);p.write_bytes(raw);rec.update(status=e.code,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),error=str(e))
 except Exception as e:rec.update(status='UNKNOWN',error=type(e).__name__+': '+str(e),body='NOT_OBTAINED')
 rec['finished_at_utc']=now();rp.write_text(json.dumps(rec,indent=2)+'\n')
 print(name,rec.get('status'),rec.get('bytes'),flush=True)
 if rec.get('status')!=200 or rec.get('over_cap'):return None
 try:return json.loads(raw)
 except Exception:return None
def logs(name,address,topic0,lo,hi,page=1,**kw):
 return read(name,dict(module='logs',action='getLogs',address=address,fromBlock=lo,toBlock=hi,page=page,offset=1000,topic0=topic0,**kw))
def receipt(name,tx):return read(name,dict(module='proxy',action='eth_getTransactionReceipt',txhash=tx))
def num(x):return int(x,16) if isinstance(x,str) and x.startswith('0x') else int(x)
def words(l):return [int(l['data'][i:i+64],16) for i in range(2,len(l['data']),64)]
