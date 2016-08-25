# Kubernetes sensor integration

Pack which allows integration with [Kubernetes](https://kubernetes.io/) service.

# Current Status & Capabilities
Creates a StackStorm Sensor (watch) on Kubernetes ThirdPartyResource API endpoint
Listens for new events. If 'ADDED', rule can pick up and create and AWS RDS database.

## Configuration

config.yaml includes:
```yaml
user: ""
password: ""
kubernetes_api_url: "https://kube_api_url"
extension_url: "/apis/extensions/v1beta1/watch/thirdpartyresources"
```
Where kube_api_url = The FQDN to your Kubernetes API endpoint.

Note: Currently SSL verification is turned off. This is a WIP.

## To setup the Kubernetes Pack
```
st2 run packs.setup_virtualenv packs=kubernetes
st2ctl reload
```

Note: AWS pack must be enabled and running


### Kubernetes Specific Settings

The following must be enabled on Kubernetes API in ```kube-apiserver.yaml```

```yaml
--runtime-config=extensions/v1beta1/thirdpartyresources=true,extensions/v1beta1/deployments=true
```

Simply add the line above. kube-api container will automatically restart to accept the change.



### To Test the RDS create event in the Kubernetes Pack

Create a yaml file with something like below:

```yaml
metadata:
  name: mysql-db31.example.com
  labels:
    resource: database
    object: mysql
apiVersion: extensions/v1beta1
kind: ThirdPartyResource
description: "A specification of database for mysql"
versions:
  - name: stable/v1
```

With kubectl run:

```
kubectl create -f name_of_your_file.yaml
```

### Deploying Mongo Replicaset in the Kubernetes Pack

First of all, do these 2 manual steps -

1. Add vault token to stackstorm:

  * Get your vault token from the kubernetes master as follows:

    ```
    [root@master-a ~]# echo "$(<vault_keys.txt)" | awk '/Initial/ {print $4}'
    eg22efe3-d7d6-acc1-3ac8-3c803892bc77a
    ```

  * now login to your stackstorm instance and add the vault token to /opt/stackstorm/packs/vault/config.yaml as follows:
    ```
    ---
    url: 'https://vault-prelive.pidah.prsn-dev.io'
    cert: ''
    token: 'eg22efe3-d7d6-acc1-3ac8-3c803892bc77a'
    verify: false
    ```

2. Add the public ip's of the stackstorm and vpc-nat instance to the VPC nat security group:

  * Get the public IP address of your stackstorm instance and the VPC nat instance via the AWS console.
  * Then add these two IP addresses to the vpc-nat security group `nat-sg-<environment name>` Inbound access to port 443 eg:
    ```
    nat-sg-pidah Inbound HTTPS 52.23.12.17/32
    ```

    _Note:_ These manual steps above would no longer be required when we move to dockerized stackstorm running directly on the PAAS ( or possibly Petsets ).

3. Create the mongo thirdparty resource:

  * Create a yaml file with something like below:

    ```yaml
    metadata:
        name: demo-mongo
        namespace: demo
        labels:
            type: mongo
            version: '2.6'
            template_filename: mongo.template
            stack_name: demo-mongo
    apiVersion: extensions/v1beta1
    kind: ThirdPartyResource
    description: ""
    versions:
      - name: stable/v1
    ```

  * With kubectl run:

    ```
    kubectl create -f name_of_your_file.yaml
    ```
