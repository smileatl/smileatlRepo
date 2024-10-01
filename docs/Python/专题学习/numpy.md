## np.array(df).ravel().astype(float)

用ravel()把数据最里面的中括号去掉



# 问题

在np.average时，当有weights时，报错TypeError: No loop matching the specified signature and casting was found for ufunc add

```python
# dtype object通常是指一个NumPy数组中的数据类型
# 在NumPy数组中，每个元素的数据类型通常是预定义的，如float、int等
# 但是如果数组中的元素具有不同的数据类型或者需要自定义数据类型，那么可以使用dtype object来指定。
def aggregate(self, models, index_s):
	index_s = np.array(index_s, dtype=object)
	self.__model.set_weights(list(np.average(list(models.values()), weights=index_s, axis=0)))
```

- dtype object是一种特殊的数据类型对象，它用于描述NumPy数组中元素的数据类型。通过指定dtype=object，可以让NumPy数组支持更多的数据类型，例如复数、日期、字符串等。此外，dtype object还可以用于指定数据类型的大小、字节顺序等属性。
- 需要注意的是，使用dtype object会使得数组的运算速度变慢，因为每个元素都需要使用Python的解释器来执行运算，而不是使用NumPy的优化运算。因此，只有在必要的情况下才应该使用dtype object，否则应该尽量使用预定义的数据类型来提高数组的运算效率。