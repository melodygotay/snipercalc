ranks = {
    "B": {
        "5": (0, 999),
        "4": (1000, 1999),
        "3": (2000, 2999),
        "2": (3000, 3999),
        "1": (4000, 4999),
    },
    "S": {
        "5": (5000, 5999),
        "4": (6000, 6999),
        "3": (7000, 7999),
        "2": (8000, 8999),
        "1": (9000, 9999),
    },
    "G": {
        "5": (10000, 10999),
        "4": (11000, 11999),
        "3": (12000, 12999),
        "2": (13000, 13999),
        "1": (14000, 14999),
    },
    "P": {
        "5": (15000, 15999),
        "4": (16000, 16999),
        "3": (17000, 17999),
        "2": (18000, 18999),
        "1": (19000, 19999),
    },
    "D": {
        "5": (20000, 20999),
        "4": (21000, 21999),
        "3": (22000, 22999),
        "2": (23000, 23999),
        "1": (24000, 24999),
    },
}

input_ranks = []

def calculate_avg(input_ranks):
    total_points = 0
    players = 0

    for rank, points in input_ranks:
        total_points += points
        players += 1
    
    if players == 0:
        return "No ranks provided."
    
    average = total_points / players

    for rank_name, levels in ranks.items():
        for level, (lower, upper) in levels.items():
            if lower <= average <= upper:
                diff = int(round(average - lower))
                return f"{rank_name}{level} {diff}"

    return "Rank not found."