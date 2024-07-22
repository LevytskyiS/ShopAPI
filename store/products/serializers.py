from django.forms.models import model_to_dict
from django.db import transaction
from rest_framework import serializers


from .models import (
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
)


def get_product_variant(validated_data: dict) -> ProductVariant | None:
    return ProductVariant.objects.filter(
        product_variant_code=validated_data.get("code")[:5]
    ).first()


def get_size(validated_data: dict) -> Size | None:
    return Size.objects.filter(code=validated_data.get("size")).first()


def get_color(validated_data: dict) -> Color | None:
    return Color.objects.filter(code=validated_data.get("colorCode")).first()


def get_product(validated_data: dict) -> Product | None:
    return Product.objects.filter(
        code=validated_data.get("product_variant_code")[:3]
    ).first()


def get_category(validated_data: dict) -> Category | None:
    return Category.objects.filter(name=validated_data.get("product_category")).first()


def get_gender(validated_data: dict) -> Gender | None:
    return Gender.objects.filter(name=validated_data.get("product_gender")).first()


def get_trademark(validated_data: dict) -> Trademark | None:
    return Trademark.objects.filter(trademark=validated_data.get("trademark")).first()


def get_product_type(validated_data: dict) -> ProductType | None:
    return ProductType.objects.filter(type=validated_data.get("type")).first()


def get_subtitle(validated_data: dict) -> Subtitle | None:
    return Subtitle.objects.filter(subtitle=validated_data.get("subtitle")).first()


def get_specification(validated_data: dict) -> Specification | None:
    return Specification.objects.filter(
        specification=validated_data.get("specification")
    ).first()


class CodeNameSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=50)
    name = serializers.CharField(max_length=50)


class CategorySerializer(CodeNameSerializer):

    class Meta:
        model = Category
        fields = ["id", "name", "code"]

    def validate(self, data):
        name = data.get("name")
        if name.isdigit():
            raise serializers.ValidationError({"name": "This field must be a string."})

        code = data.get("code")
        if code.isdigit():
            raise serializers.ValidationError({"code": "This field must be a string."})

        return data

    def create(self, validated_data: dict):
        instance_code = validated_data.get("code")

        with transaction.atomic():
            try:
                instance = Category.objects.get(code=instance_code)

                if model_to_dict(instance) == validated_data:
                    return instance

                instance.name = validated_data.get("name", instance.name)
                instance.code = validated_data.get("code", instance.code)
                instance.save()
                return instance

            except Category.DoesNotExist as e:
                return Category.objects.create(**validated_data)


class GenderSerializer(CodeNameSerializer):
    code = serializers.CharField(
        required=False, allow_blank=True, allow_null=True, max_length=50
    )

    class Meta:
        model = Gender
        fields = ["id", "name", "code"]

    def create(self, validated_data: dict):
        instance_name = validated_data.get("name")

        with transaction.atomic():
            try:
                instance = Gender.objects.get(name=instance_name)

                if model_to_dict(instance) == validated_data:
                    return instance

                instance.name = validated_data.get("name", instance.name)
                instance.code = validated_data.get("code", instance.code)
                instance.save()
                return instance

            except Gender.DoesNotExist as e:
                return Gender.objects.create(**validated_data)


class TrademarkSerializer(serializers.ModelSerializer):
    trademark = serializers.CharField()

    class Meta:
        model = Trademark
        fields = ["id", "trademark"]

    def validate(self, data):
        trademark = data.get("trademark")
        if trademark.isdigit():
            raise serializers.ValidationError({"name": "This field must be a string."})

        return data

    def create(self, validated_data: dict):
        instance_trademark = validated_data.get("trademark")

        with transaction.atomic():
            try:
                if instance_trademark:
                    instance = Trademark.objects.get(trademark=instance_trademark)

                if model_to_dict(instance) == validated_data:
                    return instance

                instance.trademark = validated_data.get("trademark", instance.trademark)
                instance.save()
                return instance

            except Trademark.DoesNotExist as e:
                return Trademark.objects.create(**validated_data)


class ProductTypeSerializer(serializers.ModelSerializer):
    type = serializers.CharField(required=True)

    class Meta:
        model = ProductType
        fields = ["id", "type"]

    def validate(self, data):
        trademark = data.get("type")
        if trademark.isdigit():
            raise serializers.ValidationError({"name": "This field must be a string."})

        return data

    def create(self, validated_data: dict):
        instance_type = validated_data.get("type")

        with transaction.atomic():
            try:
                if instance_type:
                    instance = ProductType.objects.get(type=instance_type)

                if model_to_dict(instance) == validated_data:
                    return instance

                instance.type = validated_data.get("type", instance.type)
                instance.save()
                return instance

            except ProductType.DoesNotExist as e:
                return ProductType.objects.create(**validated_data)


class SubtitleSerializer(serializers.ModelSerializer):
    subtitle = serializers.CharField(required=True)

    class Meta:
        model = Subtitle
        fields = ["id", "subtitle"]

    def validate(self, data):
        trademark = data.get("subtitle")
        if trademark.isdigit():
            raise serializers.ValidationError({"name": "This field must be a string."})

        return data

    def create(self, validated_data: dict):
        instance_subtitle = validated_data.get("subtitle")

        with transaction.atomic():
            try:
                if instance_subtitle:
                    instance = Subtitle.objects.get(subtitle=instance_subtitle)

                if model_to_dict(instance) == validated_data:
                    return instance

                instance.subtitle = validated_data.get("subtitle", instance.subtitle)
                instance.save()
                return instance

            except Subtitle.DoesNotExist as e:
                return Subtitle.objects.create(**validated_data)


class SpecificationSerializer(serializers.ModelSerializer):
    specification = serializers.CharField(required=True)

    class Meta:
        model = Specification
        fields = ["id", "specification"]

    def validate(self, data):
        trademark = data.get("specification")
        if trademark.isdigit():
            raise serializers.ValidationError({"name": "This field must be a string."})

        return data

    def create(self, validated_data: dict):
        instance_specification = validated_data.get("specification")

        with transaction.atomic():
            try:
                if instance_specification:
                    instance = Specification.objects.get(
                        specification=instance_specification
                    )

                if model_to_dict(instance) == validated_data:
                    return instance

                instance.specification = validated_data.get(
                    "specification", instance.specification
                )
                instance.save()
                return instance

            except Specification.DoesNotExist as e:
                return Specification.objects.create(**validated_data)


class DescriptionSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=True)

    class Meta:
        model = Description
        fields = ["id", "description"]

    def validate(self, data):
        trademark = data.get("description")
        if trademark.isdigit():
            raise serializers.ValidationError({"name": "This field must be a string."})

        return data

    def create(self, validated_data: dict):
        instance_description = validated_data.get("description")

        with transaction.atomic():
            try:
                if instance_description:
                    instance = Description.objects.get(description=instance_description)

                if model_to_dict(instance) == validated_data:
                    return instance

                instance.description = validated_data.get(
                    "description", instance.description
                )
                instance.save()
                return instance

            except Description.DoesNotExist as e:
                return Description.objects.create(**validated_data)


class ProductSerializer(CodeNameSerializer):
    category = serializers.CharField(source="product_category", write_only=True)
    category_name = serializers.CharField(
        source="product_category.name", read_only=True
    )

    gender = serializers.CharField(source="product_gender", write_only=True)
    gender_name = serializers.CharField(source="product_gender.name", read_only=True)

    trademark = serializers.CharField(write_only=True)
    trademark_name = serializers.CharField(source="trademark.trademark", read_only=True)

    type = serializers.CharField(write_only=True)
    product_type = serializers.CharField(source="type.type", read_only=True)

    subtitle = serializers.CharField(allow_null=True, write_only=True, required=False)
    subtitle_content = serializers.CharField(source="subtitle.subtitle", read_only=True)

    specification = serializers.CharField(
        allow_null=True, write_only=True, required=False
    )
    specification_content = serializers.CharField(
        source="specification.specification",
        allow_null=True,
        read_only=True,
    )

    class Meta:
        model = Product
        fields = [
            "name",
            "code",
            "category",
            "category_name",
            "gender",
            "gender_name",
            "trademark",
            "trademark_name",
            "type",
            "product_type",
            "subtitle",
            "subtitle_content",
            "specification",
            "specification_content",
        ]

    def create(self, validated_data: dict):
        instance_code = validated_data.get("code")

        with transaction.atomic():
            try:
                if instance_code:
                    instance = Product.objects.get(code=instance_code)

                if model_to_dict(instance) == validated_data:
                    return instance

                instance.name = validated_data.get("name", instance.name)
                instance.code = validated_data.get("code", instance.code)

                product_category = get_category(validated_data)
                instance.product_category = (
                    product_category if product_category else instance.product_category
                )

                product_gender = get_gender(validated_data)
                instance.product_gender = (
                    product_gender if product_gender else instance.product_gender
                )

                trademark = get_trademark(validated_data)
                instance.trademark = trademark if trademark else instance.trademark

                product_type = get_product_type(validated_data)
                instance.type = product_type if product_type else instance.type

                subtitle = get_subtitle(validated_data)
                instance.subtitle = subtitle if subtitle else instance.subtitle

                specification = get_specification(validated_data)
                instance.specification = (
                    specification if specification else instance.specification
                )

                instance.save()
                return instance

            except Product.DoesNotExist as e:
                product_category = get_category(validated_data)
                product_gender = get_gender(validated_data)
                trademark = get_trademark(validated_data)
                product_type = get_product_type(validated_data)

                subtitle = get_subtitle(validated_data)
                if not subtitle:
                    subtitle = None

                specification = get_specification(validated_data)
                if not specification:
                    specification = None

                validated_data["trademark"] = trademark
                validated_data["product_category"] = product_category
                validated_data["product_gender"] = product_gender
                validated_data["type"] = product_type
                validated_data["subtitle"] = subtitle
                validated_data["specification"] = specification
                return Product.objects.create(**validated_data)


class ColorSerializer(CodeNameSerializer):
    name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    image = serializers.URLField()

    class Meta:
        model = Color
        fields = ["id", "code", "name", "image"]

    def create(self, validated_data: dict):
        instance_code = validated_data.get("code")

        with transaction.atomic():
            try:
                if instance_code:
                    instance = Color.objects.get(code=instance_code)

                if model_to_dict(instance) == validated_data:
                    return instance

                instance.name = validated_data.get("name", instance.name)
                instance.code = validated_data.get("code", instance.code)
                instance.image = validated_data.get("image", instance.image)
                instance.save()
                return instance

            except Color.DoesNotExist as e:
                return Color.objects.create(**validated_data)


class ProductVariantSerializer(serializers.ModelSerializer):
    code = serializers.CharField(source="product_variant_code", required=True)
    colorCode = serializers.CharField(required=True, write_only=True)
    color = serializers.CharField(source="base_color.code", read_only=True)

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "code",
            "colorCode",
            "color",
        ]

    def validate(self, data):
        color = data.get("colorCode")
        code = data.get("product_variant_code")
        if len(color) != 2:
            raise serializers.ValidationError(
                {"name": "The color code must be 2 sign long."}
            )

        if len(code) != 5:
            raise serializers.ValidationError({"name": "The code must be 5 sign long."})

        return data

    def create(self, validated_data: dict):
        instance_code = validated_data.get("colorCode")

        with transaction.atomic():
            try:
                if instance_code:
                    instance = ProductVariant.objects.get(
                        product_variant_code=instance_code
                    )

                if model_to_dict(instance) == validated_data:
                    return instance

                instance.product_variant_code = validated_data.get(
                    "product_variant_code", instance.product_variant_code
                )

                instance_color = get_color(validated_data)
                instance.base_color = (
                    instance_color if instance_color else instance.base_color
                )

                product_code = get_product(validated_data)
                instance.base_product = (
                    product_code if product_code else instance.base_product
                )

                instance.save()
                return instance

            except ProductVariant.DoesNotExist as e:
                color = get_color(validated_data)
                product = get_product(validated_data)

                validated_data["base_color"] = color
                validated_data["base_product"] = product
                validated_data.pop("colorCode")
                return ProductVariant.objects.create(**validated_data)


class SizeSerializer(CodeNameSerializer):
    class Meta:
        model = Size
        fields = ["id", "code", "name"]

    def create(self, validated_data: dict):
        instance_code = validated_data.get("code")

        with transaction.atomic():
            try:
                if instance_code:
                    instance = Size.objects.get(code=instance_code)

                if model_to_dict(instance) == validated_data:
                    return instance

                instance.name = validated_data.get("name", instance.name)
                instance.code = validated_data.get("code", instance.code)
                instance.save()
                return instance

            except Size.DoesNotExist as e:
                return Size.objects.create(**validated_data)


class NomenclatureSerializer(CodeNameSerializer):
    code = serializers.CharField()
    ean = serializers.CharField(allow_blank=True)
    size = serializers.CharField(write_only=True)
    item_size = serializers.CharField(source="nomenclature_size.name", read_only=True)
    quantity = serializers.IntegerField(read_only=True)

    class Meta:
        model = Nomenclature
        fields = [
            "id",
            "code",
            "size",
            "item_size",
            "ean",
            "quantity",
        ]

    def create(self, validated_data: dict):
        instance_code = validated_data.get("code")

        with transaction.atomic():
            try:
                if instance_code:
                    instance = Nomenclature.objects.get(code=instance_code)

                if model_to_dict(instance) == validated_data:
                    return instance

                instance.code = validated_data.get("code", instance.code)

                size = get_size(validated_data)
                instance.nomenclature_size = (
                    size if size else instance.nomenclature_size
                )

                product_variant = get_product_variant(validated_data)
                instance.product_variant = (
                    product_variant if product_variant else instance.product_variant
                )

                instance.save()
                return instance

            except Nomenclature.DoesNotExist as e:
                size = get_size(validated_data)
                product_variant = get_product_variant(validated_data)

                validated_data["nomenclature_size"] = size
                validated_data["product_variant"] = product_variant
                validated_data.pop("size")
                return Nomenclature.objects.create(**validated_data)
