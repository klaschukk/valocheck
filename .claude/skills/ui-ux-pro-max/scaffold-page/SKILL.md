---
name: scaffold-page
description: Scaffold Flask route + Jinja2 template + JSON-LD + test for a new page type
argument-hint: "[page-type: drug|atc|condition|doctor|clinic|compare|static]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(python *), Bash(pytest *)
---

Создай полный scaffold для нового типа страницы Benovite.

## Аргумент
$ARGUMENTS — тип страницы: drug, atc, condition, doctor, clinic, compare, static

## Что создать

### 1. Flask Route
Файл: `app/routes/{type}.py`
- Blueprint с prefix из url_architecture.md
- Функция view: query DuckDB, prepare context, render template
- JSON-LD schema builder для этого типа
- Hreflang generation

### 2. Jinja2 Template
Файл: `app/templates/{type}.html`
- Extends base.html
- Все секции из docs/03_product/page_templates.md для этого типа
- Medical disclaimer block
- Breadcrumbs
- JSON-LD script tag
- Hreflang link tags
- Open Graph meta tags

### 3. JSON-LD Builder
Файл: `app/schema/{type}_schema.py`
- Функция build_{type}_schema() -> dict
- По шаблону из docs/04_seo/schema_markup.md

### 4. Test
Файл: `tests/test_{type}_page.py`
- Test: route returns 200
- Test: has h1, title, meta description
- Test: has JSON-LD
- Test: has medical disclaimer
- Test: has hreflang

## Правила
- Прочитай .claude/rules/seo.md и .claude/rules/medical-content.md
- Прочитай docs/03_product/page_templates.md для секций
- Прочитай docs/04_seo/schema_markup.md для JSON-LD
- Прочитай docs/03_product/url_architecture.md для URL паттерна
- Используй type hints, PEP 8, 120 chars max

## Пример
```
/scaffold-page drug
/scaffold-page condition
/scaffold-page doctor
```
