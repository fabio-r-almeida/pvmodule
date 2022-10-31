@RD /S /Q "./build"
timeout 2
@RD /S /Q "./dist"
timeout 2
@RD /S /Q "./pvmodule.egg-info"
timeout 2
python setup.py sdist bdist_wheel
twine upload dist/*
timeout 10

