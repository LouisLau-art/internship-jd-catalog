import unittest
from pathlib import Path


from scripts.company_registry import (
    REPO_ROOT,
    get_company_config,
    group_companies_by_scrape_group,
    parse_company_keys,
)


class CompanyRegistryTests(unittest.TestCase):
    def test_parse_company_keys_splits_dedupes_and_preserves_order(self) -> None:
        self.assertEqual(
            parse_company_keys("netease, didi,netease , oppo"),
            ["netease", "didi", "oppo"],
        )

    def test_get_company_config_returns_registered_company_metadata(self) -> None:
        company = get_company_config("didi")

        self.assertEqual(company.key, "didi")
        self.assertEqual(company.display_name, "Didi")
        self.assertEqual(company.scrape_group, "extra_bigtech")
        self.assertEqual(company.data_json, REPO_ROOT / "data" / "didi_positions_intern_tech.json")
        self.assertEqual(company.data_csv, REPO_ROOT / "data" / "didi_positions_intern_tech.csv")
        self.assertTrue(str(company.status_doc.name).endswith("extra-bigtech-crawl-status.md"))

    def test_group_companies_by_scrape_group_routes_selected_companies(self) -> None:
        grouped = group_companies_by_scrape_group(["netease", "oppo", "kuaishou"])

        self.assertEqual(list(grouped.keys()), ["extra_bigtech", "more_bigtech"])
        self.assertEqual([company.key for company in grouped["extra_bigtech"]], ["netease"])
        self.assertEqual([company.key for company in grouped["more_bigtech"]], ["oppo", "kuaishou"])

    def test_campus_core_company_uses_shared_combined_export_with_source_filter(self) -> None:
        company = get_company_config("bytedance")

        self.assertEqual(company.scrape_group, "campus_core")
        self.assertEqual(company.data_json, REPO_ROOT / "data" / "campus_positions_combined.json")
        self.assertEqual(company.data_csv, REPO_ROOT / "data" / "campus_positions_combined.csv")
        self.assertEqual(company.source_filters, ("bytedance",))
        self.assertTrue(str(company.status_doc.name).endswith("campus-core-crawl-status.md"))

    def test_unknown_company_raises_clear_error(self) -> None:
        with self.assertRaisesRegex(KeyError, "unknown company key"):
            get_company_config("baidu")


if __name__ == "__main__":
    unittest.main()
