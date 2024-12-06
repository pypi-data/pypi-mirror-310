#  SPDX-FileCopyrightText: Copyright (c) "2024" NVIDIA CORPORATION & AFFILIATES. All rights reserved.
#  SPDX-License-Identifier: Apache-2.0
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#

"""Tests for filters defined in the Nautobot Consumables app."""

from nautobot.core.testing import FilterTestCases

from nautobot_consumables import filters, models


class CheckedOutConsumableFilterSetTestCase(FilterTestCases.FilterTestCase):
    """Tests for the CheckedOutConsumableFilterSet."""

    queryset = models.CheckedOutConsumable.objects.all()
    filterset = filters.CheckedOutConsumableFilterSet

    def test_consumable_pool(self):
        """Test filtering on consumable_pool field."""
        params = {"consumable_pool": models.ConsumablePool.objects.get(name="Cable 1 Pool 1")}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_device(self):
        """Test filtering on device field."""
        consumable = models.CheckedOutConsumable.objects.get(consumable_pool__name="Cable 1 Pool 1")
        params = {"device": consumable.device}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_quantity(self):
        """Test filtering on quantity field."""
        with self.subTest(filter="exact"):
            params = {"quantity": [6]}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

        with self.subTest(filter="lt"):
            params = {"quantity__lt": [13]}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

        with self.subTest(filter="lte"):
            params = {"quantity__lte": [13]}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

        with self.subTest(filter="gt"):
            params = {"quantity__gt": [39]}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

        with self.subTest(filter="gte"):
            params = {"quantity__gte": [39]}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_search_filter(self):
        """Test the SearchFilter."""
        consumable = models.CheckedOutConsumable.objects.first()
        with self.subTest(filter="id"):
            params = {"q": consumable.pk}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

        with self.subTest(filter="pool"):
            params = {"q": "Cable"}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

        with self.subTest(filter="device"):
            params = {"q": consumable.device.name}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_tags_filter(self):
        """Skip the tags filter test for now."""
        self.skipTest("Test data has no tags.")


class ConsumableFilterSetTestCase(FilterTestCases.FilterTestCase):
    """Tests for the ConsumableFilterSet."""

    queryset = models.Consumable.objects.all()
    filterset = filters.ConsumableFilterSet

    def test_name(self):
        """Test filtering on the name field."""
        params = {"name": "Cable 1"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_consumable_type(self):
        """Test filtering on the consumable_type field."""
        params = {"consumable_type": models.ConsumableType.objects.get(name="Cable")}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 5)

    def test_manufacturer(self):
        """Test filtering on the manufacturer field."""
        consumable = models.Consumable.objects.get(name="Cable 1")
        params = {"manufacturer": consumable.manufacturer}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_product_id(self):
        """Test filtering on the product_id field."""
        params = {"product_id": ["cable_001"]}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_search_filter(self):
        """Test the SearchFilter."""
        with self.subTest(filter="id"):
            params = {"q": models.Consumable.objects.first().pk}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

        with self.subTest(filter="name"):
            params = {"q": "Cable 1"}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

        with self.subTest(filter="consumable_type"):
            params = {"q": "Cable"}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 5)

        with self.subTest(filter="manufacturer"):
            consumable = models.Consumable.objects.get(name="Cable 1")
            params = {"q": consumable.manufacturer.name}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

        with self.subTest(filter="product_id"):
            params = {"q": "cable_00"}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 5)

    def test_tags_filter(self):
        """Skip the tags filter test for now."""
        self.skipTest("Test data has no tags.")


class ConsumablePoolFilterSetTestCase(FilterTestCases.FilterTestCase):
    """Tests for the ConsumablePoolFilterSet."""

    queryset = models.ConsumablePool.objects.all()
    filterset = filters.ConsumablePoolFilterSet

    def test_name(self):
        """Test filtering on the name field."""
        params = {"name": "Cable 1 Pool 1"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_consumable(self):
        """Test filtering on the consumable field."""
        params = {"consumable": models.Consumable.objects.get(name="Cable 1")}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_location(self):
        """Test filtering on the location field."""
        pool = models.ConsumablePool.objects.get(name="Cable 1 Pool 1")
        in_location = self.filterset({"location": pool.location}, self.queryset).qs
        not_in_location = self.filterset({"location__n": pool.location}, self.queryset).qs
        self.assertEqual(in_location.count() + not_in_location.count(), self.queryset.all().count())

    def test_quantity(self):
        """Test filtering on the quantity field."""
        with self.subTest(filter="exact"):
            params = {"quantity": [13]}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

        with self.subTest(filter="lt"):
            params = {"quantity__lt": [26]}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

        with self.subTest(filter="lte"):
            params = {"quantity__lte": [26]}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

        with self.subTest(filter="gt"):
            params = {"quantity__gt": [156]}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

        with self.subTest(filter="gte"):
            params = {"quantity__gte": [130]}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 3)

    def test_search_filter(self):
        """Test the SearchFilter."""
        with self.subTest(filter="id"):
            params = {"q": models.ConsumablePool.objects.first().pk}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

        with self.subTest(filter="name"):
            params = {"q": "Cable 1"}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

        with self.subTest(filter="consumable"):
            params = {"q": "Cable"}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 5)

        with self.subTest(filter="location"):
            pool = models.ConsumablePool.objects.get(name="Cable 1 Pool 1")
            in_location = self.filterset({"q": pool.location.name}, self.queryset).qs
            not_in_location = self.filterset({"location__n": pool.location}, self.queryset).qs
            self.assertEqual(
                in_location.count(), self.queryset.all().count() - not_in_location.count()
            )

    def test_tags_filter(self):
        """Skip the tags filter test for now."""
        self.skipTest("Test data has no tags.")


class ConsumableTypeFilterSetTestCase(FilterTestCases.FilterTestCase):
    """Tests for the ConsumableTypeFilterSet."""

    queryset = models.ConsumableType.objects.all()
    filterset = filters.ConsumableTypeFilterSet

    def test_name(self):
        """Test filtering on the name field."""
        params = {"name": "Transceiver"}
        self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_search_filter(self):
        """Test the SearchFilter."""
        with self.subTest(filter="id"):
            params = {"q": models.ConsumableType.objects.get(name="Transceiver").pk}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

        with self.subTest(filter="name"):
            params = {"q": "Transceiver"}
            self.assertEqual(self.filterset(params, self.queryset).qs.count(), 1)

    def test_tags_filter(self):
        """Skip the tags filter test for now."""
        self.skipTest("Test data has no tags.")
