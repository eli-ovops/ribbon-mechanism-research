from pathlib import Path
import json,hashlib,datetime
B=Path('/Volumes/EXTERNAL/亚力克斯 /运行验证-20261015/evidence/ribbon-fixed12-live-ledger-20261017');R=B/'root';O=B/'protocol';inputs={}
def read(n):
 p=R/n;z=p.read_bytes();inputs[str(p)]={'sha256':hashlib.sha256(z).hexdigest(),'bytes':len(z)};return z
def j(n):return json.loads(read(n))
ledger=j('fixed12-actual-cashflow-ledger.json');desc=j('static-event-descriptors-complete.json');MP={a['topic']:a for a in desc}
VA='0x25751853eab4d0eb3652b5eb6ecb102a2789644b';W='0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2'
def word(b,i):return b[i*32:(i+1)*32]
def uint(b,i):return int.from_bytes(word(b,i),'big')
def val(w,t):
 if t=='address':return '0x'+w[-20:].hex()
 if t=='bool':
  assert int.from_bytes(w,'big') in (0,1);return bool(int.from_bytes(w,'big'))
 if t.startswith('uint'):
  n=int.from_bytes(w,'big');bits=int(t[4:] or '256');assert n<2**bits;return n
 if t=='bytes32':return '0x'+w.hex()
 raise ValueError(t)
def decode(l):
 d=MP.get(l['topics'][0])
 if not d:return None
 b=bytes.fromhex(l['data'][2:]);args={};ii=1;di=0
 assert len(l['topics'])==1+sum(a['indexed'] for a in d['inputs'])
 for a in d['inputs']:
  if a['indexed']:v=bytes.fromhex(l['topics'][ii][2:]);ii+=1
  else:v=word(b,di);di+=1
  assert len(v)==32
  if a['type']=='bytes' and not a['indexed']:
   off=int.from_bytes(v,'big');assert off%32==0 and off+32<=len(b);sz=int.from_bytes(b[off:off+32],'big');assert off+32+sz<=len(b);args[a['name']]='0x'+b[off+32:off+32+sz].hex()
  else:args[a['name']]=val(v,a['type'])
 return {'event':d['name'],'args':args,'emitter':l['address'],'log_index':int(l['logIndex'],16)}
receipts={};gas={};byfile={}
for n in sorted(R.glob('round*-receipt.original.txt')):
 rec=j(n.name)['result'];assert rec['status']=='0x1'
 assert all(z['transactionHash']==rec['transactionHash'] and z['blockHash']==rec['blockHash'] and z['blockNumber']==rec['blockNumber'] for z in rec['logs'])
 assert len({int(z['logIndex'],16) for z in rec['logs']})==len(rec['logs'])
 receipts[rec['transactionHash']]=rec;byfile[n.name]=rec
 gas[rec['transactionHash']]=int(rec['gasUsed'],16)*int(rec['effectiveGasPrice'],16)
def ev(rec,name,emitter=None):
 return [d for l in rec['logs'] for d in [decode(l)] if d and d['event']==name and (emitter is None or d['emitter']==emitter)]
def transfers(rec,token,fr=None,to=None):
 return [d for d in ev(rec,'Transfer',token) if (fr is None or d['args']['from']==fr) and (to is None or d['args']['to']==to)]
def getrec(tx):return receipts[tx]
native=j('indexed-native-transfers-combined.json')['records']
normal=j('normal-transactions-combined.json')['records']
factory=j('factory-eth-call-creation-events-page1.original.txt');opyn=j('opyn-all-vault-owner-events.original.txt');clear=j('gnosis-all-cleared-fixed-period.original.txt')
assert factory['status']==opyn['status']==clear['status']=='1'
fact=[decode(a) for a in factory['result']];ope=[(a,decode(a)) for a in opyn['result']]
def one(a):assert len(a)==1,len(a);return a[0]
rows=[]
for row in ledger['rows']:
 tx=row['transactions'];op=getrec(tx['open']);cl=getrec(tx['close']);sett=getrec(tx['auction_settle'])
 opened=one([a for a in ev(op,'OpenShort',VA) if a['args']['options']==row['option']])
 D=opened['args']['depositAmount']
 created=one([a for a in fact if a and a['event']=='OtokenCreated' and a['args']['tokenAddress']==row['option']])
 assert all(value==(int(row['option_metadata']['args'][key]) if isinstance(value,int) and not isinstance(value,bool) else row['option_metadata']['args'][key]) for key,value in created['args'].items())
 assert created['args']['collateral']==created['args']['underlying']==W and created['args']['isPut']==False
 dep=one([a for a in ev(op,'CollateralAssetDeposited') if a['args'].get('accountOwner')==VA])
 vid=dep['args']['vaultId'];assert dep['args']['amount']==D
 mint=one([a for a in ev(op,'ShortOtokenMinted') if a['args']['otoken']==row['option']]);Q=mint['args']['amount']
 assert sum(a['args']['value'] for a in transfers(op,W,fr=VA))==D
 assert sum(a['args']['value'] for a in transfers(op,row['option'],fr='0x'+'0'*40,to=VA))==Q
 na=one([a for a in ev(op,'NewAuction') if a['args']['_auctioningToken']==row['option']]);auction=na['emitter'];aid=na['args']['auctionId'];assert na['args']['_biddingToken']==W
 ac=one([a for a in ev(sett,'AuctionCleared',auction) if a['args']['auctionId']==aid])
 P=sum(a['args']['value'] for a in transfers(sett,W,fr=auction,to=VA))
 assert P==ac['args']['soldBiddingTokens']
 assert na['args']['_auctionedSellAmount']==ac['args']['soldAuctioningTokens']==Q
 assert not transfers(sett,row['option'],to=VA)
 se=one([a for a in ev(cl,'VaultSettled') if a['args']['accountOwner']==VA and a['args']['oTokenAddress']==row['option']])
 S=se['args']['payout'];assert se['args']['vaultId']==vid
 cse=one([a for a in ev(cl,'CloseShort',VA) if a['args']['options']==row['option']]);assert cse['args']['withdrawAmount']==S
 assert sum(a['args']['value'] for a in transfers(cl,W,to=VA))==S
 relevant=[(l,a) for l,a in ope if a and a['args'].get('vaultId')==vid and (VA in a['args'].values())]
 partial=[a for l,a in relevant if a['event']=='CollateralAssetWithdrawed']
 U=sum(a['args']['amount'] for a in partial)
 burns=[a for l,a in relevant if a['event']=='ShortOtokenBurned']
 assert U==int(row['collateral_early_released_wei'])
 assert not burns
 fee_rec=getrec(row['fee_tx'])
 fe=[a for a in ev(fee_rec,'CollectVaultFees',VA)]
 F=sum(a['args']['vaultFee'] for a in fe)
 for f in fe:
  matching=[n for n in native if n['hash']==fee_rec['transactionHash'] and n['from']==VA and n['to']==f['args']['feeRecipient'] and n['type']=='call' and n.get('isError')=='0' and int(n['value'])==f['args']['vaultFee']]
  assert len(matching)==1,(row['round_index'],'fee',len(matching))
 G=sum(gas[tx[k]] for k in ['open','auction_settle','close'])
 got={'D':D,'U':U,'S':S,'Q':Q,'P':P,'F':F,'loss':D-U-S,'component':P-(D-U-S)-F,'gas_three_transactions':G}
 expected={'D':'collateral_deposited_wei','U':'collateral_early_released_wei','S':'collateral_final_returned_wei','Q':'minted_option_raw','P':'actual_premium_received_WETH_wei','F':'actual_vault_fee_paid_nativeETH_wei','loss':'actual_collateral_loss_wei','component':'net_after_collateral_and_vault_fee_wei','gas_three_transactions':'actual_3_transaction_gas_wei'}
 for k,e in expected.items():assert got[k]==int(row[e]),(row['round_index'],k,got[k],row[e])
 assert str(vid)==row['opyn_vaultId'] and str(aid)==row['auction_id']
 got.update({'round_index':row['round_index'],'option':row['option'],'open_utc':row['open_utc'],'auction_id':aid,'opyn_vaultId':vid});rows.append(got)
summary={k:sum(a[k] for a in rows) for k in ['P','F','loss','component','gas_three_transactions']}
assert summary['P']==252776178879171899081 and summary['F']==117603280232437587211
assert summary['component']==135172898646734311870 and summary['loss']==0
indirect=[]
for p in sorted(R.glob('indexed-indirect-root*-receipt.original.txt')):
 rec=j(p.name)['result'];assert rec['status']=='0x1'
 tx=rec['transactionHash'];fl=[n for n in native if n['hash']==tx and n['type']=='call' and n.get('isError')=='0']
 indirect.append({'tx':tx,'logs':len(rec['logs']),'receipt_gas':int(rec['gasUsed'],16)*int(rec['effectiveGasPrice'],16),'visible_native_calls':[{'from':a['from'],'to':a['to'],'value':a['value']} for a in fl],'vault_events':[a for l in rec['logs'] for a in [decode(l)] if a and a['emitter']==VA]})
versions=[]
for n in ['historical-oct07-implementation-source.original.txt','temporary-nov03-implementation-source.original.txt','historical-nov19-implementation-source.original.txt','historical-dec03-implementation-source.original.txt','historical-dec10-implementation-source.original.txt']:
 d=j(n);a=d['result'][0];versions.append({'file':n,'status':d['status'],'source_bytes':len(a['SourceCode']),'ABI_verified':a['ABI']!='Contract source code not verified','contractName':a.get('ContractName')})
out={'reviewed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs':inputs,'independent_rows':rows,'independent_sums_raw':summary,'lifecycle_receipts_unique':len(receipts),'factory_count':len(factory['result']),'opyn_owner_log_count':len(opyn['result']),'clearing_count':len(clear['result']),'native_index_count':len(native),'normal_index_count':len(normal),'indirect_receipt_observations':indirect,'version_availability':versions}
(O/'own-passive-cashflow-verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['inputs','independent_rows']},indent=2))
