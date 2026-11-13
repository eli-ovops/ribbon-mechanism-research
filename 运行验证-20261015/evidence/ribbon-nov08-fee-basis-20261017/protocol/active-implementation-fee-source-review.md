# Active fee source and audit lead: limited review

**PASS_LIMITED_ACTIVE_MAIN_SOURCE_AND_AUDIT_LEAD_LIBRARY_AND_FEE_INPUTS_PENDING**; material_errors=[]

New evidence replaces the earlier two-example choice with a specific mainimplementation source identity. Sourcify declareschain1/6779, creation/runtime match, deployed13370885 and verified2025-06-22. Lastpretargetupgrade receipt actually emits6779 at13545278 before fee13601050. This is provider/platform/history evidence, not independent runtime compilation or2021first-public proof.

Five extracted source units match Sourcify literal content exactly, including the correct contracts/vaults/BaseVaults/base/RibbonVault.sol. Main code is not the initial own-function formula: active _rollToNextOption passes (_lockedBalance+queuedWithdrawAmount) into _collectVaultFees.

In attached VaultLifecycle.rollover, B=assetbalanceOf(vault), pendingP, sharesS/queuedsharesH determine pre-feePPS andQ; return is(B-Q,Q,PPS,mintedshares). Therefore the actual maincaller argument algebraically equalsB, conditional on this attached library being the executed library. getVaultFees usesA=B-P; ifA>L, performance=floor((A-L)*r/1e8), management=floor(A*m/1e8); otherwise0. Fee F is deducted fromB-Q, not from the incomingpremium variable.

Compiledsettings link external VaultLifecycle14cc. Its individual deployed/source identity is not yet separately verified in this review. Main match grade/sourcepack should not be used to silently certify the external library runtime. Root is independently investigating this precise dependency.

Initial code, this active code and laterNov19 code differ. Here PPS is still computed before fee. Attached library managementbaseB-P differs from initialC; main addsqueued to previously reducedlockedbalance. LaterNov19 subtractsfees beforePPS. None should be conflated.

Raw setManagementFee function writes periodic state without emittingManagementFeeSet. The empty queried eventlist cannot prove managementrate unchanged. Performance log0->1e7 is positive evidence of that observedchange but not a substitute for rawasof rates or unobserved upgrade/storage effects.

ChainSafe textPDFpage3 identifiescf498 initial and832817 revised commits, says a separate excessive-newdepositfee issue is not included, and states listed issues fixed by final version. Page5 section4.17 explicitly discusses repeatedprofit attribution when queuedamount is added tolockedbalance. This is a directly relevant mechanistic lead, not certification this transaction used either auditedcommit or that the samecause explains its preciseamount.

Independent fee validation still needs actualstoredr/m and rawpre-evaluation B/P/L under the correctlibrary; independently reconstructing Q/S/queuedclaims is additionally required to diagnose repeatedfee or investorburden, but not an artificial prerequisite if directfeeinputs are available. Do not invert fees to manufacture B/P/L.

Nothing here proves overchargeamount, hack, private discretionary override or full investorprofit. Previously verified totalfee32.246771456298447865 and optioncomponent remain actual cash facts; original formula review preserved as earlierstate, not overwritten.

Old fee-formula-and-minimum-original-fields files retained unchanged. Actual inputfingerprints and exact conditionalformula in JSON. Model/effortactualUNKNOWN; newnetwork and all prohibited executions0.
