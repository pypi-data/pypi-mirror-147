# Change Log

## 1.1.1 (4/21/2022)
- Added ability to use generators

## 1.1.0 (10/22/2021)
- Added ability to use the average time to estimate future time.
- Added docstrings.
- Improved performance when using "+=" opperator.
- Increased efficiency of object.

## 1.0.4.4 (6/11/2021)
- Bug Fixes

## 1.0.4 (6/11/2021)
- Added "__iter__" attribute to allow for more effective use in loops.

### Example:
```Python
for i in ProgressBar(range(10)):
    ...
```

## 1.0.3.3 (6/8/2021)
- Bug Fixes

## 1.0.3 (6/2/2021)
- Added ability to adjust "learning rate" for the rate of items
- Made "completed" arguement for "update" method default to None, which just means increment by one

## 1.0.2.2 (5/7/2021)
- Bug Fixes

## 1.0.2 (5/6/2021)
- Added support for updating multiple items (timer would update as one item)
- Added ability to adjust the starting rate of items for the timer
- Fixed bugs using "+=" (__iadd__) (caused timer to not work)

## 1.0.1.2 (5/6/2021)
- Bug Fixes

## 1.0.0 (5/6/2021)
- First Release