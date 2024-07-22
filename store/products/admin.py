from django.contrib import admin

from .models import (
    CodeNameMixin,
    Category,
    Gender,
    Trademark,
    ProductType,
    Subtitle,
    Specification,
    Description,
    Product,
    Color,
    ProductVariant,
    Size,
    Nomenclature,
    NomenclatureStock,
)


@admin.register(CodeNameMixin)
class CodeNameMixinAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name")
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name")
    search_fields = ("name",)


@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name")
    search_fields = ("name",)


@admin.register(Trademark)
class TrademarkAdmin(admin.ModelAdmin):
    list_display = ("id", "trademark")


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "type")


@admin.register(Subtitle)
class SubtitleAdmin(admin.ModelAdmin):
    list_display = ("id", "subtitle")


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ("id", "specification")


@admin.register(Description)
class DescriptionAdmin(admin.ModelAdmin):
    list_display = ("id", "description")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "name",
        "product_category",
        "product_gender",
        "trademark",
        "type",
        "subtitle",
        "specification",
    )
    list_filter = (
        "product_category",
        "product_gender",
        "trademark",
        "type",
        "subtitle",
        "specification",
    )
    search_fields = ("name",)


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name", "image")
    search_fields = ("name",)


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product_variant_code",
        "base_color",
        "base_product",
    )
    list_filter = ("base_color", "base_product")


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "name")
    search_fields = ("name",)


@admin.register(Nomenclature)
class NomenclatureAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "quantity",
        "nomenclature_size",
        "product_variant",
        "ean",
    )
    list_filter = ("nomenclature_size", "product_variant")


@admin.register(NomenclatureStock)
class NomenclatureStockAdmin(admin.ModelAdmin):
    list_display = ("id", "nomenclature", "quantity", "timestamp")
    list_filter = ("nomenclature", "timestamp")
