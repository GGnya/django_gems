from pytils.translit import slugify


def title_to_slug(title):
    return slugify(title)


def replacer_empty_to_minus(slug):
    return slug.replace(' ', '-')
