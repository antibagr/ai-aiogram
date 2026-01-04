\## Working agreements



\- Prefer small, reviewable diffs over large rewrites.

\- Before changing behavior, explain: (1) what’s wrong, (2) what you’ll change, (3) how you’ll test.

\- Never print or log secrets. If you suspect secrets exist in env/files, ask before proceeding.



\## Python conventions



\- Follow the Python Google Style Guide.

\- Use explicit module imports: `import pkg.mod` (avoid `from pkg import thing`) unless unavoidable.

\- Use type hints for public functions and important internals.

\- Write docstrings for public APIs and non-obvious logic.

\- Add/adjust tests for bug fixes and for tricky logic.



\## Tooling



\- If tests exist, run the fastest relevant subset first, then full suite if reasonable.

\- If unsure what to run, ask: “What’s the canonical lint/test command here?”



