---
name: db-schema
description: Design or inspect DuckDB table schema for Benovite databases
argument-hint: "[action: design|show|migrate] [db: drugs|reference|clinics|geo|content]"
allowed-tools: Read, Write, Edit, Bash(python *), Bash(duckdb *)
---

Проектируй или покажи схему DuckDB таблиц.

## Аргументы
- $0 — действие: design (создать новую), show (показать существующую), migrate (пересоздать)
- $1 — база данных: drugs, reference, clinics, geo, content

## Инструкции

### design — проектирование новой схемы
1. Прочитай docs/02_data/pipeline_design.md для архитектуры
2. Прочитай docs/02_data/sources.md для источников данных
3. Определи таблицы и поля на основе:
   - URL архитектуры (какие данные нужны для рендеринга)
   - Schema.org (какие поля для JSON-LD)
   - Источников данных (какие поля доступны)
4. Создай SQL файл: `data/schemas/{db}_schema.sql`
5. Включи:
   - CREATE TABLE statements
   - Комментарии к каждой таблице и полю
   - _metadata таблица (version, build_date, source, row_count)
   - Индексы для частых queries
6. Покажи ER-диаграмму в текстовом виде

### show — показать существующую схему
1. Подключись к data/dbs/{db}.db
2. Покажи все таблицы, поля, типы, row counts
3. Покажи _metadata

### migrate — пересоздать схему
1. Покажи diff между текущей и новой схемой
2. Rebuild: drop + create (DuckDB = immutable, no ALTER)
3. Запусти pipeline для заполнения

## Правила
- DuckDB read-only в Flask — schema должна быть оптимизирована для SELECT
- Используй ENUM для фиксированных значений (lang codes, status)
- VARCHAR для текста, не TEXT (DuckDB convention)
- Обязательно: _metadata таблица в каждой .db

## Пример
```
/db-schema design drugs
/db-schema show reference
/db-schema design clinics
```
