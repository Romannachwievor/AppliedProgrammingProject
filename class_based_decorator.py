from time import perf_counter
from typing import Any, Callable


class LogAndMeasure:
	"""Class-based decorator that logs calls and measures runtime."""

	def __init__(self, label: str) -> None:
		self.label = label

	def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
		def wrapper(*args: Any, **kwargs: Any) -> Any:
			start = perf_counter()
			print(f"[{self.label}] calling {func.__name__}")
			result = func(*args, **kwargs)
			elapsed_ms = (perf_counter() - start) * 1000
			print(f"[{self.label}] {func.__name__} finished in {elapsed_ms:.2f} ms")
			return result

		return wrapper


@LogAndMeasure("decorator-demo")
def create_note_summary(title: str, category: str) -> str:
	return f"{title} ({category})"


@LogAndMeasure("decorator-demo")
def add_numbers(a: int, b: int) -> int:
	return a + b


if __name__ == "__main__":
	print(create_note_summary("Sprint Planning", "work"))
	print(add_numbers(7, 5))
