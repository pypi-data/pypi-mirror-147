from feature_collection import FeatureCollection

class FeatureCollectionTransformer(FeatureCollection):

    def _to_fit_wrappers(self):
        for key in self._feature_desc_dict.keys():
            for idx, wrappedfunc in enumerate(self._feature_desc_dict[key]):
                if wrappedfunc.func is 

    def _fit(self, data, y=None):
        self.


from typing import Union
from sklearn.base import TransformerMixin
from function_wrapper import FuncWrapper

def wrap_transformer(
    transformer: Union[TransformerMixin, FuncWrapper],
) -> FuncWrapper:
    assert isinstance(transformer, FuncWrapper) or isinstance(transformer, TransformerMixin)

    # Extract the keyword arguments from the function wrapper
    func_wrapper_kwargs = {}
    if isinstance(func, FuncWrapper):
        _func = func
        func = _func.func
        func_wrapper_kwargs["output_names"] = _func.output_names
        func_wrapper_kwargs["input_type"] = _func.input_type
        func_wrapper_kwargs.update(_func.kwargs)

    output_names = func_wrapper_kwargs.get("output_names")

    def wrap_func(*series: Union[np.ndarray, pd.Series], **kwargs) -> FuncWrapper:
        if not passthrough_nans:
            series = [s[~np.isnan(s)] for s in series]
        if any([len(s) < min_nb_samples for s in series]):
            if not isinstance(output_names, list) or len(output_names) == 1:
                return error_val
            return tuple([error_val] * len(output_names))
        return func(*series, **kwargs)

    wrap_func.__name__ = "[robust]__" + _get_name(func)
    if not "output_names" in func_wrapper_kwargs.keys():
        func_wrapper_kwargs["output_names"] = _get_name(func)

    return FuncWrapper(wrap_func, **func_wrapper_kwargs)