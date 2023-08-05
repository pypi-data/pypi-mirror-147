def model_to_data(model=None):
    return tuple([i.data if hasattr(i, "data") else i for i in model])

class SqleeException(Exception):
	"""
        Sqlee Base Exception.
    """

class SqleeWarning(Warning):
    """
        Sqlee Base Warning.
    """

class VersionError(SqleeException):
    pass

class RepositoryNotFound(SqleeWarning):
    def __init__(self, repo_name=None, args="目标数据库 '{}' 不存在，将尝试建立它."):
        if repo_name:
            args = args.format(repo_name)
        super(RepositoryNotFound, self).__init__(args)
        self.repo_name = repo_name

class RepositoryNotFoundError(SqleeException):
    def __init__(self, repo_name=None, args="目标数据库 '{}' 不存在."):
        if repo_name:
            args = args.format(repo_name)
        super(RepositoryNotFoundError, self).__init__(args)
        self.repo_name = repo_name

class RepositoryConnectionRefusedError(SqleeException, ConnectionRefusedError):
    def __init__(self, repo_name=None, status_code=None, args="连接目标数据库 '{}' 出现异常."):
        if repo_name:
            args = args.format(repo_name)
        if status_code:
            args += " [Code %d]" % status_code
        super(RepositoryConnectionRefusedError, self).__init__(args)
        self.repo_name = repo_name
        self.status_code = status_code

class TableNotFoundError(SqleeException):
    def __init__(self, table_name=None, args="目标表 '{}' 不存在."):
        if table_name:
            args = args.format(table_name)
        super(TableNotFoundError, self).__init__(args)
        self.table_name = table_name

class ColumnNotFoundError(SqleeException):
    def __init__(self, column_name=None, args="目标表 '{}' 不存在."):
        if column_name:
            args = args.format(column_name)
        super(ColumnNotFoundError, self).__init__(args)
        self.column_name = column_name

class ColumnDataDoesNotFit(SqleeWarning):
    def __init__(self, namespace=None, datas=None):
        args = "数据错误: 捕获到的数据与命名域不符:\n\t命名域: {}\n\t数据: {}."
        args = args.format(namespace, model_to_data(datas))
        super(ColumnDataDoesNotFit, self).__init__(args)

class DataWasNotGiven(SqleeWarning):
    def __init__(self, namespace=None, args="数据错误: 数据 '{}' 未被传入，使用空值代替."):
        super(DataWasNotGiven, self).__init__(args.format(namespace))

class DataWasNotGivenError(SqleeException):
    def __init__(self, namespace=None, args="数据错误: 数据 '{}' 未被传入."):
        super(DataWasNotGivenError, self).__init__(args.format(namespace))

class InternetError(SqleeException):
    def __init__(self):
        super(InternetError, self).__init__("网络连接异常，请检查网络连接.")