# Source of this copy

- Upstream: https://github.com/wshobson/agents
- Path: `plugins/python-development/skills/` (16 skills)
- Commit: `4bde3168b43c0655c4d00ea2726e631719908a6d` (5 November 2026, as shown on the GitHub commits page)
- Licence: MIT, Copyright (c) 2024 Seth Hobson (the plugin manifest also declares MIT). The upstream `LICENSE` is kept next to this file; it applies to these copies, not to the rest of this repository.
- Vendored: 6 November 2026, **unmodified**. Files were downloaded as raw bytes from `raw.githubusercontent.com` at that commit.
- Not included: the plugin's `agents/` and `commands/` folders and its manifests.

## Review before vendoring

The bytes were scanned for invalid UTF-8, invisible and bidirectional characters, HTML comments and tags, long encoded blobs, phrases aimed at an AI agent (ignore previous instructions, run, upload and similar) and install or shell commands, and the frontmatter was checked for permission fields. Nothing was found that tells an agent to do anything outside the task.

- No `scripts/` folders, binaries or executable files in any skill.
- Frontmatter uses only `name` and `description`; no `allowed-tools`, hooks or other permission fields.
- Several skills show install commands (`pip install`, `brew install uv`, `cargo install --locked uv`, `winget install`) and `rm -rf test-env` as documentation examples.

## Files (sha256)

| sha256 | path |
| --- | --- |
| `f89abb55d9f073f38f1703e4518f0613c788c6174be7f13b8dfe48a1c076c746` | `LICENSE` |
| `c2da0b41953cda62a960d37126c0a5cb387b8f8b0093e3f71cc1c78455cb815a` | `skills/async-python-patterns/SKILL.md` |
| `c5a97988fb96562bdcf436ba4e022e8e67df46e69f373fe3a93315bcd2a8474c` | `skills/async-python-patterns/references/details.md` |
| `5d8074ae2408afca827b384e26d151630901a6e6f876dad6acad299e497e8be3` | `skills/python-anti-patterns/SKILL.md` |
| `ea99e3f1d4df0e0c7260e3d6436003ea980c55d8b1ad6950ba63048491eb531e` | `skills/python-background-jobs/SKILL.md` |
| `96268f59787cba8297e5d0a811fcc3c1fe70ec2ea1a4f1fcb939f67c6ca45ba2` | `skills/python-background-jobs/references/details.md` |
| `82699eefa7996bf06bbf85219f547eae0140a181ee3699444e2cbd665b7caba7` | `skills/python-code-style/SKILL.md` |
| `a9095f4388f7c61c4d5eb0fd2d2a6192e872b6da7a59baac66a10422e333d65f` | `skills/python-configuration/SKILL.md` |
| `10f2cb813e20ab446a9578c0200955875c63ff98918b6a84e44f1fc6a0eef209` | `skills/python-configuration/references/details.md` |
| `42c99b3bc55a56a65cd3f16aa24ea50672ce0fa4893eb0f34bba0cdb8a0e3319` | `skills/python-design-patterns/SKILL.md` |
| `5d85b7a1745446432060bb31ee1fa686d5a41d86cfaf3687dd2710b47b72e5ea` | `skills/python-design-patterns/references/details.md` |
| `796346a50615010c4fea52ecb93784ebf232c5d4c9f0691bfc668529d9592543` | `skills/python-error-handling/SKILL.md` |
| `022c6c6bfb362d861258763712a05f62ccac09120866355582f874db14735c82` | `skills/python-error-handling/references/details.md` |
| `bf547d6ee0284ce20bbe521af3e40d53ca9481634dfeaaf16f25c88de6828f56` | `skills/python-observability/SKILL.md` |
| `71e2fc7263c1ec20227b9f074cebf66f60e4e5cddd2f341ac18d3291aee4b649` | `skills/python-observability/references/details.md` |
| `744653d7bca3b0cfcb50155a3bb9ef56c7aba7eb4923091d07e75171261e5b49` | `skills/python-packaging/SKILL.md` |
| `598e75519ce9cfd44e3a47ee9ed829cd23509ba16b99d09a4737cc807c47ce64` | `skills/python-packaging/references/advanced-patterns.md` |
| `4bf009076d1e89cd2bf9bfffeea645095f10cd88f8fcc8b03c137303ebef27dc` | `skills/python-packaging/references/details.md` |
| `807aa725cc2b46b4d68a11a52e5b345be0449e80b7f4b60c32bfd2c35345afb5` | `skills/python-performance-optimization/SKILL.md` |
| `3109ef651c7591017505aeed1d171fbf9000ee522c1b4dac35f90192974b20f0` | `skills/python-performance-optimization/references/advanced-patterns.md` |
| `8643031fabcbaf555ae1b4e702f1b5159689a31a4b286280d4df2822c9731281` | `skills/python-performance-optimization/references/details.md` |
| `c53696fb8d9014abc280fc0e64220cae0d087766a16380e211a6745e481dae65` | `skills/python-project-structure/SKILL.md` |
| `ddf3a7dc5bd59dd228a65a3ee7ae60fe740e9dc6e98bfac0ce0be5330fcc5332` | `skills/python-resilience/SKILL.md` |
| `bacdee07c89f21324069904107b99224afd9b65415f56da8974b20aa03e4aff4` | `skills/python-resilience/references/details.md` |
| `7d79953ee92ef07795ed0929f110c0683e5f416cdf0f33d7cdf8b0a606759c25` | `skills/python-resource-management/SKILL.md` |
| `b9cf1a36f6172812c3509e8a88e2d19de76d9e1fe2c4598df10558b372e88022` | `skills/python-resource-management/references/details.md` |
| `a1020718f31629c2a5b20731cad1804dbb81b18800495c5cebdf16e6cac9c175` | `skills/python-testing-patterns/SKILL.md` |
| `f560ee8b3cffc0fe971e78269bed21dc74f541c2056eae58d34259d9e537176a` | `skills/python-testing-patterns/references/advanced-patterns.md` |
| `39411069cafe265c7000e9a605aa3c17448981756799f3981137ed2d9cc24c20` | `skills/python-testing-patterns/references/details.md` |
| `7798dd109350b73c80bb4642f6e5a0ebaa2ae392484a213d4b44b35e9b4dad66` | `skills/python-type-safety/SKILL.md` |
| `c31ae289ec8de07220ddac57434fb0b764216af8a435dcc078c446d82e6862b5` | `skills/python-type-safety/references/details.md` |
| `14df843d2d7958257e47933961914ff6598adb8422e4759000586c43ce80ab2c` | `skills/uv-package-manager/SKILL.md` |
| `5750de438fa2456c37640f6efcb87c423fe2919510da4e67e564b2af7972c0bc` | `skills/uv-package-manager/references/advanced-patterns.md` |

## Updating

Download the files again at a newer commit, repeat the review, replace the files, and update the commit, date and hashes here.
