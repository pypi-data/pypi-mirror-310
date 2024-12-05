# EZTopo

How to upload eztopo_utils package:
change setup.py version
python3 setup.py sdist
python3 setup.py bdist_wheel
python3 -m twine upload dist/\*
