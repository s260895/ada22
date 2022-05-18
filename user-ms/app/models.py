from tortoise import fields, models


class User(models.Model):
    """
        User class
        The credentials used for authentication.
    """
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password = fields.CharField(max_length=128)

    class Meta:
        table = "users"
