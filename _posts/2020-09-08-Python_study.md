---
title: Python简要知识点记录
date: 2020-09-08 11:50:20
tags: [Python, FreeBSD]
---

对于Python学习过程的记录，便于对于一些基础信息和概念的查询。


# Python Notebook

## 1 Python数据类型 (Python的数据类型可以看作是一种容器)

### 1.1 列表
- 列表对象可嵌套

    + 嵌套多属性列表
```
L1 = [1, 2, 3, 4, 5]
L2 = [1, 'spam', [2.3, 4]]
L3 = [ ]
print (L2[1][0])  #结果就是's'
```

- 有序性数据获取
    + 截取列表中的特定数据
```
L = [1,2,3,4,5,6,7,8]
print(L[0::2])
```
- 列表的动态扩展及本地修改
    + 扩展1个, 插入, 扩展多个
```
L = [1,2,3,4,5,6,7,8]
print(L[1:3])    #左闭右开
L.append(5)
L.insert(1,10)    
L.extend([11,22,33])
``` 
    + 删除
```
L1 = ['aa','bb','cc'] 
L1.remove('aa')
```
    + 后进后出
```
L1 = [1,2,3]
print(L1.pop())#末端删除一个元素，弹出删除的值
print(L1)
```
    + 排序
```
L = [1,5,3,8,3,2,10]
L.sort()
print(L)
L.reverse()
print(L)
```

### 1.2 字典
- 字典是无序的, 通过键值来反映映射关系; 可以支持异构

    Key是唯一, value是可以对应多类对象的, 比如整型, 字符, 列表, 甚至对应元组
    ```
    D = {
    'name':{'first':'Bob', 'last':'Smith'},
    'job' : ['dev','mgr'],
    'age' : 0.5,
    'addr': 'BeiJing'
    }
    ```


    可以针对字典的内容进行修改, 比如下面就是增加了一个字典KV值
    
    `D['sex'] = 'gender'`
    
- 生成字典的方法

    + 初始空字典, 动态填充
    ```
    D = {}
    D['name'] = 'Bob'
    D['job'] = 'dev'
    print(D)
    ```

    + 通过列表动态生成
    ```
    key_list = ['a','b','c']
    value_list = [11,22,33]
    D = dict(zip(key_list, value_list))
    print(D)
    ```
    
    + 键值对元组构造
    
    ```
    D = dict([('aa',11),('bb',22),('cc',33)])
    print(D)
    ```

- 更新字典

    合并两个字典, 为无规律更新覆盖, 需要注意
    ```
    D1 = {'a':1,'b':2, 'c':3}
    D2 = {'c':8, 'd':9}
    D1.update(D2)
    ```

- 获取字典键list或者值list
    
    能够快速的获取键值list
    ```
    D = {'a': 11, 'b': 22, 'c': 33, 'd': 44, 'e': 55}
    print (list(D.keys()))
    print (list(D.values())
    print (list(D.items()) #获取键值对列表
    ```

- 删除字典

    ```
    del D['a']
    D.pop('a')
    ```
    
- 字典的排序

    字典的排序是对于键的排序, 以下两个操作结果是一致的
    ```
    print(sorted(D))
    print(sorted(D.keys()))
    ```
    
### 1.3 元组

- 可以看作是不可变的列表

    ```
    T = (1,2,3,4)
    M = ('spam', 3.0, [11,22,33])
    print(T[1])
    print(M[2][0])
    ```
    
- 可以对元组进行连接
    ```
    T1 = (1,2,3,4)
    T2 = (5,6,7,8)
    print(T1 + T2)
    ```

- 元组和列表的转换

    元组转换成列表后进行排序
    ```
    T = ('cc','bb','dd','aa')
    tmp = list(T)
    tmp.sort()
    T = tuple(tmp)
    ```
    
    另外一种方式: `sorted(T)`
    
    
### 1.4 容器(数据类型)遍历和解析

- 遍历list
    ```
    List = [1,2,3]
    for x in List:
    print(x)
    ```
- 遍历元组
    ```
    D = {'a':1, 'c':2, 'b':3}
    for k in D:
        print('{}--->{}'.format(k,D[k]))
    ```
    其中, K只是Key值
- 遍历字典
    ```
    D = {'a':1, 'c':2, 'b':3}
    for k,v in D.items():
        print('{}--->{}'.format(k,v))
    ```
    直接赋值Key和values
    

- 解析的特点:
    + 序列运算表达式
    + 循环表达式
    + 过滤条件
    
    + 针对列表
    ```
    a = [1,2,3,4,5,6,7,8,9,10]
    b = [x**2 for x in a]
    print(b)
    ```
    or 加入过滤条件
    ```
    a = [1,2,3,4,5,6,7,8,9,10]
    b = [x**2 for x in a if x % 3 == 0]
    print(b)
    ```
    
    + 针对字典
    ```
    D1 = {'a': 1, 'b': 2, 'c': 3}
    D2 = {k: v*2 for (k, v) in D1.items()}
    print(D2)
    ```
    or 构造字典
    ```
    D = {c:c*4 for c in ['a', 'b', 'c', 'd']}
    print(D)
    ```
    
### 1.5 字符串

- 字符串简介

    字符串可以看作是单个字符组成的有序序列, 不可更改. 可以有如下运算:
    ```
    s = 'abcdefg'
    print(s[0])
    print(s[-2])
    print(s[1:4])
    print(s[1:4:2])
    print(s[-1:1:-1])
    print(len(s))
    ```
    字符串可以连接相加
    ```
    s1 = 'abcd'
    s2 = '1234'
    s = s1 + s2
    ```
    
- 字符串操作
    + 深cp(硬cp)
    ```
    s = ['abcdefg']
    a = s[:]
    print(a)
    print(s is a)  # False
    ```
    
    + 浅cp(软cp)
    ```
    s1 = 'abcdefg'
    s2 = s1
    print(s1 == s2)   # True
    ```
    
    + 字符串也可以被遍历
    ```
    s = 'hacker'
    for c in s:
        print(c, end=' ')
        
    h a c k e r 
    ```
    
- 进阶用法
    + 字符串查找
    ```
    s = 'abcdef'
    print(s.find('cde'))    #返回偏移值 "2"
    print(s.find('xy'))     #返回"-1"
    ```
    
    + 字符串替换
    ```
    s = 'abcdef'
    print(s.replace('bcd','XXX'))
    ```
    
    + 字符串拆分和提取, split
    
    输出列表
    ```
    s = 'Tom,21,USA,UCLA'
    l = s.split(',')
    print(l)
    ```
    or 空格分隔
    ```
    s = 'Tom 21 USA UCLA'
    l = s.split(' ')
    print(l)
    ```
    
    + 连接字符内容, join
    ```
    L = ['s', 'p', 'a', 'm', 'm', 'y']
    s = ''.join(L)
    print(s)
    ```
    or 指定分隔符
    ```
    L = ['s', 'p', 'a', 'm', 'm', 'y']
    s = '-'.join(L)
    print(s)
    ```
    
    + 去除空内容
    ```
    s = '    Tom 21 USA UCLA\n\n'
    print(s)
    print(s.strip())

    Tom 21 USA UCLA
    ```
    
- 格式化输出
    + normal 格式化输出
    ```
    name = '酱油哥'
    age = 28
    school = ['HUST','THU']
    s = 'name:{},age:{},and graduates from{}'.format(name,age,school)
    print(s)

    name:酱油哥,age:28,and graduates from['HUST', 'THU']
    ```
    
    >每一个花括号就是一个占位符，后面的变量依次进行对应，
    >最关键的是，这三个变量分别是不同的对象类型，甚至还有一个列表对象，
    >但是在字符串格式化时不需要我们对此进行任何的区分、处理。
    
    + 其他处理方式:
    ```
    template = '{1},{0} and {2}'
    s = template.format('spam', 'ham', 'eggs')
    print(s)

    ham,spam and eggs
    ```
    
    ```
    template = '{key1},{key2} and {key3}'
    s = template.format(key1 = 'spam', key2 = 'ham', key3 = 'eggs')
    print(s)

    spam,ham and eggs
    ```
    
    + 转义字符
    ```
    s = 's\tp\nam'
    print(s)

    s p
    Am
    ```
    
    + 关闭转义
    在字符串前增加"r", 即raw字符
    ```
    s = r'c:\new\test.py'
    print(s)
    ```
    
- 字符串转换
    + 转换为int
    ```
    s = '19'
    i = 3
    print(int(s) + i)
    ```
    + 转换为str
    ```
    s = '19'
    i = 3
    print(s + str(i))
    ```
    + 字符串, 浮点转换
    ```
    print(float('1.5'), str(4.56))
    ```
    
    
## 2 字符编码
字符编码的历史
## 3 字符编码转换
字符编码coding, decoding的过程

## 4 文件操作
文件操作的本质是针对文件中的每行数据进行字符串操作
- 文件操作
    + 针对文件做只读打开和可写打开;
    ```
    myfile = open('myfile.txt','w')
    myfile = open('myfile.txt','r')
    ```
   
    + 读取文件的每一行, 当返回空字符串(''), 则文件结束
    
    ```
    myfile = open('myfile.txt','r')
    
    >print(myfile.readline())
    >print(myfile.readline())
    >print(myfile.readline())
    
    >for line in myfile:
    >    print(line, end='')
    
    >print(myfile.read())
    ```
    + 关闭文件
    ```
    myfile.close()
    ```
    
## 5 循环及迭代
    
循环主要包含: for, while

### 5.1 while 循环
- 简单while循环
    ```
    a = 0
    b = 10
    while a < b:
        print(a, end=' ')
        a = a + 1

    0 1 2 3 4 5 6 7 8 9 
    ```
- while 循环中的控制: continus, break, else
    + continus循环控制; 跳出此次循环, 回主体继续新的开始
    ```
    a = 0
    b = 10
    while a < b:
        a = a + 1
        if a % 2 != 0:
            continue
        print(a, end=' ')
    ````
    + break循环控制; 直接跳出循环
    ```
    a = 0
    b = 10
    while a < b:
        a = a + 1
        if a == 5:
            break
        print(a, end=' ')

    1 2 3 4 
    ```
    + else关键字控制
    ```
    y = 29
    x = y // 2
    while x > 1:
        if y % x  == 0:
            print('{} has a factor {}'.format(y,x))
            break
        x = x - 1
    else:
        print('{} is prime'.format(y))
    ```
    
### 5.2 for 循环

- 列表循环

    ```
    for x in [1,2,3,4]:
    print(x, end=' ')
    ```
    
- 元组循环
    ```
    for x in ('i', 'am', 'a', 'teacher'):
    print(x,end=' ')
    ```
- 字典循环（1）
    ```
    D = {'a':1, 'b':2, 'c':3}
    for key in D:
        print(key, '--->', D[key])
    ```
- 字典循环（2）
    ```
    D = {'a': 1, 'b': 2, 'c': 3}
    for (key, value) in D.items():
        print(key, '--->', value)
    ```
- 文件读取循环
    ```
    file = open('myfile.txt', 'r')
        print(file.read())
    ```
- 文件读取循环
    ```
    for line in open('myfile.txt','r').readlines():
        print(line, end='')
    ```

- 文件读取
    ```
    for line in open ('myfile.txt','r'):
        print(line, end='')
    ```

### 5.3 多次迭代

```
1.使用迭代协议的逐项扫描工具可以称之为迭代环境
2.迭代环境还包含很多可以传入可迭代对象的内置方法
3.常用迭代环境：列表解析式
4.可迭代对象优势总结
```

主要是指再方法内迭代适用其他方法, 比如`print(tuple(open('myfile.txt')))`

## 6 生成器的使用

```
1.生成器函数的使用
2.生成器表达式的使用
3.与列表解析式的对比及对内存的优化
```

列表解析有很多有点, 但是如果整个列表非常大, 对内存消耗和压力很大, 可以将列表解析转换为生成器表达器.

列表解析是[ ]
生成器表达式时( )

生成器返回的是一个循环迭代;

简单举例:
```
def gen_squares(num):
    for x in range(num):
        yield x ** 2

G = gen_squares(5)
print(G)
print(iter(G))
print(next(G))
print(next(G))
print(next(G))
print(next(G))
```
或者使用for来展示:
```
def gen_squares(num):
    for x in range(num):
        yield x ** 2

for i in gen_squares(5):
    print(i, end=' ')
```

## 7 函数

### 7.1 函数的基本特征

- 是以def引导的一段可执行代码
- 函数也是对象, def创建了对象并做赋值
- 函数通过赋值语句(对象引用)传递
- 函数的多态性, 可以传递类型给函数, 也可以返回任意类型对象

例如: 可以将参数直接传入一个函数并赋予对象:
```
def func(x,y):
    return x * y

print(func(2,4))
```
也可以将函数直接赋值给另外一个对象, 然后再做参数传递
```
def func(a,b):
    return a+b

other_name = func
print(other_name(1,2))
```

### 7.2 函数的作用域

四个作用域:
- L 即本地作用域; 仅在函数内部生效的变量
- E 内嵌作用域
- G 全局作用域; 比如py等模块
- B 内置作用域; 比如print等;

关键需要注意: 如果需要global生效, 需要添加`global`关键字, 例如:
```
x = 88
def func():
    global x
    x = 99

func()
print(x)
```



