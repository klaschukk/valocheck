---
name: analyze-seo
description: Analyze SEO quality of a Benovite page template or URL pattern
argument-hint: "[template-path or url-pattern]"
allowed-tools: Read, Grep, Glob, Bash(curl *), Bash(python *)
---

Проанализируй SEO-качество страницы или шаблона Benovite.

## Аргумент
$ARGUMENTS — путь к Jinja2 шаблону или URL паттерн (например: app/templates/drug.html)

## Инструкции

1. Прочитай шаблон/файл
2. Прочитай .claude/rules/seo.md для правил
3. Прочитай docs/04_seo/schema_markup.md для JSON-LD требований
4. Проверь каждый пункт:

### Technical SEO Checklist
- [ ] `<title>` — уникальный, содержит ключевое слово, < 60 символов
- [ ] `<meta name="description">` — уникальный, 120-160 символов
- [ ] `<h1>` — ровно один, содержит ключевое слово
- [ ] Hreflang теги — все языки + x-default
- [ ] Canonical — self-referencing
- [ ] JSON-LD schema — правильный тип (Drug/Physician/MedicalCondition)
- [ ] BreadcrumbList schema
- [ ] Open Graph теги (og:title, og:description, og:image)
- [ ] Изображения: alt text, lazy loading
- [ ] Internal links: минимум 3 релевантных ссылки
- [ ] Medical disclaimer блок

### Content SEO
- [ ] Keyword в первых 100 словах
- [ ] Подзаголовки (H2/H3) содержат вариации ключевого слова
- [ ] Нет thin content (минимум 300 слов)
- [ ] Source attribution

5. Покажи отчёт: что ОК, что нужно исправить, приоритет

## Формат вывода
```
## SEO Audit: {template}

Score: {X}/12

### OK
- ...

### Needs Fix (priority)
1. ...

### Recommendations
- ...
```
