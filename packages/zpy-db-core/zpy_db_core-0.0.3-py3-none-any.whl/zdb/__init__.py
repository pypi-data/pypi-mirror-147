from zpy.utils.funcs import safely_exec

from zdb.commons import ZDatabase


class ZDBTransact:

    def __init__(self, db: ZDatabase):
        self.db = db
        self.session = None

    def __enter__(self):
        self.session = self.db.new_connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.session.rollback()
        else:
            self.session.commit()
        safely_exec(lambda x: x.close(), [self.session])
