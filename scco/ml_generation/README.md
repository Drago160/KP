# ml_generation

This service is responsible for text generation using ML models.


## Functionality
* Generates text of a CO based on `client` messages.
* Sends generated text to the `pdf_generation` service.


## Files With Secrets
See in [README.md](ml_models/README.md) in `ml_modules` folder.


## API
Example of received data from `data_preprocessing` is located in `ml_generation/tests/ml_generation/steps/preproc/data/simple_input_data.json`.

Example of sending data to `pdf_generation` is located in `ml_generation/tests/ml_generation/steps/co_gen/data/simple_pdf_gen_pub.json`.


## CI
From `ml_generation` folder run:
```bash
docker build -t scco_test_ml_generation .
docker run --name scco_test_ml_generation scco_test_ml_generation pytest
```


## Handy
* Great `pytest` docs: https://habr.com/ru/articles/426699/
