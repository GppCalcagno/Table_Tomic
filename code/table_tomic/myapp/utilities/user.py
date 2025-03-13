from ..models import Player

def add_new_user(form):
                
    level_mapping = {
    'Apprendista': 3,
    'Indeterminato': 5,
    'HeadofBiliardino': 7
    }
    
    try:
        name = form['name'].lower()
        rep = form['reparto'].lower()
        tomic_level = form['level']
        tomic_level = level_mapping.get(tomic_level, 0)
    except KeyError:
        return False

    if Player.objects.filter(name=name).exists():
        return False
    
    new_player = Player(name=name, rep=rep, tomic_level=tomic_level, match_win=0, match_total=0)
    new_player.save()
    return True
    

    



