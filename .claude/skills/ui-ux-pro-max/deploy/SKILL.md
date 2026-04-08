---
name: deploy
description: Deploy Benovite to K8s via ArgoCD with pre-deploy checklist
argument-hint: "[tag: v1.0.0]"
allowed-tools: Read, Bash(git *), Bash(helm *), Bash(kubectl *), Bash(python *), Bash(pytest *), Bash(curl *)
---

Деплой Benovite на production через ArgoCD.

## Аргумент
$ARGUMENTS — git tag для деплоя (например: v1.0.0)

## Pre-deploy Checklist

### 1. Tests
- [ ] `pytest` — все тесты проходят
- [ ] Нет warnings

### 2. Build
- [ ] Docker image собирается без ошибок
- [ ] Image tagged: benovite:$ARGUMENTS

### 3. Code Quality
- [ ] git status — нет незакоммиченных изменений
- [ ] git log — последний коммит осмысленный

### 4. Data
- [ ] DuckDB файлы актуальны (проверить _metadata.build_date)
- [ ] Все необходимые .db файлы существуют

### 5. SEO Critical
- [ ] Sitemap генерируется
- [ ] Robots.txt корректен
- [ ] Health endpoint отвечает

### 6. Deploy
```bash
# Tag
git tag $ARGUMENTS
git push origin $ARGUMENTS

# ArgoCD auto-syncs on new tag
# Verify:
kubectl get pods -l app=benovite
kubectl logs -l app=benovite --tail=20
curl -s https://benovite.com/health/
```

### 7. Post-deploy
- [ ] Health check: 200 OK
- [ ] Smoke test: главная страница загружается
- [ ] Smoke test: drug page загружается
- [ ] GSC: нет новых ошибок
- [ ] Umami: трафик идёт

## Rollback
```bash
# If something breaks:
# ArgoCD: revert to previous tag
git tag -d $ARGUMENTS
git push origin :refs/tags/$ARGUMENTS
```

## Пример
```
/deploy v0.1.0
/deploy v1.0.0
```
