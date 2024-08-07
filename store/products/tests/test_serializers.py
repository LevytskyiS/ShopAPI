from django.test import TestCase
from model_bakery import baker

from ..mixins import CodeNameMixin
from ..models import (
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
)
from ..serializers import (
    CategorySerializer,
    GenderSerializer,
    TrademarkSerializer,
    ProductTypeSerializer,
    SubtitleSerializer,
    SpecificationSerializer,
    DescriptionSerializer,
    ProductSerializer,
    ColorSerializer,
    ProductVariantSerializer,
)


class CategorySerializerTest(TestCase):
    def setUp(self):
        self.data = {"code": "t-shirts", "name": "T-shirts"}

    def test_create_valid(self):
        serializer = CategorySerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_create_invalid(self):
        data_1 = {"code": "t-shirts", "name": ""}
        serializer_1 = CategorySerializer(data=data_1)
        self.assertFalse(serializer_1.is_valid())

        data_2 = {"code": "", "name": "T-shirts"}
        serializer_2 = CategorySerializer(data=data_2)
        self.assertFalse(serializer_2.is_valid())

        data_3 = {"name": "T-shirts"}
        serializer_3 = CategorySerializer(data=data_3)
        self.assertFalse(serializer_3.is_valid())

        data_4 = {"code": ""}
        serializer_4 = CategorySerializer(data=data_4)
        self.assertFalse(serializer_4.is_valid())

        data_5 = {}
        serializer_5 = CategorySerializer(data=data_5)
        self.assertFalse(serializer_5.is_valid())

    def test_update_valid(self):
        category_1 = Category.objects.create(**self.data)
        update_data = {
            "code": "t-shirts",
            "name": "Sweatshirts",
        }

        serializer = CategorySerializer(data=update_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        if serializer.is_valid():
            category_2 = serializer.save()

        self.assertEqual(category_1.id, category_2.id)
        self.assertEqual(category_1.code, category_2.code)
        self.assertNotEqual(category_1.name, category_2.name)
        self.assertEqual(len(Category.objects.all()), 1)

    def test_update_invalid_name(self):
        Category.objects.create(**self.data)
        update_data = {
            "code": "t-shirts",
            "name": "",
        }
        serializer = CategorySerializer(data=update_data)
        self.assertFalse(serializer.is_valid())

        update_data["name"] = "1"
        serializer = CategorySerializer(data=update_data)
        self.assertFalse(serializer.is_valid())

        update_data["name"] = None
        serializer = CategorySerializer(data=update_data)
        self.assertFalse(serializer.is_valid())

        update_data["name"] = []
        serializer = CategorySerializer(data=update_data)
        self.assertFalse(serializer.is_valid())

        update_data.pop("name")
        serializer = CategorySerializer(data=update_data)
        self.assertFalse(serializer.is_valid())

    def test_update_invalid_code(self):
        update_data = {
            "code": "",
            "name": "T-shirts",
        }
        serializer = CategorySerializer(data=update_data)
        self.assertFalse(serializer.is_valid())

        update_data["code"] = "1"
        serializer = CategorySerializer(data=update_data)
        self.assertFalse(serializer.is_valid())

        update_data["code"] = None
        serializer = CategorySerializer(data=update_data)
        self.assertFalse(serializer.is_valid())

        update_data["code"] = []
        serializer = CategorySerializer(data=update_data)
        self.assertFalse(serializer.is_valid())

        update_data.pop("code")
        serializer = CategorySerializer(data=update_data)
        self.assertFalse(serializer.is_valid())

    def test_contains_expected_fields(self):
        serializer = CategorySerializer(data=self.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
        self.assertEqual(set(data.keys()), {"id", "name", "code"})


class GenderSerializerTest(TestCase):
    def setUp(self):
        self.data = {"name": "Kids", "code": "KIDS"}
        self.gender = Gender.objects.create(**self.data)

    def test_create_valid_data(self):
        serializer = GenderSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        if serializer.is_valid():
            serializer.save()
        gender = Gender.objects.get(name=self.data["name"])
        self.assertTrue(self.data["name"], gender.name)
        self.assertTrue(self.data["code"], gender.code)

    def test_create_invalid(self):
        data_1 = {"name": "Ladies", "code": ""}
        serializer_1 = GenderSerializer(data=data_1)
        self.assertTrue(serializer_1.is_valid())

        data_2 = {"name": "", "code": "UNISEX"}
        serializer_2 = GenderSerializer(data=data_2)
        self.assertFalse(serializer_2.is_valid())

        data_3 = {"name": "Gents"}
        serializer_3 = GenderSerializer(data=data_3)
        self.assertTrue(serializer_3.is_valid())

        data_4 = {"code": "KIDS/GENTS"}
        serializer_4 = GenderSerializer(data=data_4)
        self.assertFalse(serializer_4.is_valid())

        data_5 = {}
        serializer_5 = GenderSerializer(data=data_5)
        self.assertFalse(serializer_5.is_valid())

        data_6 = {"name": "Gents" * 200}
        serializer_6 = GenderSerializer(data=data_6)
        self.assertFalse(serializer_6.is_valid())

        data_7 = {"code": "GENTS" * 200}
        serializer_7 = GenderSerializer(data=data_7)
        self.assertFalse(serializer_7.is_valid())

    def test_update_valid(self):
        update_data = {
            "code": "CHILDREN",
            "name": "Kids",
        }

        serializer = GenderSerializer(data=update_data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        gender = serializer.save()
        self.assertEqual(gender.code, update_data["code"])
        self.assertEqual(gender.name, update_data["name"])

    def test_update_invalid_name(self):
        self.data["name"] = None
        serializer = GenderSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        self.data["name"] = ""
        serializer = GenderSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        self.data.pop("name")
        serializer = GenderSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

    def test_update_code(self):
        self.data["code"] = None
        serializer = GenderSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        obj: Gender = serializer.save()
        self.assertEqual(obj.code, None)

        self.data["code"] = 23
        serializer = GenderSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        obj: Gender = serializer.save()
        self.assertEqual(obj.code, "23")

        self.data["code"] = ""
        serializer = GenderSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())
        obj: Gender = serializer.save()
        self.assertEqual(obj.code, "")

        self.data["code"] = []
        serializer = GenderSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        self.data["code"] = {}
        serializer = GenderSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        self.data["code"] = "a" * 51
        serializer = GenderSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())


class TrademarkSerializerTest(TestCase):
    def setUp(self) -> None:
        self.data = {"trademark": "Universe"}
        self.trademark = Trademark.objects.create(**self.data)

    def test_create_valid_data(self):
        data = {"trademark": "Space"}
        serializer = TrademarkSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        if serializer.is_valid():
            trademark: Trademark = serializer.save()
        self.assertEqual(trademark.trademark, data["trademark"])

    def test_create_invalid_data(self):
        data = {"trademark": ""}
        serializer = TrademarkSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        data = {"trademark": None}
        serializer = TrademarkSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        data = {"trademark": False}
        serializer = TrademarkSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        data = {"trademark": 123}
        serializer = TrademarkSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        data = {}
        serializer = TrademarkSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class ProductTypeSerializerTest(TestCase):
    def setUp(self) -> None:
        self.type = ProductType.objects.create(type="Boots")

    def test_create_valid_data(self):
        data = {"type": "Clothes"}
        serializer = ProductTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        if serializer.is_valid():
            prod_type: ProductType = serializer.save()
        self.assertEqual(prod_type.type, data["type"])

    def test_create_invalid_data(self):
        data = {"type": ""}
        serializer = ProductTypeSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        data = {"type": None}
        serializer = ProductTypeSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        data = {"type": False}
        serializer = ProductTypeSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        data = {"type": 123}
        serializer = ProductTypeSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        data = {}
        serializer = ProductTypeSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class SubtitleSerializerTest(TestCase):
    def setUp(self) -> None:
        self.subtitle = Subtitle.objects.create(subtitle="Cap unisex")

    def test_create_valid_data(self):
        data = {"subtitle": "Vest men’s"}
        serializer = SubtitleSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        if serializer.is_valid():
            subtitle: Subtitle = serializer.save()
        self.assertEqual(subtitle.subtitle, data["subtitle"])

    def test_create_invalid_data(self):
        data = {"subtitle": ""}
        serializer = SubtitleSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        data = {"subtitle": None}
        serializer = SubtitleSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        data = {"subtitle": False}
        serializer = SubtitleSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        data = {"subtitle": 123}
        serializer = SubtitleSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        data = {}
        serializer = SubtitleSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class SpecificationSerializerTest(TestCase):
    def setUp(self) -> None:
        self.specification = Specification.objects.create(
            specification="Plain weave, 100 % cotton"
        )

    def test_create_valid_data(self):
        data = {"specification": "Single Jersey, 100 % cotton, silicone finish"}
        serializer = SpecificationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        if serializer.is_valid():
            specification: Specification = serializer.save()
        self.assertEqual(specification.specification, data["specification"])

    def test_create_invalid_data(self):
        data = {"specification": ""}
        serializer = SpecificationSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        data = {"specification": None}
        serializer = SpecificationSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        data = {"specification": False}
        serializer = SpecificationSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        data = {"specification": 123}
        serializer = SpecificationSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        data = {}
        serializer = SpecificationSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class DescriptionSerializerTest(TestCase):
    def setUp(self) -> None:
        self.description = Description.objects.create(
            description="cut in 'military' style, stitched, slightly curved peak, sweatband, size adjustable by velcro,"
        )

    def test_create_valid_data(self):
        data = {
            "description": "slight fit cut with side seams, neckline trimmed with shell fabric, fixing shoulder seams, shorter sleeves, silicone finish"
        }
        serializer = DescriptionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        if serializer.is_valid():
            description: Description = serializer.save()
        self.assertEqual(description.description, data["description"])

    def test_create_invalid_data(self):
        data = {"description": ""}
        serializer = DescriptionSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        data = {"description": None}
        serializer = DescriptionSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        data = {"description": False}
        serializer = DescriptionSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        data = {"description": 123}
        serializer = DescriptionSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        data = {}
        serializer = DescriptionSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class ProductSerializerTest(TestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(
            **{"code": "t-shirts", "name": "T-shirts"}
        )
        self.gender = Gender.objects.create(**{"name": "Kids", "code": "KIDS"})
        self.trademark = baker.make(Trademark)
        self.type = baker.make(ProductType)
        self.subtitle = baker.make(Subtitle)
        self.specification = baker.make(Specification)
        self.data = {
            "category": self.category.name,
            "gender": self.gender.name,
            "trademark": self.trademark.trademark,
            "type": self.type.type,
            "subtitle": self.subtitle.subtitle,
            "specification": self.specification.specification,
            "name": "Breath",
            "code": "123",
        }
        self.product = Product.objects.create(
            name="Standard Gents",
            code="555",
            product_category=self.category,
            product_gender=self.gender,
            trademark=self.trademark,
            type=self.type,
            subtitle=self.subtitle,
            specification=self.specification,
        )

    def test_create_valid_data(self):
        self.data["name"] = "Cool Gents"
        self.data["code"] = "351"
        serializer = ProductSerializer(data=self.data)
        self.assertTrue(serializer.is_valid(raise_exception=True))
        if serializer.is_valid():
            product: Product = serializer.save()
        self.assertEqual(product.name, self.data["name"])

        self.data["subtitle"] = None
        self.data["specification"] = None
        serializer = ProductSerializer(data=self.data)
        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_create_invalid_category(self):
        self.data["name"] = None
        serializer = ProductSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

    def test_create_invalid_gender(self):
        self.data["gender"] = None
        serializer = ProductSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

    def test_create_invalid_trademark(self):
        self.data["trademark"] = None
        serializer = ProductSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

    def test_create_invalid_type(self):
        self.data["type"] = None
        serializer = ProductSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

    def test_create_invalid_name(self):
        self.data["name"] = None
        serializer = ProductSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

    def test_create_invalid_code(self):
        self.data["code"] = None
        serializer = ProductSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())


class ColorSerializerTest(TestCase):
    def setUp(self) -> None:
        self.data = {
            "code": "t-shirts",
            "name": "T-shirts",
            "image": "https://upload.wikimedia.org/wikipedia/en/8/84/TestImage.jpg",
        }
        self.category = Color.objects.create(**self.data)

    def test_create_valid_data(self):
        serializer = ColorSerializer(data=self.data)
        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_create_invalid_name(self):
        self.data["name"] = None
        serializer = ColorSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_create_invalid_code(self):
        self.data["code"] = None
        serializer = ColorSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        self.data["code"] = {"test": "test"}
        serializer = ColorSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

    def test_create_invalid_image(self):
        self.data["image"] = None
        serializer = ColorSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        self.data["image"] = "12345"
        serializer = ColorSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        self.data["image"] = ["12345"]
        serializer = ColorSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        self.data["image"] = 12345
        serializer = ColorSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())


class ProductVariantSerializerTest(TestCase):
    def setUp(self) -> None:
        self.product_variant_code = "12300"
        self.color = baker.make(Color, code="11", name="Yellow")
        self.product = baker.make(Product)
        self.data = {
            "code": self.product_variant_code,
            "colorCode": self.color.code,
        }
        self.product = ProductVariant.objects.create(
            product_variant_code=self.product_variant_code,
            base_color=self.color,
            base_product=self.product,
        )

    def test_create_valid_data(self):
        serializer = ProductVariantSerializer(data=self.data)
        self.assertTrue(serializer.is_valid(raise_exception=True))

    def test_create_invalid_code(self):
        self.data["code"] = None
        serializer = ProductVariantSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

    def test_create_invalid_color_code(self):
        self.data["colorCode"] = None
        serializer = ProductVariantSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        self.data["colorCode"] = "A51"
        serializer = ProductVariantSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

        self.data["colorCode"] = "1"
        serializer = ProductVariantSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())

    def test_create_invalid_base_product(self):
        self.data["code"] = "11"
        serializer = ProductVariantSerializer(data=self.data)
        self.assertFalse(serializer.is_valid())
