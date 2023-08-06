from django.contrib import admin

from . import tasks
from .models import (
    Extraction,
    ExtractionProduct,
    MiningLedgerRecord,
    Moon,
    Notification,
    Owner,
    Refinery,
)


class ExtractionProductAdmin(admin.TabularInline):
    model = ExtractionProduct


@admin.register(Extraction)
class ExtractionAdmin(admin.ModelAdmin):
    list_display = ("chunk_arrival_at", "status", "_owner", "refinery", "_ledger")
    ordering = ("-chunk_arrival_at",)
    list_filter = ("chunk_arrival_at", "status", "refinery__owner", "refinery")
    search_fields = ("refinery__moon__eve_moon__name",)
    inlines = [ExtractionProductAdmin]
    actions = ["update_calculated_properties"]

    @admin.display(description="Update calculated properties for selected extrations.")
    def update_calculated_properties(self, request, queryset):
        num = 0
        for obj in queryset:
            tasks.update_extraction_calculated_properties.delay(extraction_pk=obj.pk)
            num += 1
        self.message_user(
            request, f"Started updating calculated properties for {num} extractions."
        )

    def _owner(self, obj):
        return obj.refinery.owner

    @admin.display(boolean=True)
    def _ledger(self, obj):
        if obj.status != Extraction.Status.COMPLETED:
            return None
        return obj.ledger.exists()

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(MiningLedgerRecord)
class MiningLedgerRecordAdmin(admin.ModelAdmin):
    list_display = ("refinery", "day", "user", "character", "ore_type", "quantity")
    ordering = ["refinery", "day", "user", "character", "ore_type"]
    list_filter = (
        "refinery",
        "day",
        "user",
        ("character", admin.RelatedOnlyFieldListFilter),
        "ore_type",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("refinery", "character", "ore_type", "user")

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Moon)
class MoonAdmin(admin.ModelAdmin):
    list_display = ("eve_moon",)

    actions = ["update_calculated_properties"]

    @admin.display(description="Update calculated properties for selected moons.")
    def update_calculated_properties(self, request, queryset):
        num = 0
        for obj in queryset:
            tasks.update_moon_calculated_properties.delay(moon_pk=obj.pk)
            num += 1
        self.message_user(
            request, f"Started updating calculated properties for {num} moons."
        )

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "notification_id",
        "owner",
        "notif_type",
        "timestamp",
        "created",
        "last_updated",
    )
    ordering = ["-timestamp"]
    list_filter = ("owner", "notif_type")

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "_alliance",
        "character_ownership",
        "is_enabled",
        "last_update_at",
        "last_update_ok",
    )
    ordering = ["corporation"]
    search_fields = ("refinery__moon__eve_moon__name",)
    list_filter = (
        "is_enabled",
        "last_update_ok",
        "corporation__alliance",
    )
    actions = ["update_owner"]

    @admin.display(ordering="corporation__alliance__alliance_name")
    def _alliance(self, obj):
        return obj.corporation.alliance

    @admin.display(description="Update selected owners from ESI")
    def update_owner(self, request, queryset):
        for obj in queryset:
            tasks.update_owner.delay(obj.pk)
            text = f"Started updating owner: {obj}. "
            self.message_user(request, text)

    def has_add_permission(self, request):
        return False

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + (
                "corporation",
                "character_ownership",
                "last_update_at",
                "last_update_ok",
            )
        return self.readonly_fields


@admin.register(Refinery)
class RefineryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "moon",
        "owner",
        "eve_type",
        "ledger_last_update_ok",
        "ledger_last_update_at",
    )
    ordering = ["name"]
    list_filter = (
        ("owner__corporation", admin.RelatedOnlyFieldListFilter),
        "ledger_last_update_ok",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related(
            "moon", "moon__eve_moon", "eve_type", "owner", "owner__corporation"
        )

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    actions = ["update_mining_ledger"]

    @admin.display(description="Update mining ledger for selected refineries from ESI")
    def update_mining_ledger(self, request, queryset):
        for obj in queryset:
            tasks.update_mining_ledger_for_refinery.delay(obj.id)
            text = f"Started updating mining ledger: {obj}. "
            self.message_user(request, text)
