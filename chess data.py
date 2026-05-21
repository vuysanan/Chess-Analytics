from chessdotcom import get_player_stats, get_player_games_by_month, Client
from datetime import datetime
import pprint
import csv

printer = pprint.PrettyPrinter(indent=4)

Client.request_config["headers"]["User-Agent"] = (
    "Chess Analytics App. Contact me at vuyisanani.inbox@gmail.com"
)

def get_summary_data(username):
    stats = get_player_stats(username).json
    #printer.pprint(stats)

    categories = ['chess_blitz', 'chess_rapid']
    
    with open('chess_data.csv', mode='w', newline='') as csvfile:
        fieldnames = ["Current Rating", "Best Rating", "Wins", "Losses", "Draws"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for category in categories:
            if category in stats['stats']:
                rating = stats['stats'][category]['last']['rating']
                best_rating = stats['stats'][category]['best']['rating']
                wins = stats['stats'][category]['record']['win']
                losses = stats['stats'][category]['record']['loss']
                draws = stats['stats'][category]['record']['draw']
                
                writer.writerow({
                    "Current Rating": rating,
                    "Best Rating": best_rating,
                    "Wins": wins,
                    "Losses": losses,
                    "Draws": draws
                })

#get_summary_data('crookedrook3000')

# get game date vs opponent rating

def get_monthly_opponent_ratings(username, year, month):
    response = get_player_games_by_month(username, year, month).json
    games = response.get('games', [])
    
    filename = f"opponents_{year}_{month:02d}.csv"
    
    with open(filename, mode='w', newline='') as csvfile:
        fieldnames = ['Date', 'Time_Format', 'Opponent_Rating']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for game in games:
            timestamp = game.get('end_time')
            if not timestamp:
                continue
                
            date_obj = datetime.fromtimestamp(timestamp)
            date_str = date_obj.strftime('%Y-%m-%d')
            
            time_format = game.get('time_class', 'unknown').capitalize()
            
            if game['white']['username'].lower() == username.lower():
                opponent_rating = game['black']['rating']
            else:
                opponent_rating = game['white']['rating']
                
            writer.writerow({
                'Date': date_str,
                'Time_Format': time_format,
                'Opponent_Rating': opponent_rating
            })

get_monthly_opponent_ratings('crookedrook3000', 2026, 5)