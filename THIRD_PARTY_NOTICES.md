# Third-party notices

Skills in this repository were adapted from the work of other authors. The adapted wshobson material keeps the upstream licence as `python-engineering/LICENSE.wshobson` and a `python-engineering/SOURCE.md` (upstream URL, pinned commit, what changed); other adapted material keeps its licence and `SOURCE.md` next to it. Everything below is MIT-licensed; the MIT licence requires its copyright and permission notice to travel with every copy or substantial portion, which is why the licence text sits next to each adapted skill.

The rest of this repository is MIT (see `LICENSE`).

## wshobson/agents (python-development plugin)

- Upstream: https://github.com/wshobson/agents
- Author and licence: Seth Hobson, MIT
- Commit: 4bde3168b43c0655c4d00ea2726e631719908a6d (5 November 2026)

| Upstream skill | Adapted into |
| --- | --- |
| `python-resource-management` | `python-engineering/references/fields/software-engineering/all/code/resources.md`, `resource-patterns.md` |
| `python-type-safety` | `python-engineering/references/fields/software-engineering/all/code/typing.md`, `typing-patterns.md` |
| `uv-package-manager` | `python-engineering/references/fields/software-engineering/all/dependencies/uv.md`, `uv-ci.md`, `uv-docker.md` |
| `async-python-patterns` | `python-engineering/references/fields/software-engineering/application/shared/async.md`, `async-patterns.md` |
| `python-background-jobs` | `python-engineering/references/fields/software-engineering/application/workers/background-jobs.md`, `background-jobs-patterns.md` |
| `python-observability` | `python-engineering/references/fields/software-engineering/application/shared/observability.md`, `observability-patterns.md` |
| `python-configuration` | `python-engineering/references/fields/software-engineering/application/shared/configuration.md`, `configuration-patterns.md` |
| `python-resilience` | `python-engineering/references/fields/software-engineering/application/shared/resilience.md`, `resilience-patterns.md` |
| `python-error-handling` | `python-engineering/references/fields/software-engineering/all/code/errors.md`, `validation.md` |
| `python-design-patterns` | `python-engineering/references/fields/software-architecture/design-principles.md` |
| `python-testing-patterns` | one section of `python-engineering/references/fields/software-engineering/all/testing/mocking.md`; the rest was already covered (see `python-engineering/SOURCE.md`) |
| `python-performance-optimization` | `python-engineering/references/fields/software-engineering/all/performance/hot-path-fixes.md`; the profiler tutorial was not copied (see `python-engineering/SOURCE.md`) |
| `python-packaging`, `python-project-structure` | `python-engineering/references/fields/software-engineering/library/shared/versioning.md`, `entry-points.md`, `tooling.md`; the rest was already covered (see `python-engineering/SOURCE.md`) |
| `python-code-style` | pointer only; nothing copied (see `python-engineering/SOURCE.md`) |

## cloudflare/security-audit-skill

- Upstream: https://github.com/cloudflare/security-audit-skill
- Author and licence: Cloudflare, Inc., MIT
- Used as an approach only; no text copied. `reviewing-python-code/references/security-audit/` restates, in new words and for Python, the boundary-and-result requirement, the source-to-sink trace, the attempt to disprove each candidate, the confirmed / needs-validation / rejected buckets with severity only for confirmed findings, and the fix with a regression test.

## Ideas only (no text copied)

- DietrichGebert/ponytail (MIT) and JuliusBrussee/caveman (Apache-2.0): the rules in the `python-engineering` front door and `all/code/comments.md` that comments say only what is not obvious, replies stay short, and negations ("not", "never", "only", "except") are never dropped. Names, installers, proxies and telemetry are not used.

## Read, nothing taken

blader/humanizer (MIT), softaworks/agent-toolkit `writing-clearly-and-concisely` (MIT), addyosmani/agent-skills (MIT), morganlinton/BeautifulRust (MIT), cathrynlavery/diagram-design (MIT), caru-ini/stack-diagram (MIT), pbakaus/impeccable (Apache-2.0), heydamir/unslop (CC BY 4.0), vercel-labs/agent-skills (no LICENSE file), mukul975/Anthropic-Cybersecurity-Skills (Apache-2.0), ComposioHQ/awesome-claude-skills, github/awesome-copilot (MIT). They were read for ideas; where a baseline case showed the model already does the thing, nothing was added. Earlier unmodified copies of humanizer, writing-clearly-and-concisely and the wshobson Python skills were removed from the repository; the adapted wshobson material is in `python-engineering` with its pinned commit.
