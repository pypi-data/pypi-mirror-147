import novauniverse as nova

"""
player = nova.Player("THEGOLDENPRO")

print(player.is_online)
"""

"""
license = nova.License(key=nova.KEYS.TOURNAMENT_DEMO_KEY)

print(license.owner)
"""

mcf_results = nova.Mcf()
for mcf in mcf_results:
    wining_players = mcf.winner_team.players
    print(f"[MCF: {mcf.display_name}] Winner: {wining_players[0].name} and {wining_players[1].name}")