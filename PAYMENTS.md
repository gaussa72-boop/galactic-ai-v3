# Quantum Payments & Credits

Shared prepaid-credit contract. Credits are granted only after verified idempotent payment events. Stripe/crypto are provider adapters, not custody. Never store private keys. Production balances, payment events, intents and ledger entries must be persisted transactionally. Reserve credits before paid generation and release them on failure. Secrets stay outside Git.
