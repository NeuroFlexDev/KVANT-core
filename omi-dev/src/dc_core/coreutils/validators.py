# -*- coding: utf-8 -*-
from string import ascii_letters, ascii_uppercase, digits, whitespace

allowed_symbols = r"""~!?@#$%^&*_-+()[]{}></\|"'.,:;"""
all_allowed_symbols = allowed_symbols + digits + ascii_letters


def validate_password(password: str) -> bool:
    # TODO: Нужны ли русские буквы?
    try:
        # Длина. 8-20 символов
        assert 8 <= len(password) <= 20
        # uppercase хотя бы одна
        assert any(uc in password for uc in ascii_uppercase)
        # digit хотя бы один
        assert any(d in password for d in digits)
        # no spaces
        assert not any(ws in password for ws in whitespace)
        # allowed symbols
        assert all(i in all_allowed_symbols for i in password)

    except AssertionError:
        return False

    return True
