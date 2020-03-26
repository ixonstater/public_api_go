#!/bin/bash
#send build file

rsync ./server_builds/dist/*.whl ixonstater@codefordays.io:~/server_root/temp/
