import graphene
from graphene_django import DjangoObjectType
from .models.requisition import Requisition
from .models.requisition_item import RequisitionItem


class RequisitionType(DjangoObjectType):
    class Meta:
        model = Requisition
        fields = "__all__"


class RequisitionItemType(DjangoObjectType):
    class Meta:
        model = RequisitionItem
        fields = "__all__"


class Query(graphene.ObjectType):
    # Requisition queries
    requisitions = graphene.List(
        RequisitionType,
        status=graphene.String(),
        priority=graphene.String(),
        requested_by=graphene.UUID(),
        requested_facility=graphene.UUID(),
        limit=graphene.Int(),
        offset=graphene.Int(),
    )

    requisition = graphene.Field(RequisitionType, id=graphene.UUID(required=True))

    # Requisition item queries
    requisition_items = graphene.List(
        RequisitionItemType,
        requisition_id=graphene.UUID(),
        product_id=graphene.UUID(),
        is_fulfilled=graphene.Boolean(),
    )

    # Healthcare specific queries
    pending_requisitions = graphene.List(RequisitionType)
    approved_requisitions = graphene.List(RequisitionType)
    rejected_requisitions = graphene.List(RequisitionType)
    fulfilled_requisitions = graphene.List(RequisitionType)
    emergency_requisitions = graphene.List(RequisitionType)

    # Dashboard statistics
    requisition_stats = graphene.JSONString()

    def resolve_requisitions(
        self,
        info,
        status=None,
        priority=None,
        requested_by=None,
        requested_facility=None,
        limit=None,
        offset=None,
    ):
        queryset = Requisition.objects.all()

        if status:
            queryset = queryset.filter(status=status)

        if priority:
            queryset = queryset.filter(priority=priority)

        if requested_by:
            queryset = queryset.filter(requested_by_id=requested_by)

        if requested_facility:
            queryset = queryset.filter(requested_facility_id=requested_facility)

        if offset:
            queryset = queryset[offset:]

        if limit:
            queryset = queryset[:limit]

        return queryset

    def resolve_requisition(self, info, id):
        return Requisition.objects.get(id=id)

    def resolve_requisition_items(
        self, info, requisition_id=None, product_id=None, is_fulfilled=None
    ):
        queryset = RequisitionItem.objects.all()

        if requisition_id:
            queryset = queryset.filter(requisition_id=requisition_id)

        if product_id:
            queryset = queryset.filter(product_id=product_id)

        if is_fulfilled is not None:
            queryset = queryset.filter(is_fulfilled=is_fulfilled)

        return queryset

    def resolve_pending_requisitions(self, info):
        return Requisition.objects.filter(status="PENDING")

    def resolve_approved_requisitions(self, info):
        return Requisition.objects.filter(status="APPROVED")

    def resolve_rejected_requisitions(self, info):
        return Requisition.objects.filter(status="REJECTED")

    def resolve_fulfilled_requisitions(self, info):
        return Requisition.objects.filter(status="FULFILLED")

    def resolve_emergency_requisitions(self, info):
        return Requisition.objects.filter(priority="EMERGENCY")

    def resolve_requisition_stats(self, info):
        from django.db.models import Count
        from django.utils import timezone
        from datetime import timedelta

        total_requisitions = Requisition.objects.count()
        pending_requisitions = Requisition.objects.filter(status="PENDING").count()
        approved_requisitions = Requisition.objects.filter(status="APPROVED").count()
        rejected_requisitions = Requisition.objects.filter(status="REJECTED").count()
        fulfilled_requisitions = Requisition.objects.filter(status="FULFILLED").count()
        emergency_requisitions = Requisition.objects.filter(
            priority="EMERGENCY"
        ).count()

        # Recent requisitions
        last_30_days = timezone.now() - timedelta(days=30)
        recent_requisitions = Requisition.objects.filter(
            created_at__gte=last_30_days
        ).count()

        # Status distribution
        status_distribution = (
            Requisition.objects.values("status")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        # Priority distribution
        priority_distribution = (
            Requisition.objects.values("priority")
            .annotate(count=Count("id"))
            .order_by("-count")
        )

        return {
            "total_requisitions": total_requisitions,
            "pending_requisitions": pending_requisitions,
            "approved_requisitions": approved_requisitions,
            "rejected_requisitions": rejected_requisitions,
            "fulfilled_requisitions": fulfilled_requisitions,
            "emergency_requisitions": emergency_requisitions,
            "recent_requisitions": recent_requisitions,
            "status_distribution": list(status_distribution),
            "priority_distribution": list(priority_distribution),
        }


class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
