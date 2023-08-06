from .strutils import _escape_characters


class _tpl_attribute:
  def __init__(self, token: str):
    if token is None:
      print("texplotlibx/attribute: NULL token not allowed!")
    self._token = token

  def get_value(self):
    if self._value is None:
      return self._value
    elif type(self._value) is str:
      return _escape_characters(self._value)
    elif type(self._value) is bool:
      return self._value
    else:
      return "%g" % self._value

  def __str__(self):
    return f"% {self._token}"

  def set_value(self, value):
    self._value = value


class _tpl_attribute_variable(_tpl_attribute):
  def __init__(self, token: str, value=None):
    super().__init__(token)
    self.set_value(value)

  def __str__(self):
    v = self.get_value()
    if v is None:
      return super().__str__()
    else:
      return self._token + "=" + v + ","


class _tpl_attribute_flag(_tpl_attribute):
  def __init__(self, token: str, enable: bool = False):
    super().__init__(token)
    self.value = enable

  def set_value(self, value: bool):
    super().set_value(value)

  def __str__(self):
    v = self.get_value()
    if v is None:
      print("texplotlibx/attribute: Unknown if statement should be set or not. Choosing to disable flag.")
    elif v:
      return f"{self._token},"
    else:
      return super().__str__()


class _tpl_attribute_function(_tpl_attribute):
  def __init__(self, token: str, value=None):
    super().__init__(token)
    self.set_value(value)

  def __str__(self):
    v = self.get_value()
    if v is None:
      return super().__str__()
    else:
      return f"\\{self._token}{{{str(v)}}};"
