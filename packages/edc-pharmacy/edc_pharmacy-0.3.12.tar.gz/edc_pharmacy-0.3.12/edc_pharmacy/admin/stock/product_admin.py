from django.contrib import admin
from django_audit_fields.admin import audit_fieldset_tuple

from ...admin_site import edc_pharmacy_admin
from ...forms import ProductForm
from ...models import Product
from ..model_admin_mixin import ModelAdminMixin


@admin.register(Product, site=edc_pharmacy_admin)
class ProductAdmin(ModelAdminMixin, admin.ModelAdmin):
    change_list_title = "Pharmacy: Products"
    show_object_tools = True
    show_cancel = True
    list_per_page = 20

    form = ProductForm

    fieldsets = (
        (
            None,
            {
                "fields": (
                    [
                        "product_identifier",
                        "formulation",
                        "assignment",
                        "name",
                    ]
                )
            },
        ),
        audit_fieldset_tuple,
    )

    list_display = (
        "identifier",
        "name",
        "formulation",
        "assignment",
        "created",
        "modified",
    )
    list_filter = (
        "formulation",
        "assignment",
    )
    search_fields = (
        "product_identifier",
        "lot__lot_no",
    )
    ordering = ("product_identifier",)
    readonly_fields = ("product_identifier", "name")
    radio_fields = {"assignment": admin.VERTICAL}

    @admin.display(description="PRODUCT #", ordering="product_identifier")
    def identifier(self, obj):
        return obj.product_identifier.split("-")[0]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ("formulation", "assignment")
        return self.readonly_fields
