from .user import User

class Message:
    def __init__(self, socket, data):
        self.__socket = socket
        self.raw = data
        self.__author = self.raw.get('author', None)
        if self.__author is not None:
            self.author = User(self.__author)
        self.id = self.raw['id']
        self.channel_id = self.raw['channel_id']
        self.components = self.raw['components']
        self.embeds = self.raw['embeds']
        self.content = self.raw['content']

    async def disable_component(self, ucid):
        for action_row in self.components:
            for component in action_row['components']:
                if component['custom_id'] == ucid:
                    component['disabled'] = True

        self.raw['components'] = self.components
        await self.__socket.make_request('PATCH', f"channels/{self.channel_id}/messages/{self.id}", json=self.raw)
        await self.__rebuild()

    async def disable_all_components(self):
        for action_row in self.components:
            for component in action_row['components']:
                component['disabled'] = True

        self.raw['components'] = self.components
        await self.__socket.make_request('PATCH', f"channels/{self.channel_id}/messages/{self.id}", json=self.raw)
        await self.__rebuild()

    async def edit(self, content: str = '', embeds: list = [], components: list = [], mentions: list = []):
        self.raw['content'] = content if content != '' else self.raw['content']
        self.raw['embeds'] = embeds if len(embeds) != 0 else self.raw['embeds']
        self.raw['components'] = components if len(components) != 0 else self.components
        self.raw['mentions'] = mentions if len(mentions) != 0 else self.raw['mentions']
        
        await self.__socket.make_request('PATCH', f"channels/{self.channel_id}/messages/{self.id}", json=self.raw)
        await self.__rebuild()

    async def delete(self):
        await self.__socket.make_request('DELETE', f"channels/{self.channel_id}/messages/{self.id}")

    async def fetch_reaction(self, reaction: str):
        reactions = await self.__socket.make_request('GET', f"channels/{self.channel_id}/messages/{self.id}/reactions/{reaction}")
        return reactions

    async def add_reaction(self, reaction: str):
        await self.__socket.make_request("PUT", f"channels/{self.channel_id}/messages/{self.id}/reactions/{reaction}/@me")

        

    async def __rebuild(self):
        message = await self.__socket.make_request('GET', f"channels/{self.channel_id}/messages/{self.id}")
        self.raw = message
        self.__author = self.raw.get('author', None)
        if self.__author is not None:
            self.author = User(self.__author)
        self.components = self.raw['components']
        self.embeds = self.raw['embeds']
        self.content = self.raw['content']
