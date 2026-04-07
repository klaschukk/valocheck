# Design System — ValoCheck

## Theme

Dark gaming aesthetic inspired by Valorant's visual identity. Mobile-first, clean, fast.

## Colors

### Core
| Variable | Value | Usage |
|----------|-------|-------|
| `--bg` | `#0f1923` | Page background |
| `--bg-surface` | `#1a2634` | Cards, header, footer |
| `--bg-card` | `#1f2f3f` | Elevated cards, badges |
| `--bg-hover` | `#253545` | Hover states |
| `--primary` | `#ff4655` | Valorant red — CTAs, logo, errors |
| `--accent` | `#00ffc2` | Teal — links, stat values, highlights |
| `--text` | `#ece8e1` | Primary text |
| `--text-muted` | `#768a9e` | Secondary text |
| `--text-dim` | `#4a5e70` | Tertiary text, timestamps |
| `--border` | `#2a3a4a` | Borders, dividers |

### Semantic
| Variable | Value | Usage |
|----------|-------|-------|
| `--win` | `#2dbe6c` | Win indicators |
| `--loss` | `#ff4655` | Loss indicators |
| `--positive` | `#2dbe6c` | Positive K/D diff |
| `--negative` | `#ff4655` | Negative K/D diff |

### Rank Colors
| Variable | Value | Rank |
|----------|-------|------|
| `--rank-iron` | `#5e5e5e` | Iron |
| `--rank-bronze` | `#a8733e` | Bronze |
| `--rank-silver` | `#c0c0c0` | Silver |
| `--rank-gold` | `#e8c858` | Gold |
| `--rank-platinum` | `#3eb8b0` | Platinum |
| `--rank-diamond` | `#b489c4` | Diamond |
| `--rank-ascendant` | `#2dbe6c` | Ascendant |
| `--rank-immortal` | `#ff4655` | Immortal |
| `--rank-radiant` | `#fce97c` | Radiant |

## Typography

- Font: system stack (`-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`)
- Base size: 16px
- Line height: 1.5
- Hero title: 3rem (2rem on mobile), weight 900, letter-spacing 2px
- Section headers: 1.125rem, weight 600
- Body: 0.875rem
- Labels: 0.75rem, uppercase, letter-spacing 1px

## Spacing

- Container max-width: 960px (720px for player page)
- Container padding: 16px horizontal
- Card padding: 12-16px
- Grid gap: 12px (stats), 4px (matches list), 8px (region tabs)
- Section margin: 24px bottom

## Border Radius

| Variable | Value | Usage |
|----------|-------|-------|
| `--radius-sm` | `4px` | Match cards, rows |
| `--radius` | `8px` | Stat cards, avatars |
| `--radius-lg` | `12px` | Player header, search |

## Components

### Stat Card
4-column grid (2 on mobile). Centered value (accent color, 1.5rem) + label (muted, uppercase).

### Match Card
6-column grid row. Left border indicates win (green) / loss (red). Shows: result, map, agent, score, KDA, K/D diff.

### Agent Row
Grid row: name, games, win rate, K/D.

### Leaderboard Row
Grid row: position, player name (linked), rank rating, wins.

### Search Form
Centered, max 480px. Dark input + red submit button. Focus: red border.

## Responsive Breakpoints

- Mobile: < 640px
  - Stats grid: 2 columns
  - Match cards: hide agent, K/D diff columns
  - Agent rows: hide extra columns
  - Leaderboard: hide wins column
  - Player header: stack vertically, center
