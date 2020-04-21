import json

from hopsworks import util, engine
from hopsworks.core import join, query_constructor_api


class Query:
    def __init__(self, feature_store, left_feature_group, left_features):
        self._feature_store = feature_store
        self._left_feature_group = left_feature_group
        self._left_features = util.parse_features(left_features)
        self._joins = []
        self._query_constructor_api = query_constructor_api.QueryConstructorApi()

    def read(self, dataframe_type="default"):
        sql_query = self._query_constructor_api.construct_query(self)["query"]
        return engine.get_instance().sql(sql_query, self._feature_store, dataframe_type)

    def show(self, n):
        sql_query = self._query_constructor_api.construct_query(self)["query"]
        return engine.get_instance().show(sql_query, self._feature_store, n)

    def join(self, sub_query, on=[], left_on=[], right_on=[], join_type="inner"):
        self._joins.append(
            join.Join(sub_query, on, left_on, right_on, join_type.upper())
        )
        return self

    def json(self):
        return json.dumps(self, cls=util.FeatureStoreEncoder)

    def to_dict(self):
        return {
            "leftFeatureGroup": self._left_feature_group,
            "leftFeatures": self._left_features,
            "joins": self._joins,
        }
