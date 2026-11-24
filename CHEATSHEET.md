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

## Sık kullanılanlar
```bash
kubectl config get-contexts
kubectl get pods -o wide
kubectl describe pod NAME
kubectl logs NAME                 # -f canlı, --previous önceki container
kubectl exec -it NAME -- sh
kubectl get all -n NAMESPACE
kubectl rollout status|history|undo deployment/NAME
kubectl get endpoints SERVICE
```

## Hata ayıklama sırası
`get` (durum ne?) -> `describe` (Events en altta) -> `logs` (uygulama ne dedi?)

| Belirti | Olası neden |
|---|---|
| ImagePullBackOff | imaj adı/etiketi yanlış, registry erişimi |
| CrashLoopBackOff | uygulama başlar başlamaz çöküyor: `logs --previous` |
| Pending | kaynak yetersiz (requests), PVC bağlanamadı |
| Service cevap vermiyor | selector-label uyumsuz: `get endpoints` boş |
