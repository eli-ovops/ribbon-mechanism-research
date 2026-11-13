# Volatility oracle source: limited review

**PASS_LIMITED_SOURCE_INPUT_SEMANTICS_HISTORY_AND_EXTERNAL_PROVENANCE_PENDING**; material_errors=[]

ManualVolOracle.sol L719-774: Provided source is an admin-written mapping, not an onchain volatility estimator. setAnnualizedVol accepts any pool and positiveuint, checks ADMIN_ROLE, overwrites value. No source-label, Deribit/DVOL proof, timestamp, age bound, cap or economic-quality validation.

L743-759 and L765-772: annualizedVol returns raw storeduint unchanged; source specifies1e8=100% annualised standard deviation. Sigma fraction=raw/1e8; display percent=raw/1e6. vol(pool) returns0 and must not be substituted for the annualized getter used by actual modules.

phase93 operational premium L278-292; strike L90-97: Consumers multiply annualized raw by1e10 to18decimal computation. No getter100x transformation or percent/fraction confusion. The source chain binds the read getter semantics, not original market data accuracy.

ManualVolOracle L729-739; AccessControl L554/634-655/700-713: Constructor grants ADMIN_ROLE to its _admin; only that role can setvol. ADMIN_ROLE is not DEFAULT_ADMIN_ROLE. In shown source constructor no default-admin grant; inherited grant/revoke require target role admin(default0x00), so do not assume a vol writer may freely grant/revoke writers. Actual historical role identities require real creation/role records; provider ConstructorArgumentsa429... is only metadata.

ManualVolOracle L767-773; ABI/source declaration: No volatility-update event is emitted by setter. Historical event-only search cannot reconstruct updates or prove none. Successful tx calldata and block/log order can support observed direct-call asof values; indirect execution or full state completeness needs appropriately scoped qualification.

Provider source envelope/compiler/settings and sourceSPDX: Provider declares ManualVolOracle,0proxy, compiler0.7.3; source SPDXGPL-3.0, provider LicenseType blank. No independent compilation/runtime or historical first-public proof. GPL source declaration is not a complete dependency/data/trading authorization audit.

Scope and static-method inference: Call it authorized publication of a volatility number, not proven manual human IV, HV or DeribitDVOL. Automated caller, private calculation or manually selected number are all consistent with this setter. The official historical DVOL explanation and actual chain values are distinct evidence layers.

Public reusable research mechanics:

- Inspect public units, pool-keyed state and role separation; preserve exact pool, raw value, update tx/UTC/block/order and last observed value before actual quotation.
- Use actual successful historical updates as recorded inputs without replaying a model; disclose stale data and omitted indirect updates rather than silently substitute current/future values.
- Publicly viewable onchain values may be research-accessible without updater role, but this review makes no promise of current free API availability or permission to write existingoracle.
- Separate algorithm/source license from original volatility-feed terms; no paid data, credentials, source execution or trading authorized here.

Preserve135.172898646734311870ETH/WETH positive option component; not full investor profit or wealth achievement. Actual inputs/SHA/bytes are in JSON. Source line numbers refer to decoded splitlines, not raw-byte offsets. Actual model/effort UNKNOWN; new network and prohibited executions zero.
