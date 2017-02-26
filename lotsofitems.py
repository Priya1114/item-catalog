from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Catalog, CatalogItem

engine = create_engine('sqlite:///catalogitemswithusers.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()




catalog1 = Catalog(name = "Soccer")

session.add(catalog1)
session.commit()


catalogItem1 = CatalogItem(title = "Jersey", description = "Players wear it while playing. Players are also identified by their Jersey numbers", catalog = catalog1, category = catalog1.name)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(title = "Soccer Cleats", description = "Those designed for grass pitches have studs on the outsole to aid grip.Cleats or studs are protrusions on the sole of a shoe, or on an external attachment to a shoe, that provide additional traction on a soft or slippery surface. In American English the term cleats is used synecdochically to refer to shoes featuring such protrusions. ", catalog = catalog1, category = catalog1.name)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(title = "Shin Guards", description = "A shin guard or shin pad is a piece of equipment worn on the front of a player's shin to protect them from injury. These are commonly used in sports including association football (soccer)", catalog = catalog1, category = catalog1.name)

session.add(catalogItem3)
session.commit()



catalog2 = Catalog(name = "Hockey")

session.add(catalog2)
session.commit()

catalogItem1 = CatalogItem(title = "Hockey Stick", description = "A long, thin implement with a curved end, used to hit or direct the ball or puck in hockey. ", catalog = catalog2, category = catalog2.name)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(title = "Hockey mouthguard", description = "A mouthguard is a protective device for the mouth that covers the teeth and gums to prevent and reduce injury to the teeth, arches, lips and gums. ", catalog = catalog2, category = catalog2.name)

session.add(catalogItem2)
session.commit()


catalog3 = Catalog(name = "Snowboarding")

session.add(catalog3)
session.commit()

catalogItem1 = CatalogItem(title = "Goggles", description = "A coating on the outside of the goggle lens reflects a greater amount of light than a non-mirrored lens. Letting in a decreased volume of light means less glare and increased visual clarity in bright conditions", catalog = catalog3, category = catalog3.name)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(title = "Snowboard", description = "a board for gliding on snow, resembling a wide ski, to which both feet are secured and that one rides in an upright position. ", catalog = catalog3, category = catalog3.name)

session.add(catalogItem2)
session.commit()



catalog4 = Catalog(name = "Frisbee")

session.add(catalog4)
session.commit()

catalogItem1 = CatalogItem(title = "Frisbee", description = "A concave plastic disc designed for skimming through the air as an outdoor game or amusement.", catalog = catalog4, category = catalog4.name)

session.add(catalogItem1)
session.commit()




catalog5 = Catalog(name = "Baseball")

session.add(catalog5)
session.commit()

catalogItem1 = CatalogItem(title = "Bat", description = "A baseball bat is a smooth wooden or metal club used in the sport of baseball to hit the ball after it is thrown by the pitcher. By regulation it may be no more than 2.75 inches in diameter at the thickest part and no more than 42 inches ", catalog = catalog5, category = catalog5.name)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(title = "Helmet", description = "A batting helmet is worn by batters in the game of baseball or softball. It is meant to protect the batter's head from errant pitches thrown by the pitcher.", catalog = catalog5, category = catalog5.name)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(title = "Glove", description = "A baseball glove or mitt is a large leather glove worn by baseball players of the defending team, which assists players in catching and fielding balls hit by a batter or thrown by a teammate. ", catalog = catalog5, category = catalog5.name)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(title = "Baseball Cleats", description = "Those designed for grass pitches have studs on the outsole to aid grip.Cleats or studs are protrusions on the sole of a shoe, or on an external attachment to a shoe, that provide additional traction on a soft or slippery surface. In American English the term cleats is used synecdochically to refer to shoes featuring such protrusions. ", catalog = catalog5, category = catalog5.name)

session.add(catalogItem4)
session.commit()


catalog6 = Catalog(name="Basketball")

session.add(catalog6)
session.commit()

catalogItem1 = CatalogItem(title = "Basketball", description = "Ball useed to play Basketball", catalog = catalog6, category = catalog6.name)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(title = "Basketball Shoes", description = "Basketball shoes are special shoes to have grip in the basketball field", catalog = catalog6, category = catalog6.name)

session.add(catalogItem2)
session.commit()


catalog7 = Catalog(name="Fooseball")

session.add(catalog7)
session.commit()

catalogItem1 = CatalogItem(title = "Fooseball Table", description = "The fooseball table is the main instrument required designed to do awesome goals just using your hands", catalog = catalog7, category = catalog7.name)

session.add(catalogItem1)
session.commit()


catalog8 = Catalog(name="Skating")

session.add(catalog8)
session.commit()

catalogItem1 = CatalogItem(title = "Skates", description = "Special Shoes designed to skate with wheels in the bottom", catalog = catalog8, category = catalog8.name)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(title = "Protective Gears", description = "Protection for skating", catalog = catalog8, category = catalog8.name)

session.add(catalogItem1)
session.commit()


catalog9 = Catalog(name="Rock Climbing")

session.add(catalog9)
session.commit()















print "added menu items!"

