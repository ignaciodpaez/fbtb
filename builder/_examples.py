
from builder._transmarket import *

save_competition_clubs('BRA1', 2000, 2004)
save_players(58, 2000, 2004)
save_players(6600, 2005, 2009)
save_user_squad('test01', [{'id': 192, 'club_id': 31, 'season_id': 2000}])
sql = "SELECT * FROM tm_players WHERE nationality LIKE '%Serbia%' ORDER BY position, id, age"
read_sql_query(pd.read_csv('data/tm_players.csv'), 'tm_players', sql)