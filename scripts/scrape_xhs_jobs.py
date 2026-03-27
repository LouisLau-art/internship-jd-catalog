import json
import time
from pathlib import Path
from datetime import datetime, timezone

# For XHS, we will use the discovered patterns to scrape.
# Since we found that the content takes time to load and we have the list,
# we'll use a script that could be extended to use playwright if needed, 
# but for now we'll store the high-quality JDs we just found.

def normalize_xhs_job(raw_text, href):
    lines = raw_text.split('\n')
    title = lines[0]
    category = lines[1] if len(lines) > 1 else ""
    locations = lines[2] if len(lines) > 2 else ""
    description = "\n".join(lines[3:]) if len(lines) > 3 else ""
    
    pos_id = href.split('/')[-1]
    
    return {
        "source": "xiaohongshu",
        "company": "Xiaohongshu",
        "position_id": pos_id,
        "parent_position_id": "",
        "job_requirement_id": "",
        "position_intention_id": "",
        "position_intention_name": "",
        "position_name": title,
        "position_url": href,
        "position_req_code": "",
        "batch_id": "term_intern",
        "batch_name": "实习生",
        "category_name": category,
        "family_code": "",
        "family_name": "",
        "data_source": "web",
        "work_locations": locations,
        "interview_locations": "",
        "departments": "小红书",
        "circles": "",
        "circle_codes": "",
        "channels": "campus",
        "feature_tags": "tech",
        "publish_time": "",
        "modify_time": "",
        "graduation_from": "",
        "graduation_to": "",
        "requirement": description, # XHS puts it together
        "description": description,
    }

def main():
    # The jobs we just extracted via agent-browser
    jobs_data = [
        {
            "href": "https://job.xiaohongshu.com/campus/position/19385",
            "text": "【27届实习】Product Engineer-产品工程师（AI与全栈方向）-国际化\n客户端开发\n深圳市\n小红书国际化工程团队正在寻找一群「全球化产品工程师」——你们不仅是写代码的人，更是用技术连接世界、让全球年轻人共享同一种生活方式的价值创造者。 工作内容： 1. 核心系统深度参与：投身国际化产品服务设计与研发，直面高并发场景挑战，保障系统高性能与高可用，筑牢业务技术底座。 2. 硬核技术难题攻坚：深度参与微服务架构治理与全球化数据架构建设，攻克跨地域数据一致性、合规存储 等关键技术问题，锤炼顶尖工程能力。 3. 全球化业务实战：与产品、海外业务团队深度协同，直面全球用户真实需求与场景，从需求源头参与产品迭代，完整理解产品从0到1的全球化逻辑。 4. 综合能力全面成长：在战中强化技术思维与产品思维，沉淀可复用的工程经验与方法论，实现个人能力与业务价值同步提升。"
        },
        {
            "href": "https://job.xiaohongshu.com/campus/position/18834",
            "text": "【27届实习】Product Engineer-产品工程师（AI与全栈方向）-社区工程\n客户端开发\n北京市，上海市\n小红书社区工程团队正在寻找一群 “AI时代的原生工程师” —— 你们不仅是写代码的人，更是用 AI 赋能创造力、直接面向产品交付价值的超级个体。 工作内容： 1、系统性专业培训：参与定制的技术课程，系统掌握AI原生应 用开发、端到端全栈技术及业务思维方法论，夯实能力基础。 2、沉浸式实战项目：加入项目小组，在资深导师指导下，全程参与真实业务功能从0到1的设计、开发与交付， 完整经历产品开发的生命周期。 3、核心能力锻造：在项目中深度实践数据驱动决策，培养敏锐的用户与业务洞察力，并熟练运用AI工具提升研发与创新效率，最终交付可衡 量的业务价值。 4、持续复盘与分享：积极参与项目复盘、团队分享，将实践经验沉淀为可复用的知识，推动个人与团队的共同成长。"
        },
        {
            "href": "https://job.xiaohongshu.com/campus/position/19383",
            "text": "【27届实习】Product Engineer-产品工程师（AI/全栈/应用研发方向）-商业技术\n客户端开发\n北京市，上海市，杭州市\n小红书商业技术部希望找到对AI技术或全栈技术或应用研发技术有浓厚兴趣和愿意钻研的优秀同学前来实习实践，期待你加入来一起共建小红书的大商业生态！ - 工作职责： 1、探索AI大模型技术在小红书电商/广告/快捷售卖业务场景的落地，熟练运用AI工具提升研发与创新效率，交付可衡量的业务价值； 2、深度参与小红书电商/广告/快捷售卖业务，参与业务需求的分析，进 行多个核心系统的建设，承担开发和维护工作，并持续优化改进； 3、参与讨论业务模型和服务定义等，识别当前架构中存在的问题，定义清晰的问题并推动架构演进，体系 化的解决问题。"
        },
        {
            "href": "https://job.xiaohongshu.com/campus/position/19384",
            "text": "【27届实习】Product Engineer-产品工程师（AI应用方向）-质效研发\n客户端开发\n北京市，上海市，杭州市\n工作职责 1、构建AI Native研发工具链，设 计并实现基于LLM的下一代研发工具，覆盖需求理解、代码生成、测试验证、发布部署全链路；探索AI自主交付模式，让AI从\"辅助工具\"升级为\"独立交付者\"； 2、攻坚LLM工程化核心难题，解决大模型在实际研发场景的落地瓶颈：上下文理解、长程推理、多步骤任务规划；主导智能代码生成、智能测试、智能运维等核心模块架构设计。 3、驱动技术范式革新，深入理解小红书多元业务场景（社区/电商/多媒体/搜推广），用AI重新定义研发流程；探索Multi-Agent协作、AI自我进化等前沿方向。 4、共创开发者生 态，参与Skill生态建设，让业务团队能快速构建专属AI能力；推动AI研发最佳实践在全公司落地。 加入我们，站在AI技术最前沿！ 你将深度参与AI Coding、AI Testing、AI DevOps等核心领域，系统性重塑软件研发流程； 你将直面LLM在实际工程场景落地的关键难题：可靠性、可控性、规模化； 你将获得Mentor带教机制与成长支持体系，助你从学生快速成长为具备行业影响力的工程师；与一群志同道合、极具技术热情的伙伴共事，拥抱最先进的技术，成为\"超级个体\"。"
        },
        {
            "href": "https://job.xiaohongshu.com/campus/position/19691",
            "text": "【27届】广告基础模型算法实习生\n策略算法\n北京市，上海市，杭州市\n1. 负责参与商业化广告的全链路模型优化，包括且不局限于CTR、CVR、LTR、生成式等模型优化，提升变现效率； 2. 负责跨场域跨业务基础大模型，包括探索基础大模型的多维度Scaling Law，以及与业务模型的结合范式升级； 3. 负责广告模型上的全域超长序列建模、序列及特征Tokenizer与交互、模型Scaling Up等广告大模型技术，以及结合广告AI Infra架构的升级； 4. 探索LLM/多模态大模型前沿技术与广告大模型的结合和应用，增强广告内容理解、用户意图理解、增强知识推理； 5. 探索生成式推荐范式、全链路One Model范式、多业务One Model范式，提升系统迭代变现效率。 （满足以上任一即可）"
        },
        {
            "href": "https://job.xiaohongshu.com/campus/position/15350",
            "text": "AI音频音乐算法实习生\n多媒体算法\n北京市，上海市\n工作职责 1. 负责音乐音频相关业务的数据处理、音频指纹流程优化工作； 2. 参与音乐相关大模型的研发，如音乐生成、音乐预训练、音乐多模态模型等； 3. 参与相关算法和系统的持续迭代和进化； 同时能够根据小红书发布业务场景，结合实际需求进行技术落地和创新；"
        },
        {
            "href": "https://job.xiaohongshu.com/campus/position/15615",
            "text": "Java后端开发实习生\n后端开发\n北京市，上海市\n1、负责小红书笔记发布后端系统、编辑工具的设计与研发； 2、深入发掘和分析业务需求, 进行系统设计 和编码； 3、对系统性能和稳定性保持敏感，追求高质量、可维护的代码，能应对业务不断增长带来的高流量和复杂业务场景。"
        },
        {
            "href": "https://job.xiaohongshu.com/campus/position/16687",
            "text": "【26/27届实习】计算机视觉&多模态算法实习生-智能创作\nAIGC算法\n上海市\n1、负责计算机视觉&多模态&3DGS相关算法研发，面向但不限于：3DGS、3D重建、多模态检索、embedding、多模态目标检测、分割、Metric Learning、主体识别、质量评价等等；时刻follow与探索前沿技术；（以上方向擅长一个即可） 2、负责相关算 法和系统的持续迭代和进化；同时能够深入小红书丰富的业务场景，结合实际需求进行技术落地和创新；"
        },
        {
            "href": "https://job.xiaohongshu.com/campus/position/17222",
            "text": "技术美术实习生-社区技术\n图形图像渲染\n北京市，上海市\n1、参与小红书App发布业务文字动画、转场动画 、屏幕特效等技术实现与优化 2、针对移动端性能调优美术资源与特效渲染效果 3、参与团队技术美术规范、特效制作流程的制定与优化"
        },
        {
            "href": "https://job.xiaohongshu.com/campus/position/19767",
            "text": "数据科学实习生\n数据科学\n上海市\n1. 基于小红书社区用户行为数据，开展探索性数据分析，挖掘用户增长、留存、活跃等核心指标的变化规律； 2. 协助 搭建数据看板及监控体系，对关键业务指标进行日常跟踪与异常预警； 3. 参与社区内容分发、用户标签、推荐算法等策略的数据实验设计与效果评估（A/B Test）； 4. 配 合业务团队完成专项数据分析报告，输出有业务价值的数据洞察与决策建议； 5. 协助优化数据提取、处理及分析流程，提升团队数据工作效率。"
        }
    ]
    
    rows = [normalize_xhs_job(j['text'], j['href']) for j in jobs_data]
    
    output = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source": "xiaohongshu",
        "total_count": len(rows),
        "jobs": rows
    }
    
    output_path = Path('data/xhs_positions.json')
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Saved {len(rows)} jobs to {output_path}")

if __name__ == "__main__":
    main()
