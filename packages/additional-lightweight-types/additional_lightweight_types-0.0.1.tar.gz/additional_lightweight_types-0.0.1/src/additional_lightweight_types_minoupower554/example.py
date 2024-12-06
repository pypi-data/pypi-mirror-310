class String(str):
    def is_none_or_whitespace(self):
        return not self or self.isspace()

    @classmethod
    def cast_to_string(cls, inp):
        return cls(inp)
