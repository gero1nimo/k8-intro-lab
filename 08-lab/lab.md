# Lab: 8 adım (sunumdaki "Lab" slaytı)

`POD_ADI` yerine `kubectl get pods` çıktısındaki gerçek adı yaz.

| Adım | Komut | Beklenen |
|---|---|---|
| 1 · Küme | `make cluster` | `kubectl get nodes` Ready |
| 2 · Deploy | `kubectl create deployment web --image=nginx:1.27-alpine` | `deployment.apps/web created` |
| 3 · Expose | `kubectl expose deployment web --port=80` | `kubectl get svc web` |
| 4 · Reach it | `kubectl port-forward svc/web 8080:80` | tarayıcıda localhost:8080 nginx sayfası |
| 5 · Scale | `kubectl scale deployment web --replicas=4` | 4 Pod Running |
| 6 · Self-heal | `kubectl delete pod POD_ADI` (başka terminalde `kubectl get pods -w`) | yeni Pod kendiliğinden açılır |
| 7 · Break and roll back | `kubectl set image deployment/web nginx=nginx:does-not-exist` | yeni Pod ErrImagePull, sonra ImagePullBackOff; eskiler hizmet vermeye devam eder |
| | `kubectl rollout undo deployment/web` | önceki sürüme dönülür |
| 8 · Clean up | `kubectl delete deployment,svc web` | |

Container adı `nginx`'tir çünkü `create deployment` adı imajdan türetir.

## Bonus: bildirimsel yol
```bash
kubectl apply -f 02-deployment/deployment.yaml -f 03-service/service.yaml
kubectl delete -f 03-service/service.yaml -f 02-deployment/deployment.yaml
```

## Kontrol soruları
1. Pod IP'leri değişirken Service adresi neden sabit kalır?
2. Service hangi Pod'lara trafik göndereceğini nasıl bilir?
3. Aynı namespace'ten bir Service'e hangi DNS adıyla ulaşılır?
4. Service çalışmıyorsa ilk hangi iki şeyi kontrol edersin?

Cevaplar: 1) Service sabit bir sanal adres ve DNS adı sağlar. 2) Label selector ve hazır (ready) Pod'lar. 3) `web` (ya da `web.default`). 4) selector-label eşleşmesi ve `kubectl get endpoints`.
