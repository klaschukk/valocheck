---
name: check-i18n
description: Check internationalization completeness for a language
argument-hint: "[lang-code: en|es|de|fr|ru|ar|zh|...]"
allowed-tools: Read, Grep, Glob, Bash(python *), Bash(duckdb *)
---

Проверь полноту интернационализации для указанного языка.

## Аргумент
$ARGUMENTS — ISO 639-1 код языка (en, es, de, fr, ru, ar, zh, ...)

## Инструкции

### 1. UI переводы (gettext)
- Проверь файл: `translations/{lang}/LC_MESSAGES/messages.po`
- Посчитай: всего строк, переведённых, пустых (fuzzy/untranslated)
- Покажи процент завершённости

### 2. Контент (content.db)
- Посчитай страницы с контентом на этом языке
- Сравни с EN (baseline): сколько процентов переведено
- Покажи по типам: drugs, conditions, atc

### 3. Slugs
- Проверь что slug-и генерируются для этого языка
- Для RTL языков (ar, he, fa): проверь транслитерацию

### 4. Hreflang
- Проверь что шаблоны включают этот язык в hreflang
- Проверь sitemap для этого языка

### 5. Locale formatting
- Числа: проверь формат (1,000.50 vs 1.000,50)
- Даты: проверь формат
- Для RTL: проверь dir="rtl" в шаблонах

### 6. Отчёт
```
## i18n Check: {lang}

### UI Translations
- Total: {n} strings
- Translated: {n} ({percent}%)
- Missing: {n}

### Content Coverage
| Type | EN (baseline) | {lang} | Coverage |
|------|--------------|--------|----------|
| Drugs | X | Y | Z% |
| Conditions | X | Y | Z% |
| ATC | X | Y | Z% |

### Issues
- ...

### Recommendations
- ...
```

## Пример
```
/check-i18n es
/check-i18n ar
/check-i18n de
```
