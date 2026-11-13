# Fixed12 live-round accounting plan

**PASS_LIMITED accounting plan only; no financial result or profit admission.**

Initial source establishes three distinct principal movements: collateral deposit when minting a short; partial withdrawal when burning remaining oTokens; final remaining collateral settlement. burnOtokens uses floor(current collateral * burn amount / current short amount) and returns actual collateral balance increase. Therefore closed-position collateral loss is D-sum(partial releases)-final returned collateral, subject to all other collateral changes and no remaining liabilities. OpenShort minus CloseShort alone can overstate loss. Fully burned positions may legitimately settle with zero additional collateral.

Unsold tokens, auction custody, actual sales, returns and burns must reconcile. Offered or minted quantity is not sale quantity. Actual premium receipts minus auction charges are not net strategy earnings until collateral loss, all relevant fees and cost bearers reconcile. Principal, refunds, subscriptions and queued withdrawals remain separate.

Rollover fees economically reference the preceding round: Sep17 fee may belong to Sep11 prewindow position, while Dec10 fee may belong to selectedDec3 round. Do not sum just the12 opening transactions. Actual own-fee path uses managementbaseC; unused helper differs. PPS is written before fee debit, so no automatic fee-netPPS assumption. Fee event total and performance component are not two costs; WETH unwrap and native payout are not two incomes.

Receipts establish actual token flows, lifecycle events/status and gas but not all internal ETH flows, economic ownership or complete period coverage. Bind effective upgrades/parameters/external option and auction modules only as needed; initial code does not automatically govern every period. Preserve actual12 openings and delayedNov8, and verify final settlement boundary. Empty/error and missing-payment evidence remain distinct.

Use asset vectors first; operatorGas is separate from vault fee and investor costs, with explicit payer/allocation. ETH quantities, a holding-ETH benchmark and USD reference returns are separate calculations. No hypothetical holder fills, all-business-lifetime requirement, permanent-parameter constraint or full privatebot demand is added. Detailed minimal fields/formulas and input fingerprints are in JSON.

Rules unchanged, inherited actual model/effort UNKNOWN. New network and source/model/backtest/ABI/EVM/SQL/strategy execution, account/payment/trading/sends zero.
