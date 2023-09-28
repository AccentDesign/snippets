from dal import autocomplete
from django.contrib.auth import get_permission_codename


class AutoCompleteView(autocomplete.Select2QuerySetView):
    paginate_by = 50
    model = None
    filter_arg = None
    create_field = None

    def get_queryset(self):
        """Returns the queryset."""

        if not self.model:
            raise NotImplementedError("AutoComplete.model must be defined.")

        if not self.filter_arg:
            raise NotImplementedError(
                "AutoComplete.filter_arg must be defined, ie name__istartswith."
            )

        if not self.request.user.is_authenticated:
            return self.model.objects.none()

        qs = self.model.objects.all()

        filter_by = "%s" % self.filter_arg

        if self.q:
            qs = qs.filter(**{filter_by: self.q})

        return qs

    def has_add_permission(self, request):
        """Return True if the user has the permission to add a model."""

        if not request.user.is_authenticated:
            return False

        opts = self.model._meta
        codename = get_permission_codename("add", opts)
        return request.user.has_perm("%s.%s" % (opts.app_label, codename))
