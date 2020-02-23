cd ..

#uninstall old build
./uninstall_old_build.sh

#create server code wheel
bin/python3 setup.py bdist_wheel

#install wheel in local venv
rm -r server_builds
mkdir server_builds
mv dist/ build/ code_for_days_server.egg-info/ server_builds
wheelname=$(ls server_builds/dist/*.whl)
bin/pip3 install $wheelname

#freeze package image into requirements.txt
./bin/pip3 freeze > requirements.txt