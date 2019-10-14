from .base import Predicate
from .is_dict_where import is_dict_where
from .is_in import is_in
from .is_superdict_where import is_superdict_where
from .is_subdict_where import is_subdict_where
from .to_pred import to_pred


class is_dict_union(Predicate):

    def __init__(self, *args, **kwargs):
        if args and isinstance(args[0], str):
            key, *args = args
        else:
            key = 'type'
        self._key = key
        self._preds = {
            value: self._to_pred(pred, value)
            for value, pred in dict(*args, **kwargs).items()
        }
        self.prerequisites = [is_superdict_where({
            key: is_in(set(self._preds)),
        })]

    def _to_pred(self, pred, value):
        pred = to_pred(pred)

        if type(pred) in [is_dict_where, is_superdict_where, is_subdict_where]:
            if type(pred) is is_superdict_where:
                cls = is_superdict_where
            else:
                cls = is_dict_where

            required = {self._key: value}
            optional = {}
            for key, subpred in pred._predicates.items():
                if key in pred._required:
                    required[key] = subpred
                else:
                    optional[key] = subpred

            pred = cls(required, optional)

        elif type(pred) is is_dict_union:
            return is_dict_union(pred._key, {
                subvalue: self._to_pred(subpred, value)
                for subvalue, subpred in pred._preds.items()
            })

        return pred

    def _evaluate(self, data, explain, context):
        return self._preds[data[self._key]](data, explain, context)
