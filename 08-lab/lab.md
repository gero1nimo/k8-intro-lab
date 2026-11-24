# Lab: 8 steps (the "Lab" slide in the deck)

Replace `POD_NAME` with the real name from `kubectl get pods`.

| Step | Command | Expected |
|---|---|---|
| 1 · Cluster | `kind create cluster --config 00-setup/kind-config.yaml` | `kubectl get nodes` shows Ready |
| 2 · Deploy | `kubectl create deployment web --image=nginx:1.27-alpine` | `deployment.apps/web created` |
| 3 · Expose | `kubectl expose deployment web --port=80` | `kubectl get svc web` |
| 4 · Reach it | `kubectl port-forward svc/web 8080:80` | the nginx page at localhost:8080 |
| 5 · Scale | `kubectl scale deployment web --replicas=4` | 4 Pods Running |
| 6 · Self-heal | `kubectl delete pod POD_NAME` (in another terminal: `kubectl get pods -w`) | a new Pod appears on its own |
| 7 · Break and roll back | `kubectl set image deployment/web nginx=nginx:does-not-exist` | new Pod: ErrImagePull, then ImagePullBackOff; old Pods keep serving |
| | `kubectl rollout undo deployment/web` | back to the previous version |
| 8 · Clean up | `kubectl delete deployment,svc web` | |

The container is named `nginx` because `create deployment` derives the name from the image.

## Bonus: the declarative way
```bash
kubectl apply -f 02-deployment/deployment.yaml -f 03-service/service.yaml
kubectl delete -f 03-service/service.yaml -f 02-deployment/deployment.yaml
```

## Check yourself
1. Why does the Service address stay the same while Pod IPs change?
2. How does a Service know which Pods to send traffic to?
3. What DNS name reaches a Service from the same namespace?
4. If a Service does not work, which two things do you check first?

Answers: 1) A Service provides a stable virtual address and DNS name. 2) Its label selector and the Pods that are ready. 3) `web` (or `web.default`). 4) That the selector matches the Pod labels, and `kubectl get endpoints`.
