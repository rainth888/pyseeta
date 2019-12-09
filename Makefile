setup:
	@python setup.py install

run.demo: extract
	@python examples/test_opencv.py

extract:
	@cd models;unrar x seeta_fr_v1.0.part1.rar

clean:
	@find -name "*.pyc" -exec rm -f {} \;
	@find -name __pycache__ | xargs rm -rf
	@find -name .pytest_cache | xargs rm -rf
	@find -name build | xargs rm -rf
	@find -name dist | xargs rm -rf
	@rm models/seeta_fr_v1.0.bin

commit: clean
	@commit