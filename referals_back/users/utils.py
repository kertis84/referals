from django.utils import crypto

class CodeGenerator(object):
    allowed_symbols="abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ0123456789!@#$%^&*()+-=/:;<>.,"
    allowed_chars="abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ0123456789"
    allowed_nums="0123456789"

    @classmethod
    def get_nums(self, length=4):
        return crypto.get_random_string(length, self.allowed_nums)
    
    @classmethod
    def get_chars(self, length=6):
        return crypto.get_random_string(length, self.allowed_chars)

    @classmethod
    def get_symbols(self, length):
        return crypto.get_random_string(length, self.allowed_chars)

