from pathlib import Path
import json,hashlib,datetime
from passive_original_reader import OUT,num,words,now
OLD=OUT.parents[1]/'ribbon-fixed12-live-ledger-20261017/root'
# Only decode static event fields from previously published ABI descriptors.
DESCRIPTORS=json.loads((OLD/'static-event-descriptors-complete.json').read_text())
BYTOP={x['topic']:x for x in DESCRIPTORS if x.get('topic')}
WETH='0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2';VAULT='0x25751853eab4d0eb3652b5eb6ecb102a2789644b';POOL='0x5934807cc0654d46755ebd2848840b616256c6ef';CTRL='0x4ccc2339f87f6c59c6893e1a678c2266ca58dc72';AUCTION='0x0b7ffc1f4ad541a4ed16b40d8c37f0929158d101';TRANSFER='0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
def ev(l):
 e=BYTOP.get(l['topics'][0]);
 if not e:return None
 ds=[l['data'][i:i+64] for i in range(2,len(l['data']),64)];ti=1;di=0;f={}
 for x in e['inputs']:
  if x['indexed']:v=l['topics'][ti][2:];ti+=1
  else:v=ds[di];di+=1
  typ=x['type']
  if typ=='address':v='0x'+v[-40:]
  elif typ.startswith(('uint','int')):v=int(v,16)
  elif typ=='bool':v=bool(int(v,16))
  elif typ=='bytes':v={'dynamic_offset_only':int(v,16)}
  else:v='0x'+v
  f[x['name']]=v
 return {'event':e['name'],'fields':f,'emitter':l['address'],'tx':l['transactionHash'],'block':num(l['blockNumber']),'log':num(l['logIndex'])}
def rc(path):return json.loads(Path(path).read_text())['result']
def trans(rec,token,fr=None,to=None):
 return [l for l in rec['logs'] if l['address']==token and l['topics'][0]==TRANSFER and (fr is None or l['topics'][1][-40:]==fr[2:]) and(to is None or l['topics'][2][-40:]==to[2:])]
def amt(ls):return sum(int(l['data'],16) for l in ls)
def eid(rec,name):return [e for l in rec['logs'] for e in [ev(l)] if e and e['event']==name]
def save():
 bindings=json.loads((OUT/'selected-receipt-query-bindings.json').read_text())['rows'];sel=json.loads((OUT/'selected-opens-frozen-before-outcomes.json').read_text());owner=[]
 for p in OUT.glob('opyn-owner-events-page*.original.json'):
  d=json.loads(p.read_text());assert isinstance(d['result'],list)
  owner.extend(d['result'])
 owner_dec=[ev(l) for l in owner];unknown=[];rows=[]
 native=[]
 for p in sorted(OUT.glob('indexed-native-vault-window-page*.original.json')):
  d=json.loads(p.read_text());assert isinstance(d['result'],list);native.extend(d['result'])
 for x in bindings:
  i=x['sample_index'];op=rc(x['open_receipt']);ar=rc(OUT/('selected-%02d-auction-settlement-receipt.original.json'%i));cl=rc(OUT/('selected-%02d-close-receipt.original.json'%i));nxt=rc(OUT/('selected-%02d-open-receipt.original.json'%(i+1)))
  m=[e for e in eid(op,'ShortOtokenMinted') if e['fields'].get('otoken')==x['option']];assert len(m)==1;vid=m[0]['fields']['vaultId'];opened=m[0]['fields']['amount'];deps=[e for e in eid(op,'CollateralAssetDeposited') if e['fields']['vaultId']==vid];assert len(deps)==1
  dep=deps[0]['fields']['amount'];ws=trans(op,WETH,VAULT,POOL);assert amt(ws)==dep
  vs=[e for e in eid(cl,'VaultSettled') if e['fields']['oTokenAddress']==x['option'] and e['fields']['vaultId']==vid];assert len(vs)==1;ret=vs[0]['fields']['payout'];assert amt(trans(cl,WETH,POOL,VAULT))==ret
  mids=[]
  for e in owner_dec:
   if e and e['fields'].get('vaultId')==vid and e['emitter']==CTRL and e['event'] in ['CollateralAssetWithdrawed','ShortOtokenBurned','CollateralAssetDeposited','VaultLiquidated'] and (e['block'],e['log'])>(x['block'],m[0]['log']) and(e['block'],e['log'])<(vs[0]['block'],vs[0]['log']):mids.append(e)
  added=sum(e['fields']['amount'] for e in mids if e['event']=='CollateralAssetDeposited');early=sum(e['fields']['amount'] for e in mids if e['event']=='CollateralAssetWithdrawed');burn=sum(e['fields']['amount'] for e in mids if e['event']=='ShortOtokenBurned')
  ac=[e for e in eid(ar,'AuctionCleared') if e['fields']['auctionId']==x['auction_id']];assert len(ac)==1;cash=amt(trans(ar,WETH,AUCTION,VAULT));fields=ac[0]['fields'];sold=fields['soldAuctioningTokens'];bid=fields['soldBiddingTokens'];assert cash==bid
  fees=eid(nxt,'CollectVaultFees');fs=[]
  for e in fees:
   f=e['fields'];matches=[t for t in native if t.get('hash')==e['tx'] and t.get('from')==VAULT and t.get('to')==f['feeRecipient'] and int(t.get('value','0'))==f['vaultFee'] and t.get('isError','0')=='0'];fs.append({'event':e,'actual_native_matching_count':len(matches),'actual_native_matches':matches})
  row=dict(x,opyn_vault_id=vid,collateral_deposit_raw=str(dep),additional_collateral_raw=str(added),early_collateral_withdrawal_raw=str(early),collateral_return_raw=str(ret),collateral_return_plus_early_difference_raw=str(dep+added-ret-early),short_minted_raw=str(opened),short_burned_early_raw=str(burn),auction_sold_raw=str(sold),auction_reported_bid_raw=str(bid),actual_WETH_premium_transfer_raw=str(cash),unsold_return_in_settlement_raw=str(amt(trans(ar,x['option'],AUCTION,VAULT))),intermediate_events=mids,settlement_event=vs[0],next_roll_fee_records=fs,next_roll_fee_event_count=len(fees),three_actual_receipt_gas=[{'hash':z['transactionHash'],'from':z['from'],'gasUsed':num(z['gasUsed']),'effectiveGasPrice':num(z['effectiveGasPrice']),'fee_wei':str(num(z['gasUsed'])*num(z['effectiveGasPrice'])),'status':num(z['status'])} for z in [op,ar,cl]])
  rows.append(row)
 (OUT/'passive-position-correspondence.preliminary.json').write_text(json.dumps({'at_utc':now(),'rows':rows,'owner_returned_logs':len(owner),'native_index_rows':len(native),'method':'Own static descriptor decoding and original token/native comparisons, not source/ABI execution; return difference not yet automatically payout.'},indent=2)+'\n')
 print('ROWS',[(x['sample_index'],x['opyn_vault_id'],x['collateral_return_plus_early_difference_raw'],len(x['intermediate_events']),[f['actual_native_matching_count'] for f in x['next_roll_fee_records']]) for x in rows],flush=True)
if __name__=='__main__':save()
