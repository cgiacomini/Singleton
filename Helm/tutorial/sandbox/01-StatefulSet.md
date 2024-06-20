# Helm Chart for MongoDB Deployment as StatefulSet

MongoDB is a general-purpose, document-based NoSQL database program.  
As with other non-relational database management systems, MongoDB focuses on scalability and the speed of queries.

**This document describe how to create an helm chart from scratch to deploy and run a instance of MongoDB**

This deployment is purely for test purpose and is not adequate for a production.

## Step 1 - Label the Node
We have decided which node we should run the MongoDB instance on. 
Because we later may want to access the MongoDB instance from outside the kubernet cluster via and ingress, as for the other previous example we decide to run mongodb on a specifi kubernetes node.
We need then to force the instance to be deployed on the node of our choice. Here we dedicate the *k8s-master* node for this. 
We need then to give the *k8s-master* node a label as we did for previous examples for doker-registry and ingress controller.
```
$ kubectl get nodes --show-labels
$ kubectl get nodes --show-labels

NAME         STATUS   ROLES           AGE    VERSION   LABELS
k8s-master   Ready    control-plane   321d   v1.25.3   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=k8s-master,kubernetes.io/os=linux,node-role.kubernetes.io/control-plane=,node.kubernetes.io/exclude-from-external-load-b
alancers=,run-dashboard=true,run-docker-registry=true,run-ingress-controller=true
k8s-node1    Ready    <none>          321d   v1.25.3   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=k8s-node1,kubernetes.io/os=linux
k8s-node2    Ready    <none>          321d   v1.25.3   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=k8s-node2,kubernetes.io/os=linux

$ kubectl label nodes k8s-master run-mongodb=true
node/k8s-master labeled

$ kubectl get nodes --show-labels
NAME         STATUS   ROLES           AGE    VERSION   LABELS
k8s-master   Ready    control-plane   321d   v1.25.3   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=k8s-master,kubernetes.io/os=linux,node-role.kubernetes.io/control-plane=,node.kubernetes.io/exclude-from-external-load-b
alancers=,run-dashboard=true,run-docker-registry=true,run-ingress-controller=true,run-mongodb=true
k8s-node1    Ready    <none>          321d   v1.25.3   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=k8s-node1,kubernetes.io/os=linux
k8s-node2    Ready    <none>          321d   v1.25.3   beta.kubernetes.io/arch=amd64,beta.kubernetes.io/os=linux,kubernetes.io/arch=amd64,kubernetes.io/hostname=k8s-node2,kubernetes.io/os=linux
```

## Step 2 - Create a Storage Class
A storage class in Kubernetes defines different storage types, which allows the user to request a specific type of storage for their workloads.
With storage class we provide a dynamic storage provisioning.  
Dynamic storage provisioning is the process of automatically allocating storage to containers in a Kubernetes cluster. This is done automatically by the Kubernetes control plane when it detects that a container needs storage.
The control plane will select a storage class based on the container’s requirements, then automatically create a new persistent volume using that storage class.  
After that, as in static provisioning, the PV is attached to the container, and the container can use the storage via a PVC.

Here we define a local storage class specific for MongoDB. (*Note*: provisioner: kubernetes.io/no-provisioner)

### StorageClass.yaml 
```
kind: StorageClass
apiVersion: storage.k8s.io/v1
metadata:
  name: mongodb-storageclass
provisioner: kubernetes.io/no-provisioner
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
```

## Step 3 - Create Persistent Storage (PV and PVC)
Here we define a PersistentVolume which define a piece of storage of the given StorageClass. When a POD require a a persistent storage it can claim it via a PersistentStorageClaim.
### PersistentStorager.yaml
```
apiVersion: v1
kind: PersistentVolume
metadata:
    name: mongodb-pv
spec:
  capacity:
    storage: 2Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  storageClassName: mongodb-storageclass
  local:
    path: /mnt/data
  nodeAffinity:
    required:
      nodeSelectorTerms:
      - matchExpressions:
        - key: run-mongodb
          operator: In
          values:
            - true
```
+ ***capacity***: For this storage we request 2 gibibytes
+ ***volumeMode***: Here we request to use a normal *filesystem* instead of *block*
+ ***accessMode***: *ReadWriteOnce* mien that th volume can be mounted in Read/Write mode only by a single node.
+ ***persistentVolumeReclaimPolicy***: *Retain* (default) means that the data will still be there once the claim has been deleted.
+ ***storageClassName***: here we reffer to the previously create storage class *mongodb-storageclass*
+ ***local***: define the **path** of the volume on the node. ( The dedicated node were we run MongoDB should have this path **/mnt/data** if not we need to create it directly on the node.
+ ***nodeAffinity***: here we simply tell which nodes can access the volume. In this case the nodes labeled *run-mongod:true*

Later we could change the PersistentVolume to use the shared nfs as we did in other examples.

### PersistentVolumeClaim.yaml
```
kind: PersistentVolumeClaim
apiVersion: v1
metadata:
  name: mongodb-pvc
spec:
  storageClassName: mongodb-storageclass
  accessModes:
    - ReadWriteOnce
  volumeMode: Filesystem
  resources:
    requests:
      storage: 1Gi
```

Here we instruct Kubernetes to claim volumes belonging to mongodb-storageclass. In particular we claim 1 gibibytes of the two provide by teh PersistentVolume.


## Step 4 - Step 4: Create a ConfigMap
The config map here defines two MongoDB configuration files **mongo.conf** and **ensure-users.json**.  
These two files will then be mounted as volumes by the deployed mongodb POD.

***Note***: **/etc/k8-test** will be the mount point of the secrete containing the username and password.

### ConfigMap.yaml
```
apiVersion: v1
kind: ConfigMap
metadata:
  name: mongodb-configmap
data:
  mongo.conf: |
    storage:
      dbPath: /data/db
  ensure-users.js: |
    const targetDbStr = 'test';
    const rootUser = cat('/etc/k8-test/admin/MONGO_ROOT_USERNAME');
    const rootPass = cat('/etc/k8-test/admin/MONGO_ROOT_PASSWORD');
    const usersStr = cat('/etc/k8-test/MONGO_USERS_LIST');

    const adminDb = db.getSiblingDB('admin');
    adminDb.auth(rootUser, rootPass);
    print('Successfully authenticated admin user');

    const targetDb = db.getSiblingDB(targetDbStr);

    const customRoles = adminDb
      .getRoles({rolesInfo: 1, showBuiltinRoles: false})
      .map(role => role.role)
      .filter(Boolean);

    usersStr
      .trim()
      .split(';')
      .map(s => s.split(':'))
      .forEach(user => {
        const username = user[0];
        const rolesStr = user[1];
        const password = user[2];

        if (!rolesStr || !password) {
          return;
        }

        const roles = rolesStr.split(',');
        const userDoc = {
          user: username,
          pwd: password,
        };

        userDoc.roles = roles.map(role => {
          if (!~customRoles.indexOf(role)) {
            return role;
          }
          return {role: role, db: 'admin'}; 
        });

        try {
          targetDb.createUser(userDoc);
        } catch (err) {
          if (!~err.message.toLowerCase().indexOf('duplicate')) {
            throw err;
          }
        }
      });
```

## Step 5: Create a Secret

The secret defined here defines some key/value data that will be mounted as files by the below *StatufulSet*. Each key will be a file and the value its content.

### Secret.yaml
```
apiVersion: v1
kind: Secret
metadata:
  name: mongodb-secret
type: Opaque
data:
  MONGO_ROOT_USERNAME: YWRtaW4K
  MONGO_ROOT_PASSWORD: cGFzc3dvcmQK
  MONGO_USERNAME: dGVzdAo=
  MONGO_PASSWORD: cGFzc3dvcmQK
  MONGO_USERS_LIST: dGVzdDpkYkFkbWluLHJlYWRXcml0ZTpwYXNzd29yZAo=
```

# Step 6 - Create a MongoDB Service

Here we create a ***headless*** service.

These are the types of Kubernetes Service

+ ***ClusterIP*** (default): Internal clients send requests to a stable internal IP address.
+ ***NodePort***: Clients send requests to the IP address of a node on one or more nodePort values that are specified by the Service.
+ ***LoadBalancer***: Clients send requests to the IP address of a network load balancer.
+ ***ExternalName***: Internal clients use the DNS name of a Service as an alias for an external DNS name.

While there are four official types of Kubernetes service (by definition) there is one more type of service which is the **Headless Service**.
Kubernetes headless service is a Kubernetes service that does not assign an IP address to itself. Insted it returns the IP addresses of the pods associated with it.
Kubernetes still create DNS records for the service and each endpoint, when doing a nslookup of the service,  ***Kubernetes will return the POD's IP address instead.***

Technically Headless service is of *type ClusterIP* with property **clusterIP: Node** .


### Service.yaml
```
apiVersion: v1
kind: Service
metadata:
  name: mongodb-test
  labels:
    app: database
spec:
  clusterIP: None
  selector:
    app: database
```


## Step 7: Create a StatefulSet


***StatefulSets***  are valuable for applications that require:
  + Stable, unique network identifiers.
  + Stable, persistent storage.
  + Ordered, graceful deployment and scaling.
  + Ordered, automated rolling updates.

Stable : persistence across Pod (re)scheduling.


A *StatefulSet* is a Kubernetes controller that is used to manage and maintain one or more Pods. However, so do other controllers like *ReplicaSet* and, the more robust, *Deployment*. 
+ *Stateless Application*: Is one that does not care which network it is using, and it does not need permanent storage
+ *Statefull Application*: Tipically application that cares about its state, such databases application, where heach pod can reach each other through a unique identity that does not change (hostnames, IPs…etc.)

+ For a StatefulSet with n replicas, when Pods are being deployed, they are created sequentially, ordered from {0..n-1}. In our case we only have one replica but we can still see the the deployed POD will have name **mongodb-test-0**.
+ Each Pod has a stable hostname based on its ordinal index. I our case once deployed we can see that the service is pointing to *mongodb-test-0.mongodb-test.sandbox.svc.cluster.local* but in case of more replicas we will have a DNS record for each MongoDB instance.


```
$ kubectl exec mongodb-test-0 -- sh -c "hostname"
mongodb-test-0
```
*  The DNS record for the service (SRV) will point to the host providing the service, in our case :
```
$ kubectl run -i --tty --image busybox:1.28 dns-test --restart=Never --rm
If you don't see a command prompt, try pressing enter.
/ # nslookup mongodb-test
Server:    10.96.0.10
Address 1: 10.96.0.10 kube-dns.kube-system.svc.cluster.local

Name:      mongodb-test
Address 1: 10.10.0.172 mongodb-test-0.mongodb-test.sandbox.svc.cluster.local
```

### StatefulSet.yaml

```
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: mongodb-test
spec:
  serviceName: mongodb-test
  replicas: 2
  selector:
    matchLabels:
      app: database
  template:
    metadata:
      labels:
        app: database
        selector: mongodb-test
    spec:
      containers:
      - name: mongodb-test
        image: mongo:4.0.8
        env:
          - name: MONGO_INITDB_ROOT_USERNAME_FILE
            value: /etc/k8-test/admin/MONGO_ROOT_USERNAME
          - name: MONGO_INITDB_ROOT_PASSWORD_FILE
            value: /etc/k8-test/admin/MONGO_ROOT_PASSWORD
        volumeMounts:
        - name: k8-test
          mountPath: /etc/k8-test
          readOnly: true
        - name: mongodb-scripts
          mountPath: /docker-entrypoint-initdb.d
          readOnly: true
        - name: mongodb-configmap
          mountPath: /config
          readOnly: true
        - name: mongodb-data
          mountPath: /data/db
      nodeSelector:
        run-mongodb: true
      volumes:
      - name: k8-test
        secret:
          secretName: mongodb-secret
          items:
          - key: MONGO_ROOT_USERNAME
            path: admin/MONGO_ROOT_USERNAME
            mode: 0444
          - key: MONGO_ROOT_PASSWORD
            path: admin/MONGO_ROOT_PASSWORD
            mode: 0444
          - key: MONGO_USERNAME
            path: MONGO_USERNAME
            mode: 0444
          - key: MONGO_PASSWORD
            path: MONGO_PASSWORD
            mode: 0444
          - key: MONGO_USERS_LIST
            path: MONGO_USERS_LIST
            mode: 0444
      - name: mongodb-scripts
        configMap:
          name: mongodb-configmap
          items:
          - key: ensure-users.js
            path: ensure-users.js
      - name: mongodb-configmap
        configMap:
          name: mongodb-configmap
          items:
          - key: mongo.conf
            path: mongo.conf
      - name: mongodb-data
        persistentVolumeClaim:
          claimName: mongodb-pvc
```

***NOTE***: As explainded before here we 
+ mount the secret keys / values individually inside **/etc/k8-test** as readonly
+ mount the configmap data **ensure-users.js** as **/docker-entrypoint-initdb.d**
+ mount *mongo.conf* as **/config/mongo.conf**
+ mount the local filestem /mnt/data of the designeted node (k8s-master) as **data/db**


## Step 8 - Deployment

* We would like to be able to deploy the MongoDb instance via helm, for this we ask helm chart structure manuallu.
```
$ mkdir -p mongodb-chart/templates
$ mkdir -p mongodb-chart/charts
$ echo "" > mongodb-chart/values.yaml
```
* Create the *mongodb-chart/Chart.yaml* file with the folowing content:
```
apiVersion: v2
name: mongodb-chart
description: A Helm chart for Kubernetes

# Chart Type
type: application

# Chart Version
version: 0.1.0

# Application Version
appVersion: "1.16.0"

```
* Created the above described manifests file inside *mongodb-test/templates* directory.  At the end we will have the following structure :
```
$ tree mongodb-chart/
mongodb-chart/
├── Chart.yaml
├── charts
├── templates
│   ├── ConfigMap.yaml
│   ├── PersistentVolume.yaml
│   ├── PersistentVolumeClaim.yaml
│   ├── Secret.yaml
│   ├── Service.yaml
│   ├── StatefulSet.yaml
│   └── StorageClass.yaml
└── values.yaml
```

* Deploy the chart using helm
```
$ helm install mongodb mongodb-chart/
NAME: mongodb
LAST DEPLOYED: Tue Sep  5 15:48:25 2023
NAMESPACE: sandbox
STATUS: deployed
REVISION: 1
TEST SUITE: None

cgiacomini@NCEL143449 ~/GitHub/HelmDoc/sandbox
$ kubectl get pods
NAME             READY   STATUS    RESTARTS   AGE
mongodb-test-0   1/1     Running   0          
```
## Step 9 - Test mongodb Standalone Instance

+ To test if MongoDb deployment is working as expected we connect to the instance and we run the mongo client *mongo*
```
$ kubectl exec -it mongodb-test-0 -- sh

# mongo
MongoDB shell version v4.0.8
connecting to: mongodb://127.0.0.1:27017/?gssapiServiceName=mongodb
Implicit session: session { "id" : UUID("0dd1dbf3-43f3-48e2-8844-dd010b7fe586") }
MongoDB server version: 4.0.8
Welcome to the MongoDB shell.
For interactive help, type "help".
For more comprehensive documentation, see
        http://docs.mongodb.org/
Questions? Try the support group
        http://groups.google.com/group/mongodb-user
> 
> uset test> uset test
switched to db test
>
> db.auth('test','password')
1
>
```
Number 1 in the output confirms the successful authentication.

