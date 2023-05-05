from channels.generic.websocket import AsyncWebsocketConsumer
import json
from rest_framework.authtoken.models import Token

from group.models import Group
from asgiref.sync import sync_to_async


class ChatRoomView(AsyncWebsocketConsumer):
    group_id = None
    group_name = None

    @sync_to_async
    def auth_and_check_input(self, group_id: int, token: str):
        try:
            token_name, token_key = token.split()
            if token_name == 'Token':
                token = Token.objects.get(key=token_key)
                self.scope['user'] = token.user
            else:
                raise Exception("Invalid Token")
        except Token.DoesNotExist:
            raise Exception("Invalid Token")

        if not isinstance(group_id, int):
            raise Exception("id is not integer")

        group = Group.objects.filter(pk=self.group_id).filter().first()
        if group is None:
            raise Exception("group does not exist")

        if self.scope['user'] not in group.users.all():
            raise Exception("you dont have the permission to this group")

    async def connect(self):
        try:
            token = dict(self.scope['headers'])[b'authorization'].decode()
            self.group_id = int(self.scope["url_route"]["kwargs"]["group_id"])
        except Exception as e:
            pass

        self.group_name = "chat_%s" % self.group_id

        await self.auth_and_check_input(self.group_id, token)

        await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chatbox_message",
                "message": message,
                "user": {
                    "id": self.scope['user'].id,
                    "nickname": self.scope['user'].nickname,
                    "username": self.scope['user'].username
                }
            },
        )

    async def chatbox_message(self, event):
        message = event["message"]
        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "user": {
                        "id": event["user"]["id"],
                        "nickname": event["user"]["nickname"],
                        "username": event["user"]["username"],
                    }
                }
            )
        )
