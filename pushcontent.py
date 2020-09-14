#!/usr/bin/env python
# coding: utf-8

import git
import time

#repo = git.Repo.init(path='/home/pstreem/project/github')
repo = git.Repo('/home/pstreem/project/github')

pull_info = repo.git.pull()

add_info = repo.git.add('.')

date = time.ctime()

commit_info = repo.git.commit('-m', date)
push_info = repo.git.push()

log_file = open('push.log','w',encoding='utf-8')
log_file.write(commit_info)
log_file.write(pull_info)
log_file.write(add_info)
log_file.write(push_info)
log_file.write('\n')
log_file.close()
