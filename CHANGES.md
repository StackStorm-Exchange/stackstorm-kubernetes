# Change Log

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

