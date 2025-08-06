# Contributing

Contributions should preserve the purpose of this repository: safe, runnable,
and transparent SOC exercises using only synthetic data.

## Before submitting a change

1. Confirm that the change contains no real personal, sensitive, credential, or
   production-system data.
2. Add or update a scenario fixture when changing detection behavior.
3. Update the linked playbook when changing a detection’s triage or response
   requirements.
4. Run the checks below.

~~~text
make validate
make test
~~~

## Documentation standard

Use clear, concise language. Do not use emoji characters in documentation or
code. State assumptions, safety boundaries, false-positive considerations, and
the expected outcome of each lab.
