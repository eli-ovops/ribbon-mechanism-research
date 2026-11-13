# Holder selection and terminal accounting review

PASS_LIMITED_SELECTION_AND_TERMINAL_ACCOUNTING_PLAN_NOT_HOLDER_PROFIT_ADMISSION

Selection is acceptable: first positive standard Deposit before the selected Sep17 opening, ordered by block/global log, with only actually evidenced owner/keeper/zero exclusions and no profit/holding-period filter. Application owner is not proxy admin. Initial source236-239 has no keeper-change event, so event absence cannot prove unchanged roles. DepositFor credits a creditor while another address may pay. No candidate cashflows were read by this reviewer.

For an early fully closed holder episode, reconcile actual capital paid, all actual receipts, share transfers, pending deposit receipts, queued claims, and attributable gas/approval/failed-attempt expenses. No need to force a closed account to hold until Dec10. Redeem is a share transfer, initiateWithdraw is escrow, completeWithdraw is cash payout: do not count them as three incomes. Vault fee already reflected in cashout is not another expense to deduct. Opening rights need not be zero and FIFO/private-bot disclosure is not required for an incremental ledger.

Terminal boundary is material. November19 ThetaVault284-345 closes and settles the old short. Later350-371 calls rollover, finalizes fee/PPS, then creates another short in that transaction. Thus Dec10 post-close/pre-roll cash is not automatically fee-net, and post-roll locked collateral is not fair NAV with the new option valued0. Older active RibbonVault590-597 records pre-fee PPS; terminal November19 Lifecycle220-260 deducts fees before PPS. Versions cannot be interchanged.

Residual minimum: held shares; depositReceipts(round,amount,unredeemedShares); withdrawals(round,shares); exact vault round and applicable finalized PPS; fee treatment/version; material assets and queued/option liabilities needed for this holder. Prior receipt conversion is floor(amount*10^d/PPS)+unredeemedShares; current pending amount is separate. Finalized queued entitlement is floor(shares*PPS[withdrawal.round]/10^d), not an additional right on top of its escrowed shares. Actual complete withdrawal may settle the holder without pricing the entire vault. Continuing material exposure without value remains UNKNOWN, not cash profit.

Inputs and source line locations are in JSON. Rules PERMISSIONS-2026-10-14-v1 and ROUTING-2026-10-13-v4; actual model/effort UNKNOWN. Network/source/model/backtest/EVM/trading execution all0. This validates the limited plan, not depositor profit, full profitable-case admission, or wealth-target completion.
