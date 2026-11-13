from pathlib import Path
import json,hashlib,datetime
from decimal import Decimal
B=Path('/Volumes/EXTERNAL/亚力克斯 /运行验证-20261015/evidence/ribbon-fixed12-live-ledger-20261017');R=B/'root';O=B/'protocol'
own=json.loads((O/'own-passive-cashflow-verification.json').read_text());inputs=own['inputs'].copy();checks={}
def read(n):
 p=R/n;z=p.read_bytes();inputs[str(p)]={'sha256':hashlib.sha256(z).hexdigest(),'bytes':len(z)};return z
def j(n):return json.loads(read(n))
normalpages=[]
for i in range(1,5):normalpages+=j('vault-normal-transactions-period-page'+str(i)+'.original.txt')['result']
suffix=j('vault-normal-transactions-period-inclusive-suffix.original.txt')['result']
checks['normal_suffix_boundary']=suffix[0]['blockNumber']==normalpages[-1]['blockNumber']
merged={}
for a in normalpages+suffix:merged[a['hash']]=a
normal=j('normal-transactions-combined.json')['records']
checks['normal_raw_merged_equal']=list(merged.values())==normal
native=[]
for n in ['vault-indexed-internal-transfers-period','vault-indexed-internal-transfers-period-page2']:native+=j(n+'.original.txt')['result']
checks['native_raw_merged_equal']=native==j('indexed-native-transfers-combined.json')['records']
checks['native_identity_unique']=len({(a['hash'],a['traceId'],a['type']) for a in native})==len(native)
for stem in ['vault-normal-transactions-period-page1','vault-normal-transactions-period-page2','vault-normal-transactions-period-page3','vault-normal-transactions-period-page4','vault-normal-transactions-period-inclusive-suffix','vault-indexed-internal-transfers-period','vault-indexed-internal-transfers-period-page2','factory-eth-call-creation-events-page1','opyn-all-vault-owner-events','gnosis-all-cleared-fixed-period']:
 a=read(stem+'.original.txt');rr=j(stem+'.read-receipt.json');d=json.loads(a)
 checks[stem+'_receipt']=rr['status']==200 and rr['bytes']==len(a) and rr['sha256']==hashlib.sha256(a).hexdigest()
 checks[stem+'_body']=d['status']=='1' and d['message']=='OK'
receipts={};indirect={}
for pat,target in [('round*-receipt.original.txt',receipts),('indexed-indirect-root*-receipt.original.txt',indirect)]:
 for p in sorted(R.glob(pat)):
  a=read(p.name);rr=j(p.name.replace('.original.txt','.read-receipt.json'));d=json.loads(a)['result']
  checks[p.name+'_receipt']=rr['status']==200 and rr['bytes']==len(a) and rr['sha256']==hashlib.sha256(a).hexdigest()
  target[d['transactionHash']]=d
normalgas=sum(int(a['gasUsed'])*int(a['gasPrice']) for a in normal)
extra=sum(int(a['gasUsed'],16)*int(a['effectiveGasPrice'],16) for tx,a in receipts.items() if tx not in merged)
indgas=sum(int(a['gasUsed'],16)*int(a['effectiveGasPrice'],16) for a in indirect.values())
checks['indirect_not_already_gas_counted']=not(set(indirect)&(set(merged)|set(receipts)))
for tx,a in receipts.items():
 if tx in merged:checks['receipt_normal_gas_'+tx]=int(merged[tx]['gasUsed'])==int(a['gasUsed'],16) and int(merged[tx]['gasPrice'])==int(a['effectiveGasPrice'],16)
sup=j('fixed12-ledger-completeness-supplement.json');leg=j('fixed12-actual-cashflow-ledger.json');ds=j('static-event-descriptors-complete.json');topic=next(a['topic'] for a in ds if a['name']=='CollectVaultFees')
perf=0
for row,part in zip(leg['rows'],sup['fee_parts']):
 ls=[l for l in receipts[row['fee_tx']]['logs'] if l['address']=='0x25751853eab4d0eb3652b5eb6ecb102a2789644b' and l['topics'][0]==topic]
 p=sum(int(l['data'][2:66],16) for l in ls);perf+=p;checks['fee_part_'+str(row['round_index'])]=p==int(part['fee_performance_wei']) and int(row['actual_vault_fee_paid_nativeETH_wei'])-p==int(part['fee_management_by_difference_wei'])
pair=sup['native500_pair'];inc=pair['incoming_normal_index'];out=pair['outgoing_indexed_internal_record']
checks['native500_pair']=merged[inc['hash']]==inc and out in native and inc['from']==out['to'] and inc['to']==out['from'] and int(inc['value'])==int(out['value'])==500*10**18
for a in pair['later_same_sender_deposit_attempts']:
 n=merged[a['hash']];checks['later_deposit_'+a['hash']]=all(n[k]==v for k,v in a.items() if k!='methodId') and n['input'][:10]==a['methodId']
for n in ['nov19-RibbonVault.sol.source.txt','nov19-RibbonThetaVault.sol.source.txt','nov19-VaultLifecycle.sol.source.txt']:read(n)
P=own['independent_sums_raw']['P'];F=own['independent_sums_raw']['F'];totalgas=normalgas+extra+indgas
checks['new_gas_total']=totalgas==9181600067662971822
checks['new_cost_sensitivity']=P-F-totalgas==125991298579071340048
checks['performance_total']=perf==79065793872676495252
checks['management_difference']=F-perf==38537486359761091959
z={'inputs':inputs,'checks':checks,'all_checks_passed':all(checks.values()),'failed_checks':[k for k,v in checks.items() if not v],'gas_raw':{'normal_index':normalgas,'extra_known_receipts':extra,'five_indirect_roots':indgas,'total':totalgas,'component_after_cost_sensitivity':P-F-totalgas},'performance_raw':perf,'management_difference_raw':F-perf,'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
(O/'own-completeness-and-supplement-check.json').write_text(json.dumps(z,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in z.items() if k not in ['inputs','checks']},indent=2))
