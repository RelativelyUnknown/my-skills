# AI writing patterns in documentation

Language models drift toward the statistical middle: safe, inflated, generic phrasing that reads as filler. This file lists the patterns that matter most in technical documentation. It condenses Wikipedia's "Signs of AI writing" editor guide, as packaged in softaworks' *writing-clearly-and-concisely*, and adapts it to docs. `scripts/lint_prose.py` catches the word-level ones; the structural ones need a read.

## Contents

- Word level
- Sentence level
- Structure and formatting
- Content
- Rewrites

## Word level

<!-- lint-prose: off -->
- **Puffery**: powerful, robust, seamless, cutting-edge, comprehensive, pivotal, crucial, game-changing, blazing fast.
- **AI vocabulary**: delve, leverage, utilize, foster, realm, tapestry, multifaceted, embark, elevate, unlock, empower, streamline, harness, holistic, landscape, ever-evolving.
- **Hedging stacks**: "may potentially", "can help to", "generally tends to".
- **Empty -ing tails**: "..., ensuring reliability", "..., highlighting its flexibility", "..., making it ideal for".
<!-- lint-prose: on -->

## Sentence level

- **Negative parallelism**: "It's not just a parser, it's a platform." State what it is.
- **Rule of three**: lists padded to three items or three adjectives ("fast, flexible, and reliable") regardless of content.
- **False range**: "from small scripts to enterprise pipelines" when nothing in the docs is about either end.
- **Elegant variation**: calling one thing "the client", "the connector" and "the tool" in one page. Docs need one term.
- **Signposting**: "Let's dive in", "In this section, we will explore", "Now that we've covered X, let's look at Y".
- **Summary echo**: "In summary", "Overall", "In conclusion" followed by a restatement of the page.
- **Vague attribution**: "is widely regarded as", "many developers find". Name the source or cut it.

## Structure and formatting

- Bold sprinkled on phrases in every paragraph.
- Bulleted lists where each item is a bold label, a colon and a sentence ("**Speed:** It is fast."). Use a table or prose.
- Headings in Title Case, often with emoji.
- Em dashes as the default punctuation.
- Sections that exist because a template has them: "Key features", "Benefits", "Conclusion", "Future enhancements".
- Every section the same length, regardless of how much there is to say.

## Content

- **Invented facts**: options, flags, defaults, version numbers or API names that do not exist. Check each against the code or `--help` output.
- **Fake specifics**: benchmark numbers or "99.9%" claims without a source.
- **Generic advice** that applies to any software ("follow best practices", "ensure proper error handling").
- **Conversation residue**: "As requested", "Here is the updated documentation", "I hope this helps", "Let me know if".
- **Unrequested sections**: troubleshooting, FAQ or roadmap pages invented to look complete.
- **Knowledge-cutoff hedges**: "as of my last update". Documentation states facts verified now, or links to the source.

## Rewrites

| Generated | Rewritten |
| --- | --- |
| "This powerful library seamlessly integrates with your existing workflow, empowering developers to unlock new possibilities." | "The library reads and writes Parquet files that pandas, Polars and DuckDB can open." |
| "It's important to note that the cache may potentially become stale." | "The cache is not invalidated when the source file changes. Call `cache.clear()` after editing it." |
| "In this section, we'll delve into configuration options." | (delete; the heading says it) |
| "**Fast:** Optimized for performance." | "Loads a 1 GB file in 2 s on an M2 laptop ([benchmark](https://example.com/benchmarks))." or delete |
| "Whether you're a beginner or an expert, this guide has you covered." | (delete) |
