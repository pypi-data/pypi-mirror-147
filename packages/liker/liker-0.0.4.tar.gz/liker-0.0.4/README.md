# Python package `liker`

The book `(R과 비교하며 배우는) 파이썬 전처리와 시각화` introduces Python to R Users.
This package `liker` has functions that mimic R in Python.

Here are examples

```python
c(2,3,5,7,11) # creates list or array with elements 2,3,5,7,11
ac(2,3,5,7,11) # creates a numpy array
lc(2,3,5,7,11) # creates a list
c = lc        

pdDataFrame(x=[1,3,2], y=['a', 'b', 'c'])
# equivalent to R data.frame(x=c(1,3,2), y=c('a', 'b', 'c'))
# you can also do
pdDataFrame(x=c(1,3,2), y=c('a', 'b', 'c'))
```

More examples to come!
