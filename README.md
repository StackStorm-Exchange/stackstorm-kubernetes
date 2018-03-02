# Kubernetes Integration Pack

Pack which allows integration with [Kubernetes](https://kubernetes.io/) service.

This pack has been tested with kubernetes 1.4 and 1.5

# Current Status & Capabilities
Creates actions and sensors to interact with kubernetes through stackstorm
Listens for new third party resources, and dynamically creates new sensors for these
It does not create rules to match the generated sensors.
Actions can be created to react to third party resource addition/deletion (for example
create services in AWS through cloudformation)

This pack is mostly generated from the Kubernetes OpenAPI spec. There are several additional
actions, rules and sensors to facilitate dynamic third party resource management.

Action names are derived from OperationID's within the Kubernetes spec



## Configuration

Copy `kubernetes.yaml.example` to `/opt/stackstorm/configs/kubernetes.yaml`. It should contain something like this:
```yaml
user: "admin"
password: "password"
client_cert_path: "/path/to/cert.pem"
client_cert_key_path: "/path/to/cert.key"
kubernetes_api_url: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
verify: false

template_path: "/opt/stackstorm/packs/kubernetes/"
```
Where kubernetes_api_url = The FQDN to your Kubernetes API endpoint.

Only user and password or client_cert_path (key is optional) need to be set for this to work

Note: Currently SSL verification is turned off. This is a WIP.

All actions allow an optional 'config_override' argument which takes an object with any of the above
example:

```
{"kubernetes_api_url": "http://master.mydomain.kube", "user": "admin", "password": "password"}
```

**Note** : When modifying the configuration in `/opt/stackstorm/configs/` please
           remember to tell StackStorm to load these new values by running
           `st2ctl reload --register-configs`

## To install the Kubernetes Pack

```
st2 pack install kubernetes
```

### Kubernetes Specific Settings

The following must be enabled on Kubernetes API in ```kube-apiserver.yaml```

```yaml
--runtime-config=extensions/v1beta1/thirdpartyresources=true,extensions/v1beta1/deployments=true
```

Simply add the line above. kube-api container will automatically restart to accept the change.

### To test creating a namespace:

kubernetes.createCoreV1Namespace - set the body variable as

```
{"kind":"Namespace","apiVersion":"v1","metadata":{"name":"testing2","creationTimestamp":null},"spec":{},"status":{}}
```
