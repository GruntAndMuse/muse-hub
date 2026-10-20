# AI Model Modes & Trigger Phrases

Reference for getting the most out of each free AI. Compiled 2026-10-10.
Modes are per-session toggles — set them BEFORE sending the prompt.

## DeepSeek (chat.deepseek.com)

| Mode | What it does | When to use |
|---|---|---|
| **DeepThink** | Reasoning mode — shows chain-of-thought, max accuracy | Hard problems: code review, math, logic. Always on for gauntlets. |
| **Search** | Real-time web search | Current events, prices, anything training data might miss |
| **Expert** (`deepseek-expert`) | Stronger, slower model | Hardest tasks. Default is Instant (`deepseek-chat`, fast). |

DeepThink and Search are orthogonal toggles, not models — combine freely.
100% free, no usage limits.

## Gemini (AI Studio)

| Mode | What it does | When to use |
|---|---|---|
| **Thinking: High** | Deep Think Mini — 5,000-20,000+ thinking tokens | Complex debugging, architecture, gauntlets. Always High for reviews. |
| **Thinking: Medium** | ~1,000-3,000 thinking tokens, 3-8s responses | Default for most engineering work |
| **Thinking: Low** | ~300 thinking tokens, fast | Summaries, simple Q&A, classification |
| **Deep Research** | Agentic researcher — browses, writes full reports | Deep investigations, not quick reviews |

Model: 3.1 Pro Preview. Thinking level applies per session in AI Studio.

## ChatGPT (free)

No reasoning controls, no model choice on free tier. You get what you get.
Limits: 2-file attach cap, daily upload quota. Plan around it, don't fight it.

## DuckAI (duck.ai)

Model selection only (e.g. GPT-6 Luna). No file uploads — images/PDFs only.
No reasoning controls. Treat output as principles checklist, not code findings.

## Prompt phrases worth knowing

These work as plain text in any model:
- "Think deeply for at least 20 rounds." — pushes deeper analysis
- "Cut the fluff." — shorter responses
- "Explain it like I'm 10." — simpler language
- "The keyword for this conversation is X." — anchors long conversations

## Gauntlet defaults

| Runner | Model | Mode |
|---|---|---|
| DeepSeek | deepseek-expert | DeepThink ON |
| Gemini | 3.1 Pro Preview | Thinking: High |
| ChatGPT | (free tier) | n/a |
| DuckAI | (selected) | n/a |

Set explicitly every run. Don't assume defaults.
