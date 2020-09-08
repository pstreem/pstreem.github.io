#!/usr/bin/env python
# coding: utf-8

import git
import time

#repo = git.Repo.init(path='/home/pstreem/project/github')
repo = git.Repo('/home/pstreem/project/github')

print (repo.git.add('.'))

print (repo.git.pull())

date = time.ctime()
commit_comment = '-m \"'+date+'\"'
#print (repo.git.commit(commit_comment))
print (repo.git.commit('-m', date))

print (repo.git.push())
