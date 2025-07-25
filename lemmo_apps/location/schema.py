import graphene
from graphene_django import DjangoObjectType
from .models.location import Location, LocationType
from .models.facility import Facility, FacilityType, FacilityDepartment, FacilityContact


class LocationTypeType(DjangoObjectType):
    class Meta:
        model = LocationType
        fields = "__all__"


class LocationType(DjangoObjectType):
    class Meta:
        model = Location
        fields = "__all__"


class FacilityTypeType(DjangoObjectType):
    class Meta:
        model = FacilityType
        fields = "__all__"


class FacilityType(DjangoObjectType):
    class Meta:
        model = Facility
        fields = "__all__"


class FacilityDepartmentType(DjangoObjectType):
    class Meta:
        model = FacilityDepartment
        fields = "__all__"


class FacilityContactType(DjangoObjectType):
    class Meta:
        model = FacilityContact
        fields = "__all__"


class Query(graphene.ObjectType):
    # Location queries
    locations = graphene.List(
        LocationType,
        type_id=graphene.UUID(),
        is_active=graphene.Boolean(),
        search=graphene.String(),
    )

    location = graphene.Field(LocationType, id=graphene.UUID(required=True))

    location_types = graphene.List(LocationTypeType)

    # Facility queries
    facilities = graphene.List(
        FacilityType,
        facility_type_id=graphene.UUID(),
        category=graphene.String(),
        operational_status=graphene.String(),
        is_active=graphene.Boolean(),
        search=graphene.String(),
        has_pharmacy=graphene.Boolean(),
        has_laboratory=graphene.Boolean(),
        emergency_services=graphene.Boolean(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )

    facility = graphene.Field(FacilityType, id=graphene.UUID(required=True))

    facility_types = graphene.List(FacilityTypeType)

    # Healthcare specific queries
    hospitals = graphene.List(FacilityType)
    clinics = graphene.List(FacilityType)
    pharmacies = graphene.List(FacilityType)
    laboratories = graphene.List(FacilityType)
    warehouses = graphene.List(FacilityType)
    active_facilities = graphene.List(FacilityType)

    # Dashboard statistics
    facility_stats = graphene.JSONString()

    def resolve_locations(self, info, type_id=None, is_active=None, search=None):
        from .models.location import Location

        queryset = Location.objects.all()

        if type_id:
            queryset = queryset.filter(type_id=type_id)

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset

    def resolve_location(self, info, id):
        from .models.location import Location

        return Location.objects.get(id=id)

    def resolve_location_types(self, info):
        from .models.location import LocationType

        return LocationType.objects.all()

    def resolve_facilities(
        self,
        info,
        facility_type_id=None,
        category=None,
        operational_status=None,
        is_active=None,
        search=None,
        has_pharmacy=None,
        has_laboratory=None,
        emergency_services=None,
        limit=None,
        offset=None,
    ):
        from .models.facility import Facility

        queryset = Facility.objects.all()

        if facility_type_id:
            queryset = queryset.filter(facility_type_id=facility_type_id)

        if category:
            queryset = queryset.filter(category=category)

        if operational_status:
            queryset = queryset.filter(operational_status=operational_status)

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        if search:
            queryset = queryset.filter(name__icontains=search)

        if has_pharmacy is not None:
            queryset = queryset.filter(has_pharmacy=has_pharmacy)

        if has_laboratory is not None:
            queryset = queryset.filter(has_laboratory=has_laboratory)

        if emergency_services is not None:
            queryset = queryset.filter(emergency_services=emergency_services)

        if offset:
            queryset = queryset[offset:]

        if limit:
            queryset = queryset[:limit]

        return queryset

    def resolve_facility(self, info, id):
        from .models.facility import Facility

        return Facility.objects.get(id=id)

    def resolve_facility_types(self, info):
        from .models.facility import FacilityType

        return FacilityType.objects.all()

    def resolve_hospitals(self, info):
        from .models.facility import Facility

        return Facility.objects.filter(category="HOSPITAL", is_active=True)

    def resolve_clinics(self, info):
        from .models.facility import Facility

        return Facility.objects.filter(category="CLINIC", is_active=True)

    def resolve_pharmacies(self, info):
        from .models.facility import Facility

        return Facility.objects.filter(category="PHARMACY", is_active=True)

    def resolve_laboratories(self, info):
        from .models.facility import Facility

        return Facility.objects.filter(category="LABORATORY", is_active=True)

    def resolve_warehouses(self, info):
        from .models.facility import Facility

        return Facility.objects.filter(category="WAREHOUSE", is_active=True)

    def resolve_active_facilities(self, info):
        from .models.facility import Facility

        return Facility.objects.filter(is_active=True, operational_status="ACTIVE")

    def resolve_facility_stats(self, info):
        from .models.facility import Facility
        from django.db.models import Count

        total_facilities = Facility.objects.count()
        active_facilities = Facility.objects.filter(is_active=True).count()
        operational_facilities = Facility.objects.filter(
            operational_status="ACTIVE"
        ).count()

        # Category distribution
        category_distribution = (
            Facility.objects.values("category")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        # Facility types distribution
        type_distribution = (
            Facility.objects.values("facility_type__name")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        return {
            "total_facilities": total_facilities,
            "active_facilities": active_facilities,
            "operational_facilities": operational_facilities,
            "category_distribution": list(category_distribution),
            "type_distribution": list(type_distribution),
        }


class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
