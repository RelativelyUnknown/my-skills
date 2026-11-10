# Entry points

Built with uv 0.11.32 on 7 November 2026.

A command is `[project.scripts]` with `name = "pkg.cli:main"`. `main()` returns `None` or an exit code; the generated script calls `sys.exit(main())`. After `uv sync`, `uv run name` works, and the wheel's `entry_points.txt` lists it under `[console_scripts]`. Check it in the built wheel, not in the source tree (`unzip -p dist/*.whl '*/entry_points.txt'`).
