class ColumnType:
    name = None

class StrColumn(ColumnType):
    name = "TEXT"

class IntColumn(ColumnType):
    name = "BIGINT"
    
class TableMeta(type):
    def __new__(cls, name, base, dct, **kwargs):
        dct["tablename"] = kwargs.pop("table_name", name)
        columns = {}
        for name, type_ in dct.items():
            if isinstance(type_, ColumnType):
                columns[name] = type_.name
        dct["columns"] = columns
        return super().__new__(cls, name, base, dct)
    
class TableError(Exception):
    pass
    
class Table(metaclass=TableMeta):
    @property
    def create(self):
        columns = ', '.join(f'{i} {self.columns[i]}' for i in self.columns)
        return f"CREATE TABLE IF NOT EXIST {self.tablename}({columns})"
    
    def insert(self, **kwargs):
        for name in kwargs:
            if not name in self.columns:
                raise TableError("存在しないカラムです")
        colums = ", ".join(name for name in kwargs)
        values = [kwargs[name] for name in kwargs]
        valuetext = ', '.join('%s' for i in values)
        return f"INSERT INTO {self.tablename}({colums}) VALUES({valuetext})", values
    
    def select(self, **kwargs):
        if kwargs == {}:
            return f"SELECT * FROM {self.tablename}"
        else:
            for name in kwargs:
                if not name in self.columns:
                    raise TableError("存在しないカラムです")
            text = " AND ".join(f"{name}=%s" for name in kwargs)
            data = [kwargs[name] for name in kwargs]
            return f"SELECT * FROM {self.tablename} WHERE {text}", data
