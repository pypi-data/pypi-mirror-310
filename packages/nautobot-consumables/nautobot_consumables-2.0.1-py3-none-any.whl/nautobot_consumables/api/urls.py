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

"""URL routes for Nautobot Consumables API endpoints."""

from nautobot.apps.api import OrderedDefaultRouter

from nautobot_consumables.api import views

router = OrderedDefaultRouter()

router.register("checked-out-consumables", views.CheckedOutConsumableAPIViewSet)
router.register("consumables", views.ConsumableAPIViewSet)
router.register("consumable-pools", views.ConsumablePoolAPIViewSet)
router.register("consumable-types", views.ConsumableTypeAPIViewSet)

app_name = "nautobot_consumables-api"
urlpatterns = router.urls
