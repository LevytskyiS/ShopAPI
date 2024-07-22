from django.test import TestCase
from model_bakery import baker

from ..tasks import update_current_stock
from ..models import Nomenclature, ProductVariant, Size


class UpdateNomenclatureStockTest(TestCase):
    def setUp(self) -> None:
        self.mock_product_variant = baker.make(ProductVariant)
        self.mock_size = baker.make(Size)
        self.nomenclature = Nomenclature.objects.create(
            code="1234567",
            ean="12345",
            product_variant=self.mock_product_variant,
            nomenclature_size=self.mock_size,
        )

    # def test_import_stock(self):
    #     Nomenclature.objects.create(
    #         code="12345698",
    #         ean="12345",
    #         product_variant=self.mock_product_variant,
    #         nomenclature_size=self.mock_size,
    #     )
    #     result = update_current_stock()
    #     updated_item = Nomenclature.objects.get(code="1234567")
    #     self.assertEqual(result, 204)
    #     self.assertEqual(updated_item.quantity, 122244)
