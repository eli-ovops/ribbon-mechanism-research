# Ribbon historical rules and fees: limited review

**PASS_LIMITED_HISTORICAL_MECHANISM_REVIEW_ACTUAL_PARAMETERS_PENDING**; no financial case admitted.

Official page metadata dates the algorithm article to2021-08-30, Gnosis auctions to2021-09-08 and launch to2021-09-13 (first announced sales Sep17). Pages also show later modification dates, so these are retrieved official historical statements, not independent contemporary snapshots. Algorithm article L24 and L34-38 explicitly separates onchain strike computation from manually updated weekly DVOL inputs. Current offchain/proprietary-IV and Paradigm docs cannot be backfilled into that version.

Source controls: owner can replace strike/pricer, discount/duration and override a current-round strike; keeper executes roll/start/burn, while commitAndClose has no keeper modifier. Expiry is computed as Friday08:00UTC; selected strike follows current-round override or external selection. Public/reconstructable variable parameters are not a hard replication failure. Conversely, broad governance discretion is not itself a full fixed generator policy.

**Fee-path distinction affecting accounting:** RibbonVault._rollToNextOption calls its own _collectVaultFees. For C=currentLockedBalance,P=pending,L=lastLocked, fees apply only when C-P>L. Performance base is C-P-L, while management base is C. VaultLifecycle.getVaultFees instead uses C-P as management base, but is not called by this shown path. Actual state rates remain UNKNOWN. Fees transfer underlying assets, with WETH unwrapped to ETH; event performance component and total fee must not both be counted as full charges. roundPricePerShare is recorded before this transfer, so do not assume it is fee-net without actual version/flows. No security defect is inferred here.

Repository deployment artifact address257518... conflicts with receipt.contractAddress B0A54... (block13195416). It cannot alone prove the selected proxy's initial rates or initialization. All three units declare MIT SPDX, limited to these source units; dependency or commercial-service permissions and historical deployed binding remain separate.

Premium is paid by option buyers for rights, against a short-call obligation. Mint/lock, unsold-option burn and settlement unlocking principal are not income. Net outcome requires actual auction receipts, collateral returned/lost, actual fees, holder share/flow accounting, gas and failures. Do not double-deduct settlements or fees already included in final assets. No actual profit/ROI or personal replication advantage is concluded.

Complete inputs and source line locations are recorded in JSON. Actual model/effort UNKNOWN; additional network and all source/model/backtest/ABI/EVM/SQL/strategy execution, account/payment/trading/sends zero.
