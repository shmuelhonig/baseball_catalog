from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from models import Base, Users, Teams, Players


engine = create_engine('sqlite:///baseball.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Populate baseball.db with teams and players

# Team Scorpions
scorpions = Teams(name="Scorpions")
session.add(scorpions)
session.commit()

# Scorpions Roster
gutierrez = Players(name="Randal Gutierrez", position="1B", number="44",
                    handedness="L", teams=scorpions)
session.add(gutierrez)
session.commit()

walsh = Players(name="Horace Walsh", position="2B", number="12",
                handedness="R", teams=scorpions)
session.add(walsh)
session.commit()

jones = Players(name="Steve Jones", position="3B", number="71", handedness="R",
                teams=scorpions)
session.add(jones)
session.commit()

houston = Players(name="Joel Houston", position="SS", number="3",
                  handedness="R", teams=scorpions)
session.add(houston)
session.commit()

burns = Players(name="Ryan Burns", position="LF", number="19", handedness="R",
                teams=scorpions)
session.add(burns)
session.commit()

rice = Players(name="Isaac Rice", position="CF", number="33", handedness="R",
               teams=scorpions)
session.add(rice)
session.commit()

mcdonald = Players(name="Clyde Mcdonald", position="RF", number="25",
                   handedness="L", teams=scorpions)
session.add(mcdonald)
session.commit()

guerrero = Players(name="Kirk Guerrero", position="C", number="14",
                   handedness="R", teams=scorpions)
session.add(guerrero)
session.commit()

hansen = Players(name="Perry Hansen", position="P", number="1", handedness="R",
                 teams=scorpions)
session.add(hansen)
session.commit()

# Team Rebels
rebels = Teams(name="Rebels")
session.add(rebels)
session.commit()

# Rebels Roster
richardson = Players(name="Albert Richardson", position="1B", number="29",
                     handedness="R", teams=rebels)
session.add(richardson)
session.commit()

haynes = Players(name="Donnie Haynes", position="2B", number="3",
                 handedness="R", teams=rebels)
session.add(haynes)
session.commit()

chambers = Players(name="Timmy Chambers", position="3B", number="20",
                   handedness="R", teams=rebels)
session.add(chambers)
session.commit()

klein = Players(name="Brent Klein", position="SS", number="37", handedness="R",
                teams=rebels)
session.add(klein)
session.commit()

swanson = Players(name="Mack Swanson", position="LF", number="51",
                  handedness="L", teams=rebels)
session.add(swanson)
session.commit()

reyes = Players(name="Wendell Reyes", position="CF", number="29",
                handedness="L", teams=rebels)
session.add(reyes)
session.commit()

hardy = Players(name="Scott Hardy", position="RF", number="17", handedness="R",
                teams=rebels)
session.add(hardy)
session.commit()

barnett = Players(name="Guadalupe Barnett", position="C", number="16",
                  handedness="R", teams=rebels)
session.add(barnett)
session.commit()

allen = Players(name="Forrest Allen", position="P", number="11",
                handedness="L", teams=rebels)
session.add(allen)
session.commit()
