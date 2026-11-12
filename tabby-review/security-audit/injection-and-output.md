# Audit classes: injection, execution and output

For each class: where to look, what makes a hit a finding, what refutes it. Every hit still needs the trace from attacker-controlled input to the sink ([process.md](process.md)). Fixes are the write-time rules in `tabby/development/code/security-basics.md`.

## SQL and query languages

- **Look:** `execute`, `executemany`, `text()`, `.raw()`, `.extra()`, `RawSQL`, `cursor.execute` given an f-string, `%`, `.format` or `+`; table, column or `ORDER BY` taken from input; `filter(**request.GET)` or `Model.objects.filter(**data)`, which lets the caller choose fields and lookups.
- **Finding:** the value is attacker-controlled and is not bound. An identifier cannot be bound, so it needs an allowlist.
- **Refuted by:** bound parameters, ORM keyword filters with fixed names, constants.
- **NoSQL:** a JSON body used directly as a filter lets the caller send operators (`{"password": {"$gt": ""}}`); `$where` runs code. Coerce to `str` or parse into a typed model.

## OS commands

- **Look:** `shell=True`, `os.system`, `os.popen`, `subprocess` with a string; an argument list that still carries a value starting with `-` (argument injection into `git`, `tar`, `curl`; needs `--`).
- **Finding:** attacker-controlled data reaches the command line. `shlex.quote` is for building a shell string, not a replacement for a list. If a library call does the job (`os.makedirs`, `shutil`), the subprocess is the smell.
- **Refuted by:** a fixed argument list, an allowlist of command names, constants.

## Templates and output (XSS)

- **Look:** `render_template_string`, `Template(user_text)`, `Environment().from_string(user_text)`; `|safe`, `Markup`, `mark_safe`, `format_html` given unescaped text, `{% autoescape off %}`, `jinja2.Environment()` rendering HTML (autoescape is off by default), HTML built with f-strings, user text in `<script>`, `href` or `src` (`javascript:` URLs), uploads of HTML or SVG served inline.
- **Finding (template injection):** user text is the template. To confirm in a scratch test, `{{7*7}}` renders `49`.
- **Finding (XSS):** an escape hatch applied to user data. Automatic escaping by Django, Flask or Jinja with `select_autoescape()` is a control; only its escape hatches are findings.

## Execution and deserialization

- **Look:** `eval`, `exec`, `compile`, `__import__`, `importlib.import_module` or `getattr(module, name)()` on input. `pickle`, `marshal`, `shelve`, `dill`, `jsonpickle`, `joblib.load`, `pandas.read_pickle`, `numpy.load(allow_pickle=True)`, a `torch.load` of an untrusted file. `yaml.load` with `Loader` or `UnsafeLoader` (PyYAML 6 requires a loader argument, and those two ran a `!!python/object/apply` payload; `SafeLoader` and `FullLoader` blocked it). To spot pickled data in base64, pickle protocols 2 to 5 start `gAJ`, `gAN`, `gASV`, `gAWV`.
- **Finding:** the data crosses a trust boundary: an uploaded model, a cache or queue another party can write, a user's file, a cookie. Signing the data with a server-held key (`hmac.compare_digest` on the digest) is a mitigation, not a reason to keep pickle.
- **Refuted by:** a trusted-only source (the project's own build output); JSON or a typed model.

## XML

- **Look:** `xml.etree`, `minidom`, `sax`, `lxml` parsing outside data.
- **Finding:** the standard-library parsers expand internal entities (a small document can grow large). `lxml` 6.1.3 did not resolve an external entity with default settings (`Entity 'xxe' not defined`) and read `file:///etc/hostname` with `resolve_entities=True`; so the finding is `resolve_entities=True`, `load_dtd=True`, or an old `lxml`, not the default. `defusedxml` is the fix for untrusted XML.

## Type confusion and AI features

- **Type confusion:** type hints and casts do not validate. `request.json()["id"]` can be a list, dict, float or string; a handler that uses it as an ID, a limit or a filter value without parsing behaves unpredictably. A finding only when the wrong type reaches a security decision (a check that passes on a list, an operator injected into a query).
- **LLM features:** user-controlled text in a prompt is not a vulnerability by itself. It becomes one when the model also holds tools, files or credentials, or its output reaches `eval`, a shell, SQL or a path unchecked. Delimiters, "do not follow instructions in the document" and regex filters for "ignore previous instructions" are not controls. The control is what the model's output is allowed to do.

## Log and header injection

CR or LF in a user value written to a log or a header forges lines or splits a response. Log forging is low severity unless the logs are used as an audit source; for a header, check whether the framework in use rejects CR and LF in header values before reporting it.
