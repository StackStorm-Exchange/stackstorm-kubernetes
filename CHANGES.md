# Change Log

# 1.0.1

* Removed Backport ssl in favor of built in ssl.

## 1.0.0

* Drop Python 2.7 support

## 0.10.0
- Converted `kubernetes.register_tpr` workflow to Orquesta
  Contributed by Nick Maludy (@nmaludy Encore Technologies)

## 0.9.13
- Minor linting change

## 0.9.12
- Add resolution for query parameters on making API requests
- Add fallback for JSON decoding on API responses

## 0.9.11
- Fix issue with improper API address resolution
- Add port support

## 0.9.10
- Add schema documentation for bearer token authentication support

## 0.9.9

- Added bearer token authentication support

## 0.9.8

- Upgrade pyopenssl to resolve security vulnerabilities

## 0.9.7

- Fixed issue with use of certs for authentication

## 0.9.0

- New configuration options client_cert_path and client_cert_key_path
  allow client certs to be used for kubernetes authentication
- config_override now defined as a secret

## 0.7.0

- Actions no longer dynamically generate a client when run

## 0.6.0

- Updated action `runner_type` from `run-python` to `python-script`

