# pytrycatch


```py
from pytrycatch import handle_errors

@handle_errors(log=True, default_return="safe fallback")
def risky_operation():
    return 1 / 0

print(risky_operation())  # Output: "safe fallback"

```