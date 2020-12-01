# raelvaes
1. Authentication with the API itself -> Correct Username and Password
2. /access/<string:cloud-provider-name> -> to authenticate with cloud provider AWS, Azure or using SSH/k8s
3. /execute/platform -> Platform
4. /execute/station -> 
5. /journey/start



Notes :
1. First an authentication to the API with the username and the password
2. Securing authentication to the VM, either SSH or AWS or k8s(for now)
3. Executing platform is preparing a VM for task deployments by creating a new machine from cloud access keys. Nothing is to be done when platform is to be SSHed.
4. A station can have multiple platforms, platforms are VMs, so station is nothing but a bunch of VM that you wish to pack together in a group.
5. The journey will begin from start( for e.g. Station 1) till end (for e.g. Station 5).


# Mechanism to connect using SSH
1. Using username and password
2. Key based 
```
## 1. Username

    POST /access/ssh
    {
        "type": "user-based"
        "username": "ubuntu"
        "password" : {
            "type": "secure"
            "hash": _________
        }
        "password": "
    }
 ```
 # Architecture
 ![alt text] (<Architecture.png>)
