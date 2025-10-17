
.PHONY: run test fmt lint

run:
	uvicorn aml_service_mapper.main:app --reload

test:
	pytest -q

fmt:
	python -m pip install black isort && black . && isort .

lint:
	python -m pip install ruff && ruff check .
