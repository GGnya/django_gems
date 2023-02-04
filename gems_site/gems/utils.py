from pytils.translit import slugify


def title_to_slug(title):
    return slugify(title)

def replacer_empty_to_minus(slug):
    return slug.replace(' ', '-')

# slug = AutoSlugField(populate_from=(title_to_slug(self.title)),
#                          slugify=replacer_empty_to_minus(self.value),
#                          unique=True, db_index=True, verbose_name="URL")