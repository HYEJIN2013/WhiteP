from App.config import getConfiguration

import transaction

configuration = getConfiguration()
db = configuration.dbtab.getDatabase(name='main')

tm = transaction.TransactionManager()
conn = db.open(transaction_manager=tm)
tm.begin()

try:
    root = conn.root()
    del root['zc.async']
    tm.commit()
except Exception:
    tm.abort()
    raise
finally:
    conn.close()
