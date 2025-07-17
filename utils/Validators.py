# utils/Validators.py
import re

class Validators:
    CASE_ID_PATTERN = re.compile(r'^(?:\d{2}|\d{4})-\d{1,8}(?:-[A-Za-z0-9_]+)?$')

    @staticmethod
    def is_valid_case_id(case_id):
        return bool(Validators.CASE_ID_PATTERN.match(case_id))
