#!/usr/bin/env python
# coding: utf-8

import git
import time

#repo = git.Repo.init(path='/home/pstreem/project/github')
repo = git.Repo('/home/pstreem/project/github')

print (repo.git.pull())
print (repo.git.add('.'))

date = time.ctime()
print (repo.git.commit('-m', date))

print (repo.git.push())