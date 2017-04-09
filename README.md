# DotaLawliet
## Simple Guide
* Use the "locate server_log.txt" buton to find the server_log.txt file located under the game directory. Ususally in Windows, the file is located in C:/Program Files (x86)/Steam/steamapps/common/dota 2 beta/game/dota/server_log.txt.
* The tool will create a local.txt file in local directory so it will memorize the server_log.txt location so next time you open this tool, it will automatically load this settting.
* Click the "refresh match" button to refresh the game state. If the tool successfully refresh the game state, the "refresh match" button will have 20 seconds cooldown to comply with Opendota API requirement.
* In the "Radiant" and "Dire" sections, it will pull following player information from Opendota API: estimated mmr, solo mmr, team mmr and the most recent 50 matches.

## Known Bug
* If there is a coach in either side of the team, the behavior is unknown.
