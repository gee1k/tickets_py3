# 命令行查询火车票余票 - Python3

- Install
```
pip install docopt
pip install prettytable
pip install colorama
```

- Usage:
```cmd
python tickets.py [-dgktz] <from> <to> <date>
```

- Options:
```cmd
-h --help       显示帮助
-d              动车
-g              高铁
-k              快速
-t              特快
-z              直达
```

- Example:
```cmd
python tickets.py 上海 苏州 2017-10-20
python tickets.py -dg 上海 苏州 2017-10-20
python tickets.py -g 上海 苏州 2017-10-20
```