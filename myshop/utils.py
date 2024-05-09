from django.forms.utils import ErrorList


class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ""
        return f"""
            <div>
                <ul class="mt-3 alert alert-danger">
                    {''.join(['<li class="text-danger">%s</li>' % e for e in self])}
                </ul>
            </div>
         """


class DivErrorList2(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self:
            return ""
        return f"""
            <div>
                <ul class="alert alert-danger">
                    {''.join(['<li class="text-danger">%s</li>' % e for e in self])}
                </ul>
            </div>
         """


from django.utils.text import slugify


def generate_unique_slug(model_instance, slug_field_name, target_field_name):
    """
    Generate a unique slug for a model instance.

    :param model_instance: The instance of the model for which the slug is generated.
    :param slug_field_name: The name of the slug field in the model.
    :param target_field_name: The name of the field used to generate the slug.
    """
    slug = slugify(getattr(model_instance, target_field_name))
    unique_slug = slug
    suffix = 1
    model_class = model_instance.__class__

    while model_class.objects.filter(**{slug_field_name: unique_slug}).exclude(id=model_instance.id).exists():
        unique_slug = f"{slug}-{suffix}"
        suffix += 1

    return unique_slug
