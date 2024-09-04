# Build stage

For every service `SERVICE_NAME` run:
```bash
echo $CI_REGISTRY_PASSWORD | docker login $CI_REGISTRY -u $CI_REGISTRY_USER --password-stdin
cd <PROJECT_ROOT>
./tests/ci/build_image.sh -p "$(pwd)" -s <SERVICE_NAME> -i scco_prod_<SERVICE_NAME>
docker push scco_prod_<SERVICE_NAME>
```

# Unit test stage

On `docker` image:
```bash
cd <PROJECT_ROOT>
./tests/ci/run_unit_tests.sh -p "$(pwd)" -s <SERVICE_NAME>
```

TODO: make tests to run on built images.
