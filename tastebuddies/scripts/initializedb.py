import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models import (
    DBSession,
    Cost,
    Taste,
    Base,
    Location,
    Diet,
    AgeGroup
    )


def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)
    with transaction.manager:
        tastes = [
            'Sour',
            'Sweet',
            'Salty',
            'Spicy',
            'Bitter',
            'Italian',
            'Indian',
            'Chinese',
            'American Classic',
            'German',
            'British',
            'French',
            'Vietnamese',
            'Japanese',
            'Pub',
            'Persian',
            'Mediterranian',
            'Greek',
            'Afghan',
            'Somolian',
            'Thai',
            'Barbecue',
            'Soul',
            'Ethiopian',
            'Jamaican',
            'Mexican',
            'Korean',
        ]

        for taste in tastes:
            Taste.write(taste=taste)

        diets = [
            'Vegetarian',
            'Vegan',
            'Gluten Free',
            'Low Carb'
        ]

        for diet in diets:
            Diet.write(diet=diet)

        locations = [
            'Seattle',
            'Kitsap',
            'Eastside',
            'Skagit',
            'South King'
        ]

        for location in locations:
            Location.write(city=location)

        ages = [
            '18-25',
            '25-34',
            '35-44',
            '45-54',
            '55-64',
            '65-74',
            '75+'
        ]

        for age in ages:
            AgeGroup.write(age_group=age)

        costs = [
            '$',
            '$$',
            '$$$',
            '$$$$'
        ]

        for cost in costs:
            Cost.write(cost=cost)
