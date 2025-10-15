## Generate API client module

```sh
docker run --rm -v "${PWD}/generated:/generated" openapitools/openapi-generator-cli generate \
    -i https://api-apimanager.insee.fr/portal/environments/DEFAULT/apis/2ba0e549-5587-3ef1-9082-99cd865de66f/pages/6548510e-c3e1-3099-be96-6edf02870699/content \
    -g python \
    --package-name sirene3 \
    -o /generated/openapi
```

## Local development

```sh
uv pip install --editable .
uv run -m crawl.main
```
