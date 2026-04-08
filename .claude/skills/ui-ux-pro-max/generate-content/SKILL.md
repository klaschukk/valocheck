---
name: generate-content
description: Generate medical content for Benovite pages using Claude API prompts
argument-hint: "[page-type] [entity]"
allowed-tools: Read, Grep, Bash(python *)
---

Сгенерируй контент для страницы Benovite.

## Аргументы
- `$0` — тип страницы: drug, condition, atc, doctor, comparison
- `$1` — сущность: название препарата, ICD-код, ATC-код, и т.д.

## Инструкции

1. Прочитай docs/00_strategy/content_strategy.md для промпт-шаблонов
2. Прочитай .claude/rules/medical-content.md для YMYL-правил
3. Определи тип контента по аргументу $0
4. Собери данные из DuckDB (если доступен) или покажи какие данные нужны
5. Сгенерируй контент по шаблону:
   - Структурированные данные (из БД)
   - Описательный текст (по промпту из content_strategy.md)
   - Source attribution
   - Medical disclaimer
6. Проверь quality checklist:
   - [ ] Длина 300-500 слов
   - [ ] Есть source attribution
   - [ ] Нет medical advice фраз
   - [ ] Нет hallucinated данных
   - [ ] Правильный язык
7. Покажи готовый контент

## Пример
```
/generate-content drug ibuprofen
/generate-content condition essential-hypertension
/generate-content atc M01AE01
```
