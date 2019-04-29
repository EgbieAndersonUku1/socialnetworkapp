import bcrypt


class Password(object):

    @classmethod
    def hash_password(cls, plain_text_password):
        """"""
        hashed_password = bcrypt.hashpw(plain_text_password.encode('utf-8'), salt=bcrypt.gensalt())
        return cls._if_byte_convert_to_str(hashed_password)

    @classmethod
    def _if_byte_convert_to_str(cls, hashed_password):
        """"""
        if type(hashed_password) != str:
            hashed_password = hashed_password.decode("utf-8")
        return hashed_password

    @classmethod
    def check_password(cls, plain_text_password, hashed_password):
        return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode("utf-8"))