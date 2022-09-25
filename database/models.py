from tortoise.models import Model
from tortoise import fields


class Subscription(Model):
    id = fields.IntField(pk=True)
    user_setter_id = fields.BigIntField()
    server_id = fields.BigIntField()
    channel_id = fields.BigIntField()
    image_url = fields.CharField(max_length=255)

    class Meta:
        unique_together = ("server_id", "channel_id")

    def __str__(self):
        return str(self.__dict__)
