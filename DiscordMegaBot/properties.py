import discord as api
prefix = ':'
token = '<your token>'
dagpi_token = '<your dagpi token>'
intents = api.Intents.default()
intents.members = True
intents.presences = True
insensitiveCase = True
ownerID = "<your id> (without quotes)"