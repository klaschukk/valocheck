---
name: run-pipeline
description: Run a data pipeline and validate results with data-validator agent
argument-hint: "[pipeline: atc|icd10|drugs|clinics|content|geo]"
allowed-tools: Read, Bash(python *), Bash(duckdb *), Glob, Grep
---

Запусти data pipeline и провалидируй результат.

## Аргумент
$ARGUMENTS — имя пайплайна: atc, icd10, drugs, clinics, content, geo

## Инструкции

### 1. Pre-flight check
- Проверь что скрипт существует: `data/pipelines/{name}_pipeline.py` или `scripts/pipelines/{name}_pipeline.py`
- Проверь зависимости (requirements)
- Покажи ожидаемый output: какой .db файл будет создан/обновлён

### 2. Запуск
- Выполни pipeline скрипт
- Логируй: время начала, время окончания, кол-во записей

### 3. Валидация (data-validator agent checklist)
- [ ] Таблица _metadata существует (version, build_date)
- [ ] Row count > 0 и в пределах ожидаемого
- [ ] Нет NULL в обязательных полях
- [ ] Primary keys уникальны
- [ ] Формат кодов валиден (ATC: буква+цифры, ICD-10: буква+цифры)
- [ ] UTF-8 корректность

### 4. Отчёт
```
## Pipeline: {name}
Status: OK / FAILED
Duration: {seconds}s
Records: {count}
DB file: data/dbs/{name}.db
Validation: {passed}/{total} checks

### Issues (if any)
- ...
```

## Пример
```
/run-pipeline atc
/run-pipeline drugs
```
