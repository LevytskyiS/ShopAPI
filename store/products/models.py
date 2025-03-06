from django.db import models
from django.core.validators import MinValueValidator

from .mixins import CodeNameMixin


class Category(CodeNameMixin):
    pass

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Gender(CodeNameMixin):
    pass

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Gender"
        verbose_name_plural = "Genders"


class Trademark(models.Model):
    trademark = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.trademark

    class Meta:
        verbose_name = "Trademark"
        verbose_name_plural = "Trademarks"


class ProductType(models.Model):
    type = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.type

    class Meta:
        verbose_name = "Product Type"
        verbose_name_plural = "Product Types"


class Subtitle(models.Model):
    subtitle = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.subtitle

    class Meta:
        verbose_name = "Subtitle"
        verbose_name_plural = "Subtitles"


class Specification(models.Model):
    specification = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return self.specification

    class Meta:
        verbose_name = "Specification"
        verbose_name_plural = "Specifications"


class Description(models.Model):
    description = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return self.description

    class Meta:
        verbose_name = "Description"
        verbose_name_plural = "Descriptions"


class Product(CodeNameMixin):
    product_category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )
    product_gender = models.ForeignKey(
        Gender, related_name="products", on_delete=models.CASCADE
    )
    trademark = models.ForeignKey(
        Trademark, related_name="products", on_delete=models.CASCADE
    )
    type = models.ForeignKey(
        ProductType, related_name="products", on_delete=models.CASCADE
    )
    subtitle = models.ForeignKey(
        Subtitle, related_name="products", on_delete=models.CASCADE, null=True
    )
    specification = models.ForeignKey(
        Specification, related_name="products", on_delete=models.CASCADE, null=True
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Color(CodeNameMixin):
    image = models.URLField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colors"


class ProductVariant(models.Model):
    product_variant_code = models.CharField(max_length=50, null=False)
    base_color = models.ForeignKey(
        Color, related_name="product_variants", on_delete=models.CASCADE
    )
    base_product = models.ForeignKey(
        Product, related_name="variants", on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.product_variant_code

    class Meta:
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"


class Size(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Size"
        verbose_name_plural = "Sizes"


class Nomenclature(models.Model):
    code = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0, "The price must be equal or greater than 0.")],
        default=0,
    )
    quantity = models.PositiveIntegerField(default=0)
    nomenclature_size = models.ForeignKey(
        Size, related_name="nomenclatures", on_delete=models.CASCADE
    )
    product_variant = models.ForeignKey(
        ProductVariant, related_name="nomenclatures", on_delete=models.CASCADE
    )
    ean = models.CharField(max_length=15, null=True)

    def __str__(self) -> str:
        return self.code

    class Meta:
        verbose_name = "Nomenclature"
        verbose_name_plural = "Nomenclatures"


class NomenclatureStock(models.Model):
    nomenclature = models.ForeignKey(
        Nomenclature, related_name="nomenclature_stock", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nomenclature.code
