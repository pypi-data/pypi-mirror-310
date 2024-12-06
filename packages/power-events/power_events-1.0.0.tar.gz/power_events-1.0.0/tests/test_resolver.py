from collections.abc import Mapping
from typing import Any, Dict

import pytest

from power_events.conditions import Neg, Value
from power_events.exceptions import MultipleRoutesError, NoRouteFoundError
from power_events.resolver import EventResolver, EventRoute


class TestEventRoute:
    def test_match(self) -> None:
        def route(event: Any) -> int:
            return 1

        assert EventRoute(route, Value("a").equals(1)).match({"a": 1})

    def test_name(self) -> None:
        def route_test_name(event: Any) -> int:
            return 1

        assert EventRoute(route_test_name, Value("a").equals(1)).name == "route_test_name"
        assert EventRoute(lambda x: x, Value("a").equals(1)).name == "<lambda>"


class TestResolver:
    def test_resolve_should_raise_no_route_when_set_to_disallow(self) -> None:
        app = EventResolver(allow_no_route=False)

        with pytest.raises(NoRouteFoundError):
            app.resolve({"a": 1})

    def test_resolve_should_raise_multiple_route_when_set_to_disallow(self) -> None:
        app = EventResolver(allow_multiple_routes=False)

        @app.equal("a.b", "TEST")
        def handle_test(_event: Mapping[str, Any]) -> str:
            return "lol"

        @app.equal("a.b", "TEST")
        def handle_test2(_event: Dict[str, Any]) -> str:
            return "lol-2"

        with pytest.raises(MultipleRoutesError):
            app.resolve({"a": {"b": "TEST"}})

    def test_equal(self) -> None:
        app = EventResolver(allow_no_route=False)

        @app.equal("a.b", "TEST")
        def handle_test(_event: Dict[str, Any]) -> str:
            return "lol"

        res = app.resolve({"a": {"b": "TEST"}})

        assert res == ["lol"]

    def test_one_of(self) -> None:
        app = EventResolver()

        @app.one_of("a", ["BAR", "FOO"])
        def handle_foo(_event: Dict[str, Any]) -> str:
            return "BAR"

        res = app.resolve({"a": "FOO"})

        assert res == ["BAR"]

    def test_contain(self) -> None:
        app = EventResolver()

        @app.one_of("a", ["BAR", "FOO"])
        def handle_contain(_event: Dict[str, Any]) -> str:
            return "BAR"

        @app.contain("a", "b", "c")
        def handle_foo(_event: Dict[str, Any]) -> str:
            return "contain"

        res = app.resolve({"a": ["b", "c"]})

        assert res == ["contain"]

    def test_resolve_multiple_routes(self) -> None:
        event = {"a": {"b": {"c": "TEST"}, "d": 1}}
        app = EventResolver(allow_multiple_routes=True)

        @app.when(Value("a.b.c").one_of(["TEST"]))
        def handle_test(_event: Dict[str, Any]) -> str:
            return "test"

        @app.equal("a.d", 1)
        def handle_d(_event: Dict[str, Any]) -> str:
            return "d"

        res = app.resolve(event)

        assert res == ["test", "d"]

    def test_readme_simple(self) -> None:
        app = EventResolver()

        @app.equal("type", "order_created")
        def handler_order_created(event: dict[str, Any]) -> str:
            return f"Order created : {event['order_id']}"

        @app.one_of("type", ["order_update", "order_delete"])
        def handle_order_modification(event: dict[str, Any]) -> str:
            return f"Order modification <{event['type']}> : {event['order_id']}"

        assert app.resolve({"type": "order_created", "order_id": "12345", "user_id": "67890"}) == [
            "Order created : 12345"
        ]

        assert app.resolve({"type": "order_delete", "order_id": "12345", "user_id": "67890"}) == [
            "Order modification <order_delete> : 12345"
        ]

    def test_readme_complex(self) -> None:
        app = EventResolver()

        # Order created and digital purchase.
        @app.when(Value("type").equals("order_created") & Value("cart.is_digital").is_truthy())
        def handle_digital_purchase(event: dict[str, Any]) -> str:
            return f"The order created is a digital purchase: {event['order_id']}"

        # Order created and physical.
        @app.when(Value("type").equals("order_created") & Neg(Value("cart.is_digital").is_truthy()))
        def handle_physical_purchase(event: dict[str, Any]) -> str:
            return f"The order created is a physical purchase: {event['order_id']}"

        assert app.resolve(
            {
                "type": "order_created",
                "order_id": "12345",
                "user_id": "67890",
                "cart": {"is_digital": True, "items": ["$10 voucher"]},
            }
        ) == ["The order created is a digital purchase: 12345"]
        assert app.resolve(
            {
                "type": "order_created",
                "order_id": "12345",
                "user_id": "67890",
                "cart": {"is_digital": False, "items": ["keyboard"]},
            }
        ) == ["The order created is a physical purchase: 12345"]
