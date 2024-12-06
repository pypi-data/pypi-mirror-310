from typing import Callable, Concatenate, Generic, ParamSpec, TypeAlias, TypeVar

ErrorCode: TypeAlias = int

_T = TypeVar("_T")
_E = TypeVar("_E")
_P = ParamSpec("_P")
_R = TypeVar("_R")


def private(fn: Callable[_P, _R]) -> Callable[Concatenate[bool, _P], _R]:
	def private_init(ignore_private: bool = False, *args: _P.args, **kwargs: _P.kwargs) -> _R:
		if not ignore_private:
			raise Exception("This constructor shall be called privately only.")
		result = fn(*args, **kwargs)
		return result

	return private_init


def do(private_fn: Callable[Concatenate[bool, _P], _R]) -> Callable[_P, _R]:
	"""
	Very Important Procedure, ignoring the @private decorator.

	```python
	@private
	def my_private_func(a: int) -> ...:
		...

	vip(my_private_func)(a=3)
	```
	"""

	def non_private_init(*args: _P.args, **kwargs: _P.kwargs) -> _R:
		result = private_fn(True, *args, **kwargs)
		return result

	return non_private_init


class Result:
	class Ok(Generic[_T]):
		# private
		def __init__(
			self,
			obj: _T,
			is_constructor_called_privately: bool = False,
		):
			if not is_constructor_called_privately:
				raise Exception("This constructor shall be called privately only.")
			self._obj = obj

		@property
		def obj(self) -> _T:
			return self._obj

		@property
		def is_ok(self) -> bool:
			return True

		@property
		def is_err(self) -> bool:
			return False

	class Err(Generic[_E]):
		# private
		def __init__(
			self,
			obj: _E,
			is_constructor_called_privately: bool = False,
		):
			if not is_constructor_called_privately:
				raise Exception("This constructor shall be called privately only.")
			self._obj = obj

		@property
		def obj(self) -> _E:
			return self._obj

		@property
		def is_ok(self) -> bool:
			return False

		@property
		def is_err(self) -> bool:
			return True

	@staticmethod
	def ok(obj: _T) -> "Result.Ok[_T]":
		return Result.Ok(obj=obj, is_constructor_called_privately=True)

	@staticmethod
	def err(obj: _E) -> "Result.Err[_E]":
		return Result.Err(obj=obj, is_constructor_called_privately=True)

	@staticmethod
	def is_ok(result: "Result.Ok[_T]|Result.Err[_E]") -> bool:
		return result.is_ok

	@staticmethod
	def is_err(result: "Result.Ok[_T]|Result.Err[_E]") -> bool:
		return result.is_err
