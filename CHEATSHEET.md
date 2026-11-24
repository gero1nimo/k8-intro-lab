# Cheatsheet

## Docker -> kubectl
| Docker / Compose | kubectl |
|---|---|
| `docker run nginx` | `kubectl create deployment web --image=nginx` |
| `docker ps` | `kubectl get pods` |
| `docker logs web` | `kubectl logs POD` |
| `docker exec -it web sh` | `kubectl exec -it POD -- sh` |
| `docker rm -f web` | `kubectl delete pod POD` |
| `docker compose up -d` | `kubectl apply -f file.yaml` |
| `docker compose down` | `kubectl delete -f file.yaml` |
| `docker service scale web=6` | `kubectl scale deployment web --replicas=6` |

## Common commands
```bash
kubectl config get-contexts
kubectl get pods -o wide
kubectl describe pod NAME
kubectl logs NAME                 # -f to follow, --previous for the last container
kubectl exec -it NAME -- sh
kubectl get all -n NAMESPACE
kubectl rollout status|history|undo deployment/NAME
kubectl get endpoints SERVICE
```

## Debugging order
`get` (what state?) -> `describe` (Events at the bottom) -> `logs` (what did the app say?)

| Symptom | Likely cause |
|---|---|
| ImagePullBackOff | wrong image name or tag, registry access |
| CrashLoopBackOff | the app crashes on start: `logs --previous` |
| Pending | not enough resources (requests), PVC cannot bind |
| Service does not answer | selector and labels do not match: `get endpoints` is empty |
