from sqlalchemy.exc import IntegrityError, DataError, ProgrammingError, InterfaceError, OperationalError

class MySQLError:

    def __init__(self):
        self.integrity_error = IntegrityError
        self.data_error = DataError
        self.programming_error = ProgrammingError
        self.interface_error = InterfaceError
        self.operational_error = OperationalError

mysql_error = MySQLError()