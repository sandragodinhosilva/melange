

set -ex



nosetests --verbosity=3 pygraphviz/tests
conda inspect linkages -p $PREFIX $PKG_NAME
exit 0
