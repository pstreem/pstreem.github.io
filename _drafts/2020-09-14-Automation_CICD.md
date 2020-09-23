---
title: 自动化测试及DevOps
date: 2020-09-14 20:32:20
tags: [Python, Automation]
---

自动化测试的一些记录过程;

# Robot Framework 框架

## 在FreeBSD下构建Robot Environment

采用标准包管理方式直接构建robot环境:
>pkg install py37-robotframework

系统会自动安装依赖的包, 比如Python3.7等;



## 创建第一个Robot 测试用例

```python
*** Settings ***

Documentation	Example using the test cases
Library		SeleniumLibrary
Library		OperatingSystem
Library		Collections
Library		RequestsLibrary

#Suite Setup	Get Auth Token
#Suite Teardown	Delete All Sessions

Default tags	HL

*** Variables ***
${MESSAGE}    Hello,Wrold!
${UNAME}      PstreeM
${PASSWORD}   password

*** Test Cases ***
Case Test1
     [Tags]	newcase
     Log	${MESSAGE}
     Self Keyword	/tmp
      
Case Test2
      [Tags]	HL
      Should Be Equal	${MESSAGE} Hello,World!
      Log	message it's right

*** Keywords ***

Self Keyword
     [Arguments]	${path}
     Directory Should Exist	${path}
```



逐一解释:

| Paramater  | Description                                         |
| ---------- | --------------------------------------------------- |
| Settings   | 是针对测试用例的前期设置, 包含调用的库, 环境设置等; |
| Variables  | 针对变量的设定, 在测试case中会用到;                 |
| Test Cases | 编写的测试用例                                      |
| Keywords   | 设置的关键字                                        |

