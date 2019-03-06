#!/bin/bash
git add --all
git commit -a -m %1
git push gitlab LnDevel_gitlab
git push github LnDevel_github
