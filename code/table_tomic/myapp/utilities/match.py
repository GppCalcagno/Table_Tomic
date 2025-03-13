import math
import numpy as np

from ..models import Player, Match



def manage_match(form):
    try:
        team1_goalkeeper = Player.objects.get(name=form['team1_goalkeeper'].lower())
        team1_attacker = Player.objects.get(name=form['team1_attacker'].lower())
        team2_goalkeeper = Player.objects.get(name=form['team2_goalkeeper'].lower())
        team2_attacker = Player.objects.get(name=form['team2_attacker'].lower())

        # Check that all player IDs are different
        player_ids = [team1_goalkeeper.player_id, team1_attacker.player_id, team2_goalkeeper.player_id, team2_attacker.player_id]
        if len(player_ids) != len(set(player_ids)):
            raise ValueError("All player IDs must be different")
        
        match1 = [int(form['match1_points_team1']), int(form['match1_points_team2'])]
        match2 = [int(form['match2_points_team1']), int(form['match2_points_team2'])] if form['match2_points_team1'] and form['match2_points_team2'] else None
        match3 = [int(form['match3_points_team1']), int(form['match3_points_team2'])] if form['match3_points_team1'] and form['match3_points_team2'] else None
    except Exception as e:
        print(e)
        return False
    
    team1 = [team1_goalkeeper.tomic_level, team1_attacker.tomic_level]
    team2 = [team2_goalkeeper.tomic_level, team2_attacker.tomic_level]

    is_winner_team1 = 0 
    delta_team1 = [0,0]
    delta_team2 = [0,0]
    for match in [match1,match2,match3]:

        if match is not None: 
            
            if match[0] > match[1]:
                is_winner_team1 += 1
            elif match[0] < match[1]:
                is_winner_team1 -= 1

            _, _, d1, d2 = update_ratings(team1, team2, match[0], match[1])
            delta_team1 = [delta_team1[i] + d1[i] for i in range(2)]
            delta_team2 = [delta_team2[i] + d2[i] for i in range(2)]

            match_data = Match(
                team1_goalkeeper=team1_goalkeeper,
                team1_attacker=team1_attacker,
                team2_goalkeeper=team2_goalkeeper,
                team2_attacker=team2_attacker,
                team1_goals=match[0],
                team2_goals=match[1], 
            ).save()


    team1_goalkeeper.tomic_level = round(team1_goalkeeper.tomic_level + delta_team1[0], 2)
    team1_attacker.tomic_level = round(team1_attacker.tomic_level + delta_team1[1], 2)
    team2_goalkeeper.tomic_level = round(team2_goalkeeper.tomic_level + delta_team2[0], 2)
    team2_attacker.tomic_level = round(team2_attacker.tomic_level + delta_team2[1], 2)

    for player, is_winner in zip([team1_goalkeeper, team1_attacker, team2_goalkeeper, team2_attacker],[is_winner_team1 > 0, is_winner_team1 > 0, is_winner_team1 < 0, is_winner_team1 < 0]):
        player.match_total += 1
        player.match_win += int(is_winner)
        player.save()

    message = "Team 1 won!" if is_winner_team1 > 0 else "Team 2 won!" if is_winner_team1 < 0 else "It's a draw!"

    args = {
        'team1_goalkeeper': team1_goalkeeper.name,
        'team1_goalkeeper_level': team1_goalkeeper.tomic_level,
        'team1_goalkeeper_delta': round(delta_team1[0], 2),
        'team1_attacker': team1_attacker.name,
        'team1_attacker_level': team1_attacker.tomic_level,
        'team1_attacker_delta': round(delta_team1[1], 2),
        'team2_goalkeeper': team2_goalkeeper.name,
        'team2_goalkeeper_level': team2_goalkeeper.tomic_level,
        'team2_goalkeeper_delta': round(delta_team2[0], 2),
        'team2_attacker': team2_attacker.name,
        'team2_attacker_level': team2_attacker.tomic_level,
        'team2_attacker_delta': round(delta_team2[1], 2),
        'message': message
    }

    return args


def update_ratings(team_A, team_B, score_A, score_B, K=0.35, d=1.0, beta=0.1, role_weights= {'goalkeeper': 1.0, 'attacker': 1.0}):
    """
    Update player ratings for a table football match with individual adjustments.
    Each team consists of 2 players with roles 'goalkeeper' and 'attacker'. Ratings are scaled from 0 to 10.

    Parameters:
    - team_A: list, e.g., [2.0, 7.0]
    - team_B: list, e.g., [8.5, 6.0]
    - score_A: int, goals scored by Team A
    - score_B: int, goals scored by Team B
    - K: float, constant determining maximum change per match (default: 0.5)
    - d: float, scaling factor for the expected outcome formula (default: 1.0)
    - beta: float, adjustment factor for individual rating difference (default: 0.1)
    - role_weights: dict, optional custom weights for each role,ì
    """
    
    # Step 1: Calculate the team average ratings.
    team_A_avg = np.mean(team_A)
    team_B_avg = np.mean(team_B)

    # Step 2: Calculate the expected outcome using a logistic function.
    exponent = (team_B_avg - team_A_avg) / d
    E_A = 1 / (1 + math.pow(10, exponent))
    E_B = 1 - E_A

    # Step 3: Determine the actual match result.
    S_A = 1 if score_A > score_B else 0 if score_B > score_A else 0.5
    S_B = 1 - S_A if S_A != 0.5 else 0.5
    
    goal_difference = abs(score_A - score_B)
    
    # Step 4: Compute the margin multiplier M using the logarithm of the goal difference plus one.
    # Use M = 1 if there is no goal difference (to avoid a multiplier of 0).
    M = math.log(goal_difference + 1) if goal_difference > 0 else 1

    # Step 5: Calculate the base team rating change using the formula:
    # ΔR_team = K * M * (S - E)
    delta_team_A = K * M * (S_A - E_A)
    delta_team_B = K * M * (S_B - E_B)
    
    # Step 6: Update each player's rating individually.
    # We adjust each player's change based on the difference between the team average and the player's rating.
    # For the winning team, players below the average get an extra boost, while those above get less.
    # For the losing team, players above the average lose more, while those below lose less.

    # Calculate adjustment factors
    adjustment_factors_A = 1 + beta * (team_A_avg - team_A)
    adjustment_factors_B = 1 + beta * (team_B_avg - team_B)
    
    # Inverse the adjustment factor for the losing team
    if delta_team_A < 0: adjustment_factors_A = 1 - beta * (team_A_avg - team_A)
    if delta_team_B < 0: adjustment_factors_B = 1 - beta * (team_B_avg - team_B)
    
    # Calculate new ratings
    adjustment_delta_team_A = delta_team_A * adjustment_factors_A * np.array([role_weights['goalkeeper'], role_weights['attacker']])
    adjustment_delta_team_B = delta_team_B * adjustment_factors_B * np.array([role_weights['goalkeeper'], role_weights['attacker']])
    
    # Clip ratings to be within the 0 to 10 range
    new_ratings_A = np.clip(team_A + adjustment_delta_team_A, 0, 10)
    new_ratings_B = np.clip(team_B + adjustment_delta_team_B, 0, 10)
    
    return new_ratings_A.tolist(), new_ratings_B.tolist(),adjustment_delta_team_A.tolist(), adjustment_delta_team_B.tolist()
