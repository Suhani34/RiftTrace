class OrganizationScopedQuerysetMixin:
    organization_lookup = (
        "organization"
    )


    def get_queryset(
        self,
    ):
        queryset = (
            super()
            .get_queryset()
        )


        user = (
            self.request.user
        )


        if not user.is_authenticated:
            return queryset.none()


        if user.is_superuser:
            return queryset


        lookup = (
            f"{self.organization_lookup}"
            "__memberships__user"
        )


        return (
            queryset
            .filter(
                **{
                    lookup:
                        user
                }
            )
            .distinct()
        )
