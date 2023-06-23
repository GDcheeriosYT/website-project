class GPRater:
    character_factor = 0.95
    artifact_factor = 1
    weapon_factor = 1

    @staticmethod
    def generate_power_details(json_data) -> dict:
        details = {
            'rating': {
                'unweighted': 0,
                'weighted': 0
            },
            'totals': {
                'characters': {
                    'unweighted': 0,
                    'weighted': 0
                },
                'weapons': {
                    'unweighted': 0,
                    'weighted': 0
                },
                'artifacts': {
                    'unweighted': 0,
                    'weighted': 0
                }
            },
            'per object rating': {
                'characters': [],
                'weapons': [],
                'artifacts': []
            }
        }

        def attribute_rater(attribute):
            if isinstance(attribute, dict):
                attribute = attribute["buff"]
            rating = 0
            if attribute[0] == 1:  # health
                rating += attribute[2] * 1.5

            elif attribute[0] == 2:  # attack
                rating += attribute[2] * 2.5

            elif attribute[0] == 3:  # defense
                rating += attribute[2] * 1

            elif attribute[0] == 4:  # crit rate
                rating += attribute[2] * 3

            elif attribute[0] == 5:  # crit damage
                rating += attribute[2] * 2

            return rating

        power_level = 0

        # characters
        character_names = []
        character_ratings = []
        for character in json_data["inventory"]["characters"]:
            character_rating = 0
            character_name = character["name"]
            difficulty = character["experience"]["level"] / 20
            character_rating += character["star rating"]
            character_rating += character["experience"]["level"] * 2
            character_rating += (difficulty + 1) * 10
            equips = character["equips"]
            family_names = []
            for artifact in equips["artifacts"]:
                family_names.append(artifact["family"])
                character_rating += artifact["star rating"] * 1.20
                character_rating += artifact["experience"]["level"]
                character_rating += ((artifact["experience"]["level"] / 4) * 2) + 1
                character_rating += attribute_rater(artifact["stats"]["main attribute"])
                for attribute in artifact["stats"]["attributes"]:
                    character_rating += attribute_rater(attribute)

            unique_family_names = []
            for name in family_names:
                if name not in unique_family_names:
                    unique_family_names.append(name)

            name_occurences = {}

            for unique_name in unique_family_names:
                count = 0
                for name in family_names:
                    if unique_name == name:
                        count += 1

                name_occurences[unique_name] = count

            for name in name_occurences:
                if name_occurences[name] >= 3:
                    character_rating += 10

                if name_occurences[name] == 5:
                    character_rating += 5

            try:
                character_rating += equips["weapon"]["star rating"] * 1.5
                character_rating += equips["weapon"]["experience"]["level"]
                character_rating += equips["weapon"]["stats"]["attack"] / 10
                character_rating += attribute_rater(equips["weapon"]["stats"]["buff"])

            except KeyError:
                pass

            except TypeError:
                pass

            if character["experience"]["xp"] > 0 or character["experience"]["level"] > 1:
                character_names.append(character_name)
                character_ratings.append(character_rating)

        characters_sorted = sorted(character_ratings)

        zipped_characters = zip(character_ratings, character_names)

        sorted_names = [element for _, element in sorted(zipped_characters)]

        for i in range(len(sorted_names)):
            details['per object rating']['characters'].append({sorted_names[i]: characters_sorted[i]})

        # artifacts
        artifact_names = []
        artifact_ratings = []
        for artifact in json_data["inventory"]["artifacts"]:
            artifact_rating = 0
            artifact_name = artifact['name']
            artifact_rating += artifact["star rating"] * 1.20
            artifact_rating += ((artifact["experience"]["level"] / 4) * 2) + 1

            if artifact["experience"]["xp"] > 0 or artifact["experience"]["level"] > 1:
                artifact_ratings.append(artifact_rating)
                artifact_names.append(artifact_name)

        artifacts_sorted = sorted(artifact_ratings)

        zipped_artifacts = zip(artifact_ratings, artifact_names)

        sorted_names = [element for _, element in sorted(zipped_artifacts)]

        for i in range(len(sorted_names)):
            details['per object rating']['artifacts'].append({sorted_names[i]: artifacts_sorted[i]})

        # weapons
        weapon_names = []
        weapon_ratings = []
        for weapon in json_data["inventory"]["weapons"]:
            weapon_rating = 0
            weapon_name = weapon["name"]
            weapon_rating += weapon["star rating"] * 1.50
            weapon_rating += weapon["experience"]["level"] * 1.26
            weapon_rating += weapon["stats"]["attack"] / 2

            if weapon["experience"]["xp"] > 0 or weapon["experience"]["level"] > 1:
                weapon_ratings.append(weapon_rating)
                weapon_names.append(weapon_name)

        weapons_sorted = sorted(weapon_ratings)

        zipped_weapons = zip(weapon_ratings, weapon_names)

        sorted_names = [element for _, element in sorted(zipped_weapons)]

        for i in range(len(sorted_names)):
            details['per object rating']['weapons'].append({sorted_names[i]: weapons_sorted[i]})

        details['totals']['characters']['unweighted'] = sum(character_ratings)
        details['totals']['artifacts']['unweighted'] = sum(artifact_ratings)
        details['totals']['weapons']['unweighted'] = sum(weapon_ratings)

        section_pl = 0
        for character_rating in characters_sorted:
            rating = character_rating * (GPRater.character_factor ** (character_ratings.index(character_rating)))
            section_pl += rating
            power_level += rating

        details['totals']['characters']['weighted'] = section_pl

        section_pl = 0
        for artifact_rating in artifacts_sorted:
            rating = artifact_rating * (GPRater.artifact_factor ** (artifact_ratings.index(artifact_rating)))
            section_pl += rating
            power_level += rating

        details['totals']['artifacts']['weighted'] = section_pl

        section_pl = 0
        for weapon_rating in weapons_sorted:
            rating = weapon_rating * (GPRater.weapon_factor ** (weapon_ratings.index(weapon_rating)))
            section_pl += rating
            power_level += rating

        details['totals']['weapons']['weighted'] = section_pl

        details['rating']['unweighted'] = round(sum(character_ratings) + sum(artifact_ratings) + sum(weapon_ratings), 2)
        details['rating']['weighted'] = round(power_level, 2)

        return details
