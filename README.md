# Introduction to Kubernetes: Lab Repository

Runnable examples for the "Introduction to Kubernetes" slide deck (44 slides). Each folder matches a section of the deck. Watch the slides first, then run the manifests and try things yourself.

## Requirements
- Docker (running), [kind](https://kind.sigs.k8s.io/docs/user/quick-start), `kubectl`
- minikube or the Docker Desktop cluster also work; only the cluster setup and Ingress differ.

## Quick start
```bash
make cluster                     # kind create cluster --config 00-setup/kind-config.yaml
kubectl get nodes                # STATUS: Ready
kubectl config current-context   # kind-lab
```

## Folders

| Folder | Deck topic | Files |
|---|---|---|
| `00-setup` | Local cluster | `kind-config.yaml`, `kind-multinode.yaml` |
| `01-pod` | Pod, lifecycle, probes | `pod.yaml`, `pod-probes.yaml`, `pod-liveness-fail.yaml` |
| `02-deployment` | ReplicaSet, Deployment, rollout | `deployment.yaml` |
| `03-service` | Labels, Service, DNS | `service.yaml`, `service-nodeport.yaml` |
| `04-ingress` | Ingress | `ingress.yaml` |
| `05-config-storage` | ConfigMap, Secret, PV/PVC | `configmap.yaml`, `pod-config-secret.yaml`, `pvc.yaml`, `pod-pvc.yaml` |
| `06-namespace-resources` | Namespace, requests/limits | `namespace.yaml`, `pod-oom.yaml` |
| `07-debug` | Debugging | `broken-*.yaml` (deliberately broken) |
| `08-lab` | The 8-step lab from the deck | `lab.md` |
| `CHEATSHEET.md` | Docker -> kubectl table, common commands | |

## Exercises by section

### 01 · Pod
```bash
kubectl apply -f 01-pod/pod.yaml
kubectl get pods                        # ContainerCreating -> Running
kubectl describe pod hello              # Events at the bottom: Scheduled, Pulling, Pulled, Started
kubectl port-forward pod/hello 8080:80  # open localhost:8080
kubectl delete pod hello                # nobody recreates it
```
**Probes:** apply `01-pod/pod-probes.yaml`; then apply `01-pod/pod-liveness-fail.yaml` and watch RESTARTS grow with `kubectl get pods -w`.
**Question:** What is the difference between a readiness and a liveness probe? Which one makes the container restart when it fails?

### 02 · Deployment and rollout
```bash
kubectl apply -f 02-deployment/deployment.yaml
kubectl get deploy,rs,pods
kubectl delete pod <POD_NAME>           # self-healing: a replacement appears within seconds
kubectl scale deployment web --replicas=5
kubectl set image deployment/web nginx=nginx:1.26-alpine
kubectl rollout status deployment/web
kubectl rollout history deployment/web
kubectl set image deployment/web nginx=nginx:no-such-tag   # a broken release
kubectl get pods                        # new Pod: ImagePullBackOff, old Pods still Running
kubectl rollout undo deployment/web
```
**Question:** Why was there no downtime when we pushed the broken image?

### 03 · Service and DNS
```bash
kubectl apply -f 03-service/service.yaml
kubectl get svc web
kubectl get endpoints web               # the Pod IPs are listed
kubectl run tmp --rm -it --image=busybox:1.36 --restart=Never -- wget -qO- http://web
kubectl port-forward svc/web 8080:80
```
**Question:** A Pod's IP changes when it is replaced. Why does the Service address stay the same?
**Try it:** run `kubectl scale deployment web --replicas=0` and check `kubectl get endpoints web`. Is it empty? Then scale back to 3.

### 04 · Ingress
```bash
make ingress                            # installs ingress-nginx (manifest from the kind guide)
kubectl apply -f 04-ingress/ingress.yaml
curl -H "Host: shop.example.com" http://localhost/
```
Ingress will not work if the cluster was not created with `kind-config.yaml`; continue with `port-forward` instead.

### 05 · ConfigMap, Secret, PVC
```bash
kubectl apply -f 05-config-storage/configmap.yaml
kubectl create secret generic db-pw --from-literal=password=change-me
kubectl apply -f 05-config-storage/pod-config-secret.yaml
kubectl exec config-demo -- env | grep -E "REDIS_HOST|DB_PASSWORD"
kubectl get secret db-pw -o jsonpath='{.data.password}' | base64 -d   # a Secret is only base64, not encrypted
# Persistence:
kubectl apply -f 05-config-storage/pvc.yaml -f 05-config-storage/pod-pvc.yaml
kubectl delete pod writer
kubectl apply -f 05-config-storage/pod-pvc.yaml
kubectl logs writer                     # two date lines: the data survived
```
The PVC may show `Pending` for a while: kind's StorageClass binds the volume once a Pod uses it.

### 06 · Namespace and resources
```bash
kubectl apply -f 06-namespace-resources/namespace.yaml
kubectl create deployment w --image=nginx:1.27-alpine --replicas=6 -n dev
kubectl get pods -n dev                 # the ResourceQuota blocks some Pods: kubectl describe rs -n dev
kubectl apply -f 06-namespace-resources/pod-oom.yaml
kubectl describe pod oom                # Last State: OOMKilled
```
Note: in a namespace with a quota, Pods without requests/limits can be rejected; read the message in `describe rs`.

### 07 · Debugging
Each file in `07-debug/` carries a different fault. Apply it, observe the symptom, find the cause with `get -> describe -> logs`, and fix it. Hints are in the comments at the top of each file.

### 08 · Lab
All 8 steps from the deck: `08-lab/lab.md`.

## Clean up
```bash
make clean-all
kind delete cluster --name lab
```

## Note
The manifests are derived from the examples in the deck and use the nginx image. If something fails, start with the **Events** section at the bottom of `kubectl describe`.
