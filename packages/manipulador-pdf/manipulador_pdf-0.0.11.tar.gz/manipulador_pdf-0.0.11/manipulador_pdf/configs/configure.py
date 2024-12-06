import json
import os


def configure() -> None:

    if not os.path.exists('configs'):
        os.mkdir('configs')

    if 'token.json' not in os.listdir('configs'):

        data = {"token": "ya29.a0AeDClZB1jsPm-waNkqp10xXt0KuOU_9_4W_AH4dstyURl6uwZUOZ6WOi4eAaBUSyCwgr0oSad9G9MGkU-n3oifIQHdJN4w0X8JgfZui1LdfT5zoxlL2JXsUQgDIjKhBWpmRSKPrXgfeuOEclxG5aTKzdT5P-g9oIPVRbl4POc8UaCgYKAesSARISFQHGX2MiqQIuewIrprBcLibBHaubTA0178",
                "refresh_token": "1//0hucRPjR9Y5xQCgYIARAAGBESNwF-L9IrgFPQ1DybBVly-FCfFaGWY08uVqJ4Z47DCf2fJ4XqgDmx_RfCo2m5dXFuGWWQxG5HLfk",
                "token_uri": "https://oauth2.googleapis.com/token",
                "client_id": "694930976727-1nfelmerhl3nrehsagk2g7fu9783e5u7.apps.googleusercontent.com",
                "client_secret": "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",
                "scopes": ["https://www.googleapis.com/auth/spreadsheets"],
                "universe_domain": "googleapis.com",
                "account": "",
                "expiry": "2024-11-13T16:20:15.785200Z"}

        # Escrever os dados no arquivo JSON
        with open('configs/token.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

