# Validation at the edge

Turn raw input into a domain type where it enters, and raise one error that says what was expected and what arrived. Inner code then takes the typed value and does not re-check it. Convert library errors once, at the layer boundary, not at every call site.

```python
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

@dataclass(frozen=True)
class Money:
    amount: Decimal
    currency: str

    @classmethod
    def parse(cls, raw: str) -> "Money":
        try:
            number, currency = raw.split()
            return cls(Decimal(number), currency)
        except (ValueError, InvalidOperation) as error:  # only the lines that can fail are inside
            raise ValueError(f"expected '<amount> <CURRENCY>' like '12.50 EUR', got {raw!r}") from error

assert Money.parse("12.50 EUR") == Money(Decimal("12.50"), "EUR")
try:
    Money.parse("twelve")
except ValueError as error:
    assert "got 'twelve'" in str(error)
```
