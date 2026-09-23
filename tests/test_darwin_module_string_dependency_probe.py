from __future__ import annotations

from hashlib import sha1
import unittest

from scriptorium.darwin_module_string_dependency_probe import (
    _assert_source_free,
    scan_lua_dependency_surface,
)


class DarwinModuleStringDependencyProbeTests(unittest.TestCase):
    def test_literal_wiki_dependencies_are_discovered(self) -> None:
        source = """
        local a = require('Module:Alpha')
        local b = require("Модуль:Beta")
        local c = mw.loadData('Module:Gamma')
        local d = mw.loadJsonData("Модуль:Delta")
        """
        scan = scan_lua_dependency_surface(source)
        self.assertEqual(
            scan["static_wiki_module_dependencies"],
            ["Модуль:Alpha", "Модуль:Beta", "Модуль:Delta", "Модуль:Gamma"],
        )
        self.assertEqual(scan["dynamic_or_unsupported_loader_calls"], [])
        self.assertTrue(scan["scan_complete"])
        self.assertEqual(scan["source_sha1"], sha1(source.encode("utf-8")).hexdigest())

    def test_comments_do_not_create_dependencies(self) -> None:
        source = """
        -- require('Module:Commented')
        --[[ mw.loadData("Module:AlsoCommented") ]]
        local x = "require('Module:InsideString')"
        return {}
        """
        scan = scan_lua_dependency_surface(source)
        self.assertEqual(scan["static_wiki_module_dependencies"], [])
        self.assertTrue(scan["scan_complete"])

    def test_long_comments_and_strings_do_not_create_dependencies(self) -> None:
        source = """--[=[ require('Module:Commented') ]=]
local x = [=[mw.loadData("Module:InsideLongString")]=]
return {}"""
        scan = scan_lua_dependency_surface(source)
        self.assertEqual(scan["static_wiki_module_dependencies"], [])
        self.assertTrue(scan["scan_complete"])

    def test_dynamic_loader_call_is_fail_closed(self) -> None:
        scan = scan_lua_dependency_surface("local x = require(module_name)")
        self.assertEqual(scan["dynamic_or_unsupported_loader_calls"], ["require"])
        self.assertFalse(scan["scan_complete"])

    def test_non_wiki_literal_is_separated(self) -> None:
        scan = scan_lua_dependency_surface("local util = require('libraryUtil')")
        self.assertEqual(scan["static_wiki_module_dependencies"], [])
        self.assertEqual(scan["non_wiki_require_literals"], ["libraryUtil"])
        self.assertTrue(scan["scan_complete"])

    def test_source_free_guard_rejects_source_payload(self) -> None:
        with self.assertRaises(ValueError):
            _assert_source_free({"dependency_surface": {"content": "forbidden"}})


if __name__ == "__main__":
    unittest.main()
