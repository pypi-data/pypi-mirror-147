# 修改file_client.py 中的base_url 为实际使用的

python3 setup.py sdist

# 上传到pypi
twine upload dist/*

pip3 install tyy-upload-1.0.0.tar.gz

