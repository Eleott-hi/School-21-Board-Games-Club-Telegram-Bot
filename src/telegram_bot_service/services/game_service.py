from typing import List, Dict
from database.database import games

def get_game_by_id(id: str) -> Dict:
    return list(filter(lambda x: x["id"] == id, games))[0]

def pritify_game_info(game: Dict):
    return (
        f'Title: {game["gameName"]}, {game["year"]}\n\n'
        f'Genre: {game["genre"]}\n'
        f'Players {game["minPlayers"]}-{game["maxPlayers"]}\n'
        f'Min age: {game["minAge"]}\n'
        f'Complexity: {game["gameComplexity"]}\n'
        f'Status: {game["status"]}\n'
        f'Description: {game["gameShortDescription"]}\n'
        )



def form_game_buttons(games):
    buttons = []
    callbacks = []

    for game in games:
        buttons.append(game["gameName"])
        callbacks.append("game_info_callback:" + game["id"])

    return buttons, callbacks