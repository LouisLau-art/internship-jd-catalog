import unittest


from scripts.company_fit_profiles import get_fit_profile


class CompanyFitProfileTests(unittest.TestCase):
    def test_xiaomi_profile_prioritizes_agent_and_engineering_efficiency(self) -> None:
        profile = get_fit_profile("xiaomi")

        self.assertEqual(profile.default_top_n, 3)
        self.assertEqual(
            [target.title for target in profile.targets[:3]],
            [
                "AI Agent开发实习生",
                "Miclaw-AI agent开发实习生",
                "大模型Agent开发工程师实习生",
            ],
        )
        self.assertIn("agent", profile.preferred_lanes)
        self.assertIn("测试开发实习—武汉", profile.downrank_titles)

    def test_bilibili_profile_prioritizes_agent_application_and_python_backend(self) -> None:
        profile = get_fit_profile("bilibili")

        self.assertEqual(profile.default_top_n, 3)
        self.assertEqual(
            [target.title for target in profile.targets],
            [
                "AI开发实习生（应用工程方向）【2027届】",
                "AI创作开发实习生【2027届】",
                "AI创作系统后端实习生（Python/Flask）",
            ],
        )
        self.assertIn("agent", profile.preferred_lanes)
        self.assertIn("视频生成大模型算法实习生", profile.downrank_titles)

    def test_didi_profile_prioritizes_stability_and_business_backend(self) -> None:
        profile = get_fit_profile("didi")

        self.assertEqual(profile.default_top_n, 3)
        self.assertEqual(profile.preferred_lanes, ("stability", "backend", "platform"))
        self.assertEqual(profile.targets[0].title, "网约车技术部-后端研发实习生")
        self.assertIn("Artificial Intelligence-后端研发实习生", profile.downrank_titles)

    def test_oppo_profile_prefers_ai_agent_and_aiops_roles(self) -> None:
        profile = get_fit_profile("oppo")

        self.assertEqual(
            [target.title for target in profile.targets[:2]],
            [
                "应用开发工程师（AI Agent方向）",
                "应用开发工程师（AI Infra/AIOps方向）",
            ],
        )
        self.assertIn("agent", profile.preferred_lanes)
        self.assertIn("efficiency", profile.preferred_lanes)

    def test_kuaishou_profile_tracks_three_high_fit_targets(self) -> None:
        profile = get_fit_profile("kuaishou")

        self.assertEqual(len(profile.targets), 3)
        self.assertEqual(profile.targets[1].title, "AI Agent研发实习生（AgentOps方向）")
        self.assertEqual(profile.targets[2].resume_alias, "刘新宇-快手-AI应用开发实习生-效率工程部")

    def test_alibaba_profile_uses_current_ai_application_titles(self) -> None:
        profile = get_fit_profile("alibaba")

        self.assertEqual(
            [target.title for target in profile.targets],
            [
                "AI应用研发工程师",
                "AI Agent应用开发工程师",
                "AI应用开发工程师实习生",
            ],
        )
        self.assertEqual(profile.targets[0].resume_alias, "刘新宇-阿里巴巴-AI应用研发工程师")
        self.assertEqual(profile.targets[1].resume_alias, "刘新宇-阿里巴巴-AI-Agent应用开发工程师")

    def test_antgroup_profile_covers_transfer_and_daily_ai_roles(self) -> None:
        profile = get_fit_profile("antgroup")

        self.assertEqual(
            [target.title for target in profile.targets],
            [
                "【转正实习】AI工程师-应用方向",
                "蚂蚁数字科技-研发工程师（金融AI）",
                "蚂蚁数字科技-AI PaaS平台开发（训推/知识工程）",
            ],
        )
        self.assertEqual(profile.targets[1].resume_alias, "刘新宇-蚂蚁-研发工程师-金融AI")

    def test_xiaohongshu_profile_matches_current_product_engineer_and_java_roles(self) -> None:
        profile = get_fit_profile("xiaohongshu")

        self.assertEqual(
            [target.title for target in profile.targets],
            [
                "【27届实习】Product Engineer-产品工程师（AI应用方向）-质效研发",
                "【27届实习】Product Engineer-产品工程师（AI/全栈/应用研发方向）-商业技术",
                "Java后端开发实习生",
            ],
        )
        self.assertEqual(profile.targets[2].resume_alias, "刘新宇-小红书-Java后端AI Agent实习生")


if __name__ == "__main__":
    unittest.main()
