import random
from typing import cast, Optional

import neighborly.ai.behavior_utils as behavior_utils
from neighborly.core.character.character import GameCharacter
from neighborly.core.ecs import System, GameObject
from neighborly.core.location import Location
from neighborly.core.position import Position2D
from neighborly.core.relationship import Relationship
from neighborly.core.residence import Residence
from neighborly.core.routine import Routine
from neighborly.core.social_network import RelationshipNetwork
from neighborly.core.time import HOURS_PER_YEAR
from neighborly.core.town import Town
from neighborly.engine import NeighborlyEngine


class CharacterProcessor(System):

    def process(self, *args, **kwargs):

        delta_time: float = kwargs["delta_time"]

        relationship_net = self.world.get_resource(RelationshipNetwork)

        for character_id, character in self.world.get_component(GameCharacter):
            # if character.statuses.has_status("dead"):
            #     continue

            self._grow_older(character, delta_time)
            # self._simulate_dating(character_id, character)
            #
            # if relationship_net.get_all_relationships_with_tags(character_id, "Significant Other"):
            #     self._simulate_breakup(character_id, character)
            #
            self._socialize(character)
            #
            # if (
            #         character.age >= character.max_age
            #         and character.config.lifecycle.can_die
            # ):
            #     self._die(character_id, character)

    def _grow_older(
            self, character: GameCharacter, hours: float
    ) -> None:
        """Increase the character's age and apply flags at major milestones"""
        if character.config.lifecycle.can_age:
            character.age += hours / HOURS_PER_YEAR

        # if character.age > character.config.lifecycle.adult_age:
        #     character.statuses.add_status(AdultStatus())

    # def _simulate_dating(self, character_id: int, character: GameCharacter) -> None:
    #     """Simulate the dating life of this person."""
    #     if character.relationships.significant_other:
    #         # Don't do anything if they are already dating someone
    #         return
    #
    #     if character.age < character.config.lifecycle.marriageable_age:
    #         # They are too young to date
    #         return
    #
    #     # Ask out one of the love interests
    #     love_interests = character.relationships.get_with_flags(
    #         Connection.LOVE_INTEREST
    #     )
    #
    #     if not love_interests:
    #         return
    #
    #     person_to_ask_id = random.choice(love_interests)
    #     person_to_ask = behavior_utils.get_character(self.world, person_to_ask_id)
    #
    #     # They will accept if the other person is also one of their love interests
    #     if (
    #             character_id
    #             in person_to_ask.relationships.get_with_flags(Connection.LOVE_INTEREST)
    #             and person_to_ask.relationships.significant_other is not None
    #     ):
    #         # character.statuses.add_status(DatingStatus(person_to_ask_id))
    #         character.relationships.significant_other = person_to_ask_id
    #         character.relationships[person_to_ask_id].add_modifier(
    #             get_modifier("significant other")
    #         )
    #         # person_to_ask.statuses.add_status(DatingStatus(character_id))
    #         person_to_ask.relationships.significant_other = character_id
    #         person_to_ask.relationships[character_id].add_modifier(
    #             get_modifier("significant other")
    #         )
    #
    # def _simulate_breakup(self, character_id: int, character: GameCharacter) -> None:
    #     """Simulate the potential for divorce today in the course of this person's marriage."""
    #     # Check if this person is significantly more in love with someone else in town
    #     if character.relationships.significant_other:
    #         if not character.relationships[
    #             character.relationships.significant_other
    #         ].has_flags(Connection.LOVE_INTEREST):
    #             # Break up if dating
    #             if character.statuses.has_status("dating"):
    #                 partner_id = character.relationships.significant_other
    #                 partner = behavior_utils.get_character(self.world, partner_id)
    #                 partner.relationships.significant_other = None
    #                 partner.statuses.remove_status("dating")
    #                 partner.relationships[character_id].add_modifier(
    #                     RelationshipTag(
    #                         "break up", salience=5, spark=-10, charge=-5
    #                     )
    #                 )
    #                 partner.relationships[character_id].remove_modifier(
    #                     get_modifier("significant other")
    #                 )
    #
    #                 character.relationships.significant_other = None
    #                 character.statuses.remove_status("dating")
    #                 character.relationships[partner_id].add_modifier(
    #                     RelationshipModifier(
    #                         "break up", salience=5, spark=-10, charge=-5
    #                     )
    #                 )
    #                 character.relationships[partner_id].remove_modifier(
    #                     get_modifier("significant other")
    #                 )

    def _socialize(self, character: GameCharacter) -> None:
        """Have all the characters talk to those around them"""
        if character.location:
            location = self.world.get_gameobject(character.location).get_component(Location)
            relationship_net = self.world.get_resource(RelationshipNetwork)

            character_id = character.gameobject.id

            # Socialize
            for other_character_id in location.characters_present:
                if other_character_id == character.gameobject.id:
                    continue

                if not relationship_net.has_connection(character_id, other_character_id):
                    relationship_net.add_connection(
                        character_id,
                        other_character_id,
                        Relationship(character_id, other_character_id, )
                    )
                else:
                    relationship_net.get_connection(character_id, other_character_id).update()

                if not relationship_net.has_connection(other_character_id, character_id):
                    relationship_net.add_connection(
                        other_character_id,
                        character_id,
                        Relationship(
                            other_character_id,
                            character_id,
                        )
                    )
                else:
                    relationship_net.get_connection(other_character_id, character_id).update()

    def _die(self, character_id: int, character: GameCharacter) -> None:
        """Have a character pass away. Remove them from the simulation"""
        # character.statuses.remove_status("alive")
        # character.statuses.add_status(DeadStatus())
        ...


class RoutineProcessor(System):

    def process(self, *args, **kwargs):
        del args
        del kwargs

        date = behavior_utils.get_date(self.world)

        for entity, (character, routine) in self.world.get_components(
                GameCharacter, Routine
        ):
            character = cast(GameCharacter, character)
            routine = cast(Routine, routine)

            activity = routine.get_activity(date.weekday_str, date.hour)

            if (
                    activity
                    and type(activity.location) == str
                    and activity.location in character.location_aliases
            ):
                behavior_utils.move_character(
                    self.world,
                    entity,
                    character.location_aliases[str(activity.location)],
                )
            else:
                potential_locations = behavior_utils.get_locations(self.world)
                if potential_locations:
                    loc_id, _ = random.choice(potential_locations)
                    behavior_utils.move_character(self.world, entity, loc_id)


class CityPlanner(System):
    """Responsible for adding residents to the town"""

    def process(self, *args, **kwargs) -> None:
        # Find an empty space to build a house
        residence = self.try_build_house()
        if residence is None:
            residence = self.try_get_abandoned()

        if residence is None:
            return

        # Create a new character to live at the location
        engine = self.world.get_resource(NeighborlyEngine)
        character = engine.create_character("default")
        self.world.add_gameobject(character)
        character.get_component(GameCharacter).location = residence.id
        character.get_component(GameCharacter).location_aliases['home'] = residence.id
        residence.get_component(Residence).add_tenant(character.id, True)
        residence.get_component(Location).characters_present.append(character.id)

    def try_build_house(self) -> Optional[GameObject]:
        town = self.world.get_resource(Town)
        engine = self.world.get_resource(NeighborlyEngine)
        if town.layout.has_vacancy():
            space = town.layout.allocate_space()
            place = engine.create_place("House")
            space.place_id = place.id
            place.get_component(Position2D).x = space.position[0]
            place.get_component(Position2D).y = space.position[1]
            self.world.add_gameobject(place)
            return place
        return None

    def try_get_abandoned(self) -> Optional[GameObject]:
        residences = list(filter(lambda res: res[1].is_vacant(), self.world.get_component(Residence)))
        if residences:
            return residences[0][1].gameobject
        return None
