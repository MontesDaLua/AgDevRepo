#!/usr/bin/env sh

# check file
if [ ! -d ./py_src ]; then
  echo "./py_src not found. Please change directory to the project root that has a directory named py_src."
  exit
fi

echo "getting boostrap.py"
if [ -f "bootstrap.py" ]; then
  rm bootstrap.py
fi
if which wget &> /dev/null; then
  wget http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py
else
  curl http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py > bootstrap.py
fi
echo "running bootstrap.py"
python bootstrap.py --version=1.5.2 $*
echo "running buildout"
bin/buildout
echo "done"
