from django.contrib.auth.tokens import PasswordResetTokenGenerator
# import six

class MyTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return str(user.pk) + str(timestamp)

account_activation_token = MyTokenGenerator()