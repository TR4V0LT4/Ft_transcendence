import asyncio
import json
import uuid
from .game import gameManager
from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from nopassauth.models import UserProfile	
from databases import Database
import sqlalchemy
import asyncpg
import asyncio

games = {}
lobby = []
ids = []


# Define database URL
# DATABASE_URL = "postgresql://root:root@postgres:5432/admin"

# # Create SQLAlchemy engine
# engine = sqlalchemy.create_engine(DATABASE_URL, echo=True)

# # Create databases Database instance
# database = Database(DATABASE_URL)

# Async function to perform database query
# async def get_user_by_id(user_id):
# 	query = "SELECT * FROM nopassauth_userprofile WHERE user_id=:user_id"
# 	values = {"user_id": user_id}
# 	result = await database.fetch_one(query=query, values=values)
# 	print("++++++++++++++++", result)
# 	return result


class GameConsumer(AsyncWebsocketConsumer):
	def __init__(self):
		self.groups = []

	# Connects the consumer to the WebSocket.
	async def connect(self):
		self.channel_layer = get_channel_layer()
		await self.accept()
		lobby.append(self)

	async def get_user_by_id(user_id):
		try:
		# Query the User model to retrieve the user by ID
			user = await UserProfile.objects.get(user_id=user_id)
			return user
		except UserProfile.DoesNotExist:
		# Handle the case where the user does not exist
			return None
		except Exception as e:
		# Handle other exceptions, such as database connection errors
			print("An error occurred:", e)
		return None
	# This method iterates through the channel layer's groups and checks if the current channel name
	# is present in any of the channel names associated with a group. If a match is found, the group
	# name is returned. If no match is found, None is returned.
	async def getGroup(self):
		for group, channel_names in self.channel_layer.groups.items():
			if self.channel_name in channel_names:
				return group
		return None

	# generate a new group name create a new game and add the players to the game group,
	#  and start the game loop
	async def startGame(self):
		if len(lobby) >= 2 and len(ids) >= 2:
			player2 = {'player': lobby.pop(0), 'playerID': ids.pop(0)}
			player1 = {'player': lobby.pop(0), 'playerID': ids.pop(0)}
			group_name = str(uuid.uuid4())
			games[group_name] = {"game": gameManager(self, group_name), "players": [player1["playerID"], player2["playerID"]]}
			await self.channel_layer.group_add(group_name, player1["player"].channel_name)
			await self.channel_layer.group_add(group_name, player2["player"].channel_name)
			await player1["player"].sendPlayerNumber({'playerNb': 1}, player1["player"].channel_name)
			await player2["player"].sendPlayerNumber({'playerNb': 2}, player2["player"].channel_name)
			asyncio.create_task(games[group_name]["game"].gameLoop())

	# send the player numbers to the clients
	async def sendPlayerNumber(self, data, channel_name):
		await self.channel_layer.send(
			channel_name,
			{"type": "playerUpdate", "data": data}
		)
	# send player number to each client
	async def	playerUpdate(self, event):
		data = event["data"]
		await self.send(text_data=json.dumps(data))

	# move player up or down depending on the direction received from the client
	async def receive(self, text_data):
		try:
			data = json.loads(text_data)
		except json.JSONDecodeError:
			print("Invalid JSON data received:", text_data)
			return
		user_id = data.get('playerID')
		if 'playerID' in data:
			ids.append(user_id)
			await self.startGame()
			return
		group = await self.getGroup()
		if group in games:
			arenaHeight = games[group]["game"].game.arenaHeight
			is_player_one = self.channel_name == list(self.channel_layer.groups[group])[0]
			if is_player_one:
				if data["direction"] == "up" and games[group]["game"].game.player1.zPos - 1 >= -(arenaHeight / 2):
					games[group]["game"].game.player1.zPos -= 1
				elif data["direction"] == "down" and games[group]["game"].game.player1.zPos + 1 <= (arenaHeight / 2):
					games[group]["game"].game.player1.zPos += 1
			else:
				if data["direction"] == "up" and games[group]["game"].game.player2.zPos - 1 >= -(arenaHeight / 2):
					games[group]["game"].game.player2.zPos -= 1
				elif data["direction"] == "down" and games[group]["game"].game.player2.zPos + 1 <= (arenaHeight / 2):
					games[group]["game"].game.player2.zPos += 1

	# async def get_user_by_id_async(self, user_id):
	# 	query = "SELECT * FROM user_profile WHERE user_id = :user_id"
	# 	values = {"user_id": user_id}

	# 	async with Database(DATABASE_URL) as database:
	# 		try:
	# 			result = await database.fetch_one(query=query, values=values)
	# 			return result
	# 		except Exception as e:
	# 			# Handle exceptions
	# 			print(e)
	# 		return None
		
	# send the game update to all the clients
	async def	sendUpdate(self, data, gameID):
		await self.channel_layer.group_send(
			gameID,
			{"type": "gameUpdate", "data": data}
		)

	# send the game update to the client
	async def	gameUpdate(self, event):
		data = event["data"]
		await self.send(text_data=json.dumps(data))

	# send the scores to the clients
	async def gameOver(self, scores, gameID):
		try:
			user1 = await get_user_by_id(games[gameID]["players"][0])
			if user1 is not None:
				user1.stats.games_played += 1
				if scores["player1Score"] > scores["player2Score"]:
					user1.stats.wins += 1
					user1.stats.score += 25
				elif scores["player1Score"] < scores["player2Score"]:
					user1.stats.score -= 25
				user1.stats.winrate = user1.stats.get_winrate()
				user1.stats.highest_score = user1.stats.highest_score()
				await user1.stats.save()

			user2 = await get_user_by_id(games[gameID]["players"][1])
			if user2 is not None:
				user2.stats.games_played += 1
				if scores["player1Score"] < scores["player2Score"]:
					user2.stats.wins += 1
					user2.stats.score += 25
				elif scores["player1Score"] > scores["player2Score"]:
					user2.stats.score -= 25
				user2.stats.winrate = user2.stats.get_winrate()
				user2.stats.highest_score = user2.stats.get_highest_score()
				await user2.stats.save()

		except Exception as e:
			print("An error occurred:", e)

		await self.channel_layer.group_send(
			gameID,
			{"type": "sendScores", "data": scores}
		)

	async def sendScores(self, event):
		data = event["data"]
		await self.send(text_data=json.dumps(data))
		await self.close()


	# disconnect the client and send the game over message to the clients
	async def disconnect(self, code):
		group = await self.getGroup()
		await self.channel_layer.group_send(
			group,
			{"type": "forfeit", "data": {"won": "You won by forfeit"}}
		)
		return await super().disconnect(code)
	
	async def forfeit(self, event):
		data = event["data"]
		await self.send(text_data=json.dumps(data))
		await self.close()
