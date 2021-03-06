setup:
	@python setup.py install

run.demo: extract
	@python examples/test_opencv.py

run.web.app:
	@python examples/test_web.py

test.web.app:
	@if [ ! -d "examples/uploads" ]; then mkdir -p examples/uploads; fi
	@python examples/test_rest.py

test.rest:
	@curl -F "file1=@data/1.jpg" -F "file2=@data/2.jpeg" http://0.0.0.0:5000/face_match

extract:
	@cd models;unrar x seeta_fr_v1.0.part1.rar

clean:
	@find -name "*.pyc" -exec rm -f {} \;
	@find -name __pycache__ | xargs rm -rf
	@find -name .pytest_cache | xargs rm -rf
	@find -name build | xargs rm -rf
	@find -name dist | xargs rm -rf
	@if [ -f "models/seeta_fr_v1.0.bin" ]; then rm models/seeta_fr_v1.0.bin; fi
	@find -name pyseeta.egg-info | xargs rm -rf

commit: clean
	@commit