---
name: scrapegraph-ai-scraping
description: "AI web scraping: extract data by prompt, no selectors."
version: 1.0.0
author: Hermes Agent (JARVIS)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [scraping, web-scraping, data-mining, ai, llm, automation]
    related_skills: [exploratory-data-analysis, scikit-learn, polars]
---

# ScrapegraphAI — LLM-Powered Web Scraping (No Manual Selectors)

ScrapegraphAI is a Python library that uses an LLM to understand a page's
structure and extract exactly the data requested via a natural-language
prompt — no CSS selectors, no XPath, no brittle parsing code that breaks
when a site redesigns. Good for data-mining/collection tasks where the
target page structure varies or isn't worth reverse-engineering manually.

## When to use this skill

- User wants to scrape/extract structured data from a webpage (or list of
  webpages) and describes WHAT to extract in plain language, not HOW
  (no selectors given)
- Target site's HTML structure is messy, inconsistent across pages, or
  the user wants something that survives site redesigns better than a
  hardcoded selector script
- Building a recurring data-collection pipeline (e.g. price monitoring,
  news aggregation, competitor tracking) where writing/maintaining
  selectors for many different sites isn't worth it
- For simple, well-known, stable page structures (e.g. Yahoo Finance JSON
  endpoints), prefer direct `requests`/`curl` calls — cheaper and faster
  than invoking an LLM per page. Reach for ScrapegraphAI when the
  page is HTML-only (no API) and unpredictable in structure.

## Installation

```bash
pip install scrapegraphai
# Playwright browser binaries (needed for JS-rendered / headless mode):
playwright install
```

## Core Config Pattern (using Hermes's own model — no separate API key needed)

ScrapegraphAI needs an `llm` config block. Point it at the SAME custom
OpenAI-compatible endpoint Hermes itself uses — no need for a separate
OpenAI/Anthropic key:

```python
import os
from scrapegraphai.graphs import SmartScraperGraph

graph_config = {
    "llm": {
        "api_key": os.environ["HERMES_CUSTOM_192_168_147_179_20128_API_KEY"],  # or read from wherever the deployment stores it
        "model": "openai/cc/claude-sonnet-5",   # prefix with "openai/" — scrapegraphai routes by that prefix regardless of actual backend
        "base_url": "http://192.168.147.179:20128/v1",
    },
    "verbose": True,
    "headless": True,   # set False to watch the browser while debugging
}

smart_scraper_graph = SmartScraperGraph(
    prompt="Extract the product name, price, and rating",
    source="https://example.com/product-page",
    config=graph_config,
)

result = smart_scraper_graph.run()
print(result)   # dict, e.g. {"content": {"product_name": ..., "price": ..., "rating": ...}}
```

**Env var name varies per deployment** — check `/opt/data/.env` (or the
active deployment's env) for the exact `HERMES_CUSTOM_<host>_<port>_API_KEY`
variable name matching the base_url in use; don't assume the exact string
above is correct for every environment.

## Common Graph Types

| Graph class | Use for |
|---|---|
| `SmartScraperGraph` | Single page, one prompt → structured extraction |
| `SmartScraperMultiGraph` | Same prompt across multiple URLs, one call |
| `SearchGraph` | Search the web (via a search API) then scrape+extract from top results |
| `SpeechGraph` | Scrape + convert result to speech (niche) |
| `ScriptCreatorGraph` | Generate a reusable Python scraping script instead of scraping directly (useful when you'll re-run the same extraction repeatedly and want to avoid repeated LLM calls) |

### Multi-URL example

```python
from scrapegraphai.graphs import SmartScraperMultiGraph

multi_graph = SmartScraperMultiGraph(
    prompt="Extract product name and price",
    source=[
        "https://example.com/product1",
        "https://example.com/product2",
    ],
    config=graph_config,
)
result = multi_graph.run()
```

## Output Shape

Result is typically `{"content": {...}}` where the inner dict matches
whatever fields the prompt implied — ScrapegraphAI infers the schema from
the prompt text. For a strict/guaranteed schema, pass a Pydantic model via
the `schema` config key instead of relying on prompt wording alone:

```python
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    in_stock: bool

graph_config["schema"] = Product
```

## Cost/Performance Notes

- Every scrape = at least one LLM call per page (input tokens scale with
  page HTML size) — for large-scale crawling (100s+ pages), this gets
  expensive/slow compared to selector-based scraping. Prefer
  `ScriptCreatorGraph` to generate a reusable non-LLM script if the same
  extraction will run repeatedly (e.g. in a cron job).
- `"Max input tokens for model ... not found"` warning is expected for
  custom/non-standard model names — it falls back to a conservative 8192
  token default. If pages are large, either set `model_tokens` explicitly
  in the llm config, or pre-trim HTML before passing (e.g. via `requests`
  + BeautifulSoup to strip nav/footer/script tags first).

## Pitfalls

- **JS-heavy sites**: `headless: True` uses Playwright under the hood —
  make sure `playwright install` has been run once, or fetch will fail
  silently/timeout.
- **Rate limits / ToS**: this is still scraping — same legal/ethical
  considerations apply as any scraping approach (robots.txt, ToS,
  rate limiting, no PII harvesting without basis). ScrapegraphAI does
  not bypass site-level scraping restrictions.
- **Model name prefix**: ScrapegraphAI's LiteLLM-based routing expects an
  `openai/`-style prefix on custom/local models even when the backend
  isn't literally OpenAI — omitting it causes provider-detection errors.
- **IP-literal base_url flags security scanners**: if the LLM endpoint is
  an internal IP (e.g. `192.168.x.x`), some environment security scanners
  may flag the outbound call — this is expected/benign for an internal
  Hermes-hosted model endpoint, not a real external exposure.

## Related Skills

- `exploratory-data-analysis` — profile/clean the scraped data once collected
- `scikit-learn` — clustering/pattern-mining on the collected dataset
- `polars` — fast ETL if scraping produces large tabular output
