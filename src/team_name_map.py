TEAM_NAME_MAP = {
    "Arsenal FC": "Arsenal",
    "Arsenal": "Arsenal",

    "Brighton & Hove Albion FC": "Brighton",
    "Brighton & Hove Albion": "Brighton",
    "Brighton and Hove Albion": "Brighton",
    "Brighton": "Brighton",

    "AFC Bournemouth": "Bournemouth",
    "Bournemouth AFC": "Bournemouth",
    "Bournemouth": "Bournemouth",

    "Leeds United FC": "Leeds United",
    "Leeds United": "Leeds United",

    "Real Sociedad de Fútbol": "Real Sociedad",
    "Real Sociedad": "Real Sociedad",

    "Getafe CF": "Getafe",
    "Getafe": "Getafe",

    "Liverpool FC": "Liverpool",
    "Liverpool": "Liverpool",

    "Chelsea FC": "Chelsea",
    "Chelsea": "Chelsea",

    "Manchester City FC": "Manchester City",
    "Manchester City": "Manchester City",

    "Manchester United FC": "Manchester United",
    "Manchester United": "Manchester United",

    "Tottenham Hotspur FC": "Tottenham",
    "Tottenham Hotspur": "Tottenham",
    "Tottenham": "Tottenham",

    "Wolverhampton Wanderers FC": "Wolves",
    "Wolverhampton Wanderers": "Wolves",
    "Wolves": "Wolves",

    "Newcastle United FC": "Newcastle United",
    "Newcastle United": "Newcastle United",
    "Newcastle": "Newcastle United",

    "West Ham United FC": "West Ham United",
    "West Ham United": "West Ham United",
    "West Ham": "West Ham United",

    "Nottingham Forest FC": "Nottingham Forest",
    "Nottingham Forest": "Nottingham Forest",

    "Crystal Palace FC": "Crystal Palace",
    "Crystal Palace": "Crystal Palace",

    "Fulham FC": "Fulham",
    "Fulham": "Fulham",

    "Brentford FC": "Brentford",
    "Brentford": "Brentford",

    "Burnley FC": "Burnley",
    "Burnley": "Burnley",

    "Aston Villa FC": "Aston Villa",
    "Aston Villa": "Aston Villa",

    "Everton FC": "Everton",
    "Everton": "Everton",

    "Sunderland AFC": "Sunderland",
    "Sunderland": "Sunderland",

    "Levante UD": "Levante",
    "Levante": "Levante",

    "Rayo Vallecano de Madrid": "Rayo Vallecano",
    "Rayo Vallecano": "Rayo Vallecano",

    "RCD Espanyol de Barcelona": "Espanyol",
    "Espanyol": "Espanyol",

    "Real Oviedo": "Oviedo",
    "Oviedo": "Oviedo",

    "Villarreal CF": "Villarreal",
    "Villarreal": "Villarreal",

    "Sevilla FC": "Sevilla",
    "Sevilla": "Sevilla",

    "Atlético de Madrid": "Atlético Madrid",
    "Atlético Madrid": "Atlético Madrid",

    "Athletic Club": "Athletic Bilbao",
    "Athletic Bilbao": "Athletic Bilbao",

    "CA Osasuna": "Osasuna",
    "Osasuna": "Osasuna",

    "Deportivo Alavés": "Alavés",
    "Alavés": "Alavés",

    "RCD Mallorca": "Mallorca",
    "Mallorca": "Mallorca",

    "FC Barcelona": "Barcelona",
    "Barcelona": "Barcelona",

    "RC Celta de Vigo": "Celta Vigo",
    "Celta Vigo": "Celta Vigo",

    "Real Madrid CF": "Real Madrid",
    "Real Madrid": "Real Madrid",

    "Valencia CF": "Valencia",
    "Valencia": "Valencia",

    "Girona FC": "Girona",
    "Girona": "Girona",

    "AC Milan": "AC Milan",
    "Inter Milan": "Inter Milan",
    "Juventus FC": "Juventus",
    "Juventus": "Juventus",
    "AS Roma": "AS Roma",
    "SS Lazio": "Lazio",
    "Lazio": "Lazio",
    "ACF Fiorentina": "Fiorentina",
    "Fiorentina": "Fiorentina",
    "Atalanta BC": "Atalanta BC",
    "Genoa CFC": "Genoa",
    "Genoa": "Genoa",
    "Parma Calcio 1913": "Parma",
    "Parma": "Parma",
    "Como 1907": "Como",
    "Como": "Como",
    "US Lecce": "Lecce",
    "Lecce": "Lecce",
    "Udinese Calcio": "Udinese",
    "Udinese": "Udinese",
    "Torino FC": "Torino",
    "Torino": "Torino",
    "Bologna FC 1909": "Bologna",
    "Bologna": "Bologna",
    "SSC Napoli": "Napoli",
    "Napoli": "Napoli",
    "Cagliari Calcio": "Cagliari",
    "Cagliari": "Cagliari",
    "Hellas Verona FC": "Hellas Verona",
    "Hellas Verona": "Hellas Verona",
    "US Sassuolo Calcio": "Sassuolo",
    "Sassuolo": "Sassuolo",
    "US Cremonese": "Cremonese",
    "Cremonese": "Cremonese",
    "Pisa SC": "Pisa",
    "Pisa": "Pisa"
}


def normalize_team_name(name: str):
    if not name:
        return None
    return TEAM_NAME_MAP.get(name, name)