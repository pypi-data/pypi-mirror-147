import pymongo

from DuyanCommon.CommonUtls import EntityPage, Entity
from Error import PageError, SizeError, OverSizeLimitError


class BasicDBObject(dict):
    EQUALS = "$eq"
    NOT_EQUALS = "$ne"
    GREATER_THEN = "$gt"
    GREATER_THEN_EQUALS = "$gte"
    LESS_THEN = "$lt"
    LESS_THEN_EQUALS = "$lte"
    REGEX = "$regex"
    IN = "$in"
    NOT_IN = "$nin"
    MATCH = "$match"
    GROUP = "$group"
    SUM = "$sum"
    EXISTS = "$exists"
    COND = "$cond"

    @staticmethod
    def field_value_key(field_name):
        """
        :param field_name:
        :return:
        """
        return f"${field_name}"

    def cond(self, conditions, hit_value, else_value):
        return self.put(self.COND, [conditions, hit_value, else_value])

    def eq(self, key: str, value):
        """
            等于
        """
        return self.put(key, {self.EQUALS: value})

    def ne(self, key: str, value):
        """
            不等于
        """
        return self.put(key, {self.NOT_EQUALS: value})

    def gt(self, key, value):
        """
            大于
        """
        return self.put(key, {self.GREATER_THEN: value})

    def gte(self, key, value):
        """
            大于等于
        """
        return self.put(key, {self.GREATER_THEN_EQUALS: value})

    def lt(self, key, value):
        """
            小于
        """
        return self.put(key, {self.LESS_THEN: value})

    def lte(self, key, value):
        """
            小于等于
        """
        return self.put(key, {self.LESS_THEN_EQUALS: value})

    def between(self, key, min_value, max_value):
        return self.put(key, {self.GREATER_THEN_EQUALS: min_value, self.LESS_THEN_EQUALS: max_value})

    def range(self, key, min_value, max_value, include_min=False, include_max=False):
        """
            范围查询 ， 默认前后不包括
        """
        return self.put(key,
                        {include_min and self.GREATER_THEN_EQUALS or self.GREATER_THEN: min_value,
                         include_max and self.LESS_THEN_EQUALS or self.LESS_THEN: max_value})

    def like(self, key, regex_value):
        """
            模糊匹配
        :param key:
        :param regex_value:
        :return:
        """
        return self.put(key, {self.REGEX: regex_value})

    def in_(self, key, value: list):
        return self.put(key, {self.IN: value})

    def not_in(self, key, value: list):
        return self.put(key, {self.NOT_IN: value})

    def sum(self, name, field_name):
        return self.put(name, {self.SUM: field_name})

    def exists(self, key):
        return self.put(key, {self.EXISTS: True})

    def not_exists(self, key):
        return self.put(key, {self.EXISTS: False})

    def match(self, query: dict):
        return self.put(self.MATCH, query)

    def group(self, aggregate: dict):
        return self.put(self.GROUP, aggregate)

    def put(self, key, value):
        if isinstance(key, bytes):
            key = str(key, encoding='utf-8')
        key = str(key)
        if key in self.keys():
            raise Exception(f"字段{key}条件已存在")
        self[key] = value
        return self


class MongoDBClient(object):

    def __init__(self, host: str, db_name: str, table_name: str, limit: int = 0):
        """
            mongo 客户端
        :param host:
        :param db_name:
        :param table_name:
        :param limit: 查询最大数量，防止内存不足问题 ，不设置不会对查询结果进行限制
        """
        self.host = host
        self.db_name = db_name
        self.table_name = table_name
        self.client = pymongo.MongoClient(self.host)
        self.db = self.client.get_database(self.db_name)
        self.table = self.db.get_collection(self.table_name)
        self.limit = limit if limit is not None and limit > 0 else None

    def switch_table(self, table_name):
        self.table_name = table_name
        self.table = self.db.get_collection(self.table_name)

    def __find__(self, query: BasicDBObject, order_by: list = None, page: int = None, size: int = None):
        """
            基础查询 find 的方法都给予此
        :param query:  查询sql
        :param order_by: 排序方式 ，列表例如 ：[("field_name" , pymongo.DESCENDING)]
        :param page: 分页
        :param size: 每页展示条数
        :return:
        """
        cur = self.table.find(query)

        if order_by is not None:
            cur = cur.sort(order_by)
        if page is not None and size is not None and size > 0:
            cur = cur.skip(page * size).limit(size)
        elif size is not None and size > 0:
            cur = cur.limit(size)
        return cur

    def find_one(self, query: BasicDBObject, order_by: list = None) -> Entity:
        """
            查找一条
        :param query:
        :return:
        """
        entity_obj = self.__find__(query, order_by=order_by, size=1)
        return Entity(entity_obj[0]) if entity_obj is not None and len(entity_obj) > 0 else None

    def count(self, query: BasicDBObject) -> int:
        """
            计数
        :param query:
        :return:
        """
        return self.table.count_documents(query)

    def find(self, query: BasicDBObject, order_by=None, ) -> list[Entity]:
        """
            查询 不分页
        :param query:
        :param order_by:
        :return:
        """
        data = self.__find__(query, order_by=order_by,
                             size=self.limit if self.limit is not None and self.limit > 0 else None)
        return Entity.build_list(data)

    def find_page(self, query: BasicDBObject, page: int, size: int, order_by=None) -> EntityPage:
        """
            分页查询
        :param query:
        :param page:
        :param size:
        :param order_by:
        :return:
        """
        if page is None or page < 0:
            raise PageError
        if size is None or size <= 0:
            raise SizeError
        if self.limit is not None and 0 < self.limit < size:
            raise OverSizeLimitError
        data = self.__find__(query, order_by, page, size)
        total = self.count(query)
        return EntityPage.build_obj(data, page, size, total)

    def group(self, match: BasicDBObject, group: BasicDBObject) -> list[Entity]:
        """
            聚合 这里能完成简单的聚合并提供对象
        :param match:
        :param group:
        :return:
        """
        if match.get(BasicDBObject.MATCH) is None:
            match_obj = {BasicDBObject.MATCH: match}
        else:
            match_obj = match
        if group.get(BasicDBObject.GROUP) is None:
            group_obj = {BasicDBObject.GROUP: group}
        else:
            group_obj = group
        data = self.table.aggregate([match_obj, group_obj])
        entities = list()
        for item in data:
            entity = Entity()
            for key, value in item.items():
                if key == "_id":
                    for k, v in value.items():
                        entity.__setattr__(str(k), v)
                else:
                    entity.__setattr__(str(key), value)
            entities.append(entity)
        return entities



