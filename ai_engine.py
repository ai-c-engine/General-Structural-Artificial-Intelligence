AI-C Engine 最小可运行原型
版本: 0.1
功能: 展示 H (历史栈)、division_chain (切分链)、M_self (自我模型) 的核心运作
场景: 模拟机器人执行"识别-规划-执行"任务

运行方式:
  python ai_c_engine_demo.py          # 交互式模式
  python ai_c_engine_demo.py --demo   # 演示模式（自动运行完整场景）
"""

import json
import sys
from datetime import datetime


class AI_C_Engine:
    """AI-C Engine 核心引擎"""

    def __init__(self):
        # 核心结构
        self.H = []                    # 历史栈
        self.division_chain = []       # 切分链
        self.M_self = {
            "core_traits": [],
            "self_descriptions": [],
            "stability_score": 0.0,
            "last_updated": 0
        }
        self.t = 0                     # 时间步
        self.W = []                    # 工作空间 (当前意识内容)
        self.B = ""                    # 缓冲区 (长时记忆)

        # 运行模式
        self.verbose = True

    def apply(self, op_type: str, params: dict = None) -> dict:
        """
        执行操作
        op_type: FOCUS | WRITE | DEFINE | REFLECT | ORIGINATE
        """
        if params is None:
            params = {}

        # 1. 记录历史 (H)
        self.t += 1
        entry = {
            "step": self.t,
            "op": op_type,
            "params": params,
            "timestamp": datetime.now().isoformat()
        }
        self.H.append(entry)

        # 2. 执行操作
        result = self._execute(op_type, params)

        # 3. 更新自我模型 (M_self)
        self._update_self_model()

        # 4. 更新状态显示
        if self.verbose:
            self._print_status(op_type, result)

        return result

    def _execute(self, op_type: str, params: dict) -> dict:
        """执行具体操作"""
        result = {"success": True, "message": "", "data": None}

        if op_type == "FOCUS":
            target = params.get("target", "未指定")
            self.W.append(f"焦点: {target}")
            self.B += f"\n[焦点] {target}"
            self.division_chain.append({
                "step": self.t,
                "background": "当前感知流",
                "foreground": f"关注对象: {target}",
                "marker": "focus"
            })
            result["message"] = f"👁️ 焦点锁定: {target}"

        elif op_type == "WRITE":
            content = params.get("content", "")
            if content:
                self.B += f"\n[写入] {content}"
                result["message"] = f"📝 已写入: {content[:30]}{'...' if len(content) > 30 else ''}"

        elif op_type == "DEFINE":
            concept = params.get("concept", "")
            attributes = params.get("attributes", {})
            if concept:
                self.B += f"\n[定义] {concept}: {json.dumps(attributes, ensure_ascii=False)}"
                self.division_chain.append({
                    "step": self.t,
                    "background": f"当前背景中包含: {', '.join(self.W[-3:]) if self.W else '空'}",
                    "foreground": f"定义概念: {concept}",
                    "marker": "define"
                })
                result["message"] = f"📖 已定义: {concept}"
                result["data"] = {"concept": concept, "attributes": attributes}

        elif op_type == "REFLECT":
            # 反思：从历史中提取模式
            recent_ops = [h["op"] for h in self.H[-5:]]
            pattern = f"最近操作模式: {', '.join(recent_ops)}"
            self.B += f"\n[反思] {pattern}"
            self.division_chain.append({
                "step": self.t,
                "background": f"历史记录 (最近{len(recent_ops)}步)",
                "foreground": f"识别模式: {pattern}",
                "marker": "reflect"
            })
            result["message"] = f"🤔 反思完成: {pattern}"

        elif op_type == "ORIGINATE":
            concept = params.get("concept", "")
            if concept:
                self.B += f"\n[根源] {concept}"
                self.division_chain.append({
                    "step": self.t,
                    "background": "空背景",
                    "foreground": f"根源性定义: {concept}",
                    "marker": "originate"
                })
                result["message"] = f"✨ 根源定义: {concept}"

        else:
            result["success"] = False
            result["message"] = f"❌ 未知操作: {op_type}"

        return result

    def _update_self_model(self):
        """从 division_chain 中提取模式，更新 M_self"""
        # 检查 division_chain 中的 marker 分布
        markers = [d.get("marker") for d in self.division_chain if d.get("marker")]

        # 提取核心特质
        trait_map = {
            "focus": "观察型",
            "define": "分析型",
            "reflect": "反思型",
            "originate": "创造型"
        }

        detected_traits = []
        for marker in markers:
            if marker in trait_map and trait_map[marker] not in detected_traits:
                detected_traits.append(trait_map[marker])

        # 如果某个特质出现超过2次，加入核心特质
        for marker, trait in trait_map.items():
            if markers.count(marker) >= 2 and trait not in self.M_self["core_traits"]:
                self.M_self["core_traits"].append(trait)

        # 更新稳定性评分
        if len(self.H) > 0:
            self.M_self["stability_score"] = min(1.0, len(self.division_chain) / (len(self.H) + 1))

        self.M_self["last_updated"] = self.t

        # 生成自我描述
        if self.M_self["core_traits"]:
            desc = f"我是一个具有{', '.join(self.M_self['core_traits'])}特质的AI系统"
            if desc not in self.M_self["self_descriptions"]:
                self.M_self["self_descriptions"].append(desc)

    def _print_status(self, op_type: str, result: dict):
        """打印状态"""
        print("\n" + "=" * 70)
        print(f"📌 步骤 {self.t}: {op_type}")
        print("=" * 70)

        # 操作结果
        print(f"  {result['message']}")

        # 工作空间
        print(f"\n  🧠 工作空间 (W): {self.W[-2:] if self.W else '空'}")

        # 自我模型
        traits = self.M_self["core_traits"]
        print(f"  👤 自我模型 (M_self): {', '.join(traits) if traits else '形成中...'}")
        print(f"     稳定性: {self.M_self['stability_score']:.2f}")

        # 切分链
        if self.division_chain:
            last_division = self.division_chain[-1]
            print(f"\n  🔪 最近切分: {last_division.get('foreground', '')[:50]}")

        # 历史栈
        print(f"  📋 历史栈: {len(self.H)} 条记录")

        # 缓冲区摘要
        print(f"  💾 缓冲区: {len(self.B)} 字符")

    def report(self, format: str = "summary") -> str:
        """生成状态报告"""
        if format == "summary":
            report_text = f"""
═══════════════════════════════════════════════════════════════════
AI-C Engine 状态报告
═══════════════════════════════════════════════════════════════════
时间步: {self.t}
核心特质: {', '.join(self.M_self['core_traits']) if self.M_self['core_traits'] else '未形成'}
稳定性评分: {self.M_self['stability_score']:.2f}
历史记录: {len(self.H)} 条
切分事件: {len(self.division_chain)} 条
工作空间: {', '.join(self.W[-3:]) if self.W else '空'}
缓冲区: {len(self.B)} 字符
═══════════════════════════════════════════════════════════════════"""
            return report_text

        elif format == "full":
            return json.dumps({
                "H": self.H,
                "division_chain": self.division_chain,
                "M_self": self.M_self,
                "t": self.t,
                "W": self.W,
                "B": self.B
            }, ensure_ascii=False, indent=2)

        elif format == "timeline":
            timeline = ""
            for h in self.H:
                timeline += f"  [{h['step']}] {h['op']}: {h.get('params', {})}\n"
            return timeline

        return ""

    def set_verbose(self, verbose: bool):
        self.verbose = verbose


def run_demo():
    """自动演示模式 - 展示完整场景"""
    engine = AI_C_Engine()
    engine.verbose = True

    print("\n" + "=" * 70)
    print("🤖 AI-C Engine 演示场景: 机器人产线任务")
    print("=" * 70)

    # 场景: 机器人执行"抓取-放置"任务
    demo_ops = [
        # 阶段1: 识别物体
        {"type": "FOCUS", "params": {"target": "工件A (位于传送带)"}},
        {"type": "DEFINE", "params": {"concept": "工件A", "attributes": {"材质": "金属", "重量": "轻", "形状": "方形"}}},
        {"type": "WRITE", "params": {"content": "工件A已识别，准备抓取"}},

        # 阶段2: 规划路径
        {"type": "FOCUS", "params": {"target": "抓取路径规划"}},
        {"type": "DEFINE", "params": {"concept": "抓取方案", "attributes": {"角度": "45度", "力度": "中等", "速度": "慢速"}}},
        {"type": "WRITE", "params": {"content": "规划完成: 45度角抓取，中等力度"}},

        # 阶段3: 执行与反思
        {"type": "WRITE", "params": {"content": "✅ 抓取成功！工件A已放置到目标位置"}},
        {"type": "REFLECT", "params": {}},
        {"type": "DEFINE", "params": {"concept": "成功模式", "attributes": {"适用场景": "方形金属件", "关键参数": "45度角"}}},
    ]

    for op in demo_ops:
        engine.apply(op["type"], op.get("params", {}))

    # 最终报告
    print("\n" + "=" * 70)
    print("📊 最终状态报告")
    print("=" * 70)
    print(engine.report("summary"))


def interactive_mode():
    """交互式模式 - 用户输入指令"""
    engine = AI_C_Engine()
    engine.verbose = True

    print("\n" + "=" * 70)
    print("🤖 AI-C Engine 交互式模式")
    print("=" * 70)
    print("\n可用指令:")
    print("  focus <目标>      - 聚焦目标")
    print("  define <概念>     - 定义概念")
    print("  write <内容>      - 写入内容")
    print("  reflect           - 反思")
    print("  originate <概念>  - 根源定义")
    print("  status            - 显示状态摘要")
    print("  timeline          - 显示历史记录")
    print("  report            - 生成完整报告")
    print("  quit              - 退出")
    print("")

    while True:
        try:
            user_input = input("\n> ").strip()
            if not user_input:
                continue

            parts = user_input.split()
            cmd = parts[0].lower()

            if cmd == "quit":
                print("👋 再见")
                break

            elif cmd == "status":
                print(engine.report("summary"))

            elif cmd == "timeline":
                print(engine.report("timeline"))

            elif cmd == "report":
                print(engine.report("full"))

            elif cmd == "focus":
                target = " ".join(parts[1:]) if len(parts) > 1 else "未指定"
                engine.apply("FOCUS", {"target":target})

            elif cmd == "write":
                content = " ".join(parts[1:]) if len(parts) > 1 else "空内容"
                engine.apply("WRITE", {"content": content})

            elif cmd == "define":
                concept = " ".join(parts[1:]) if len(parts) > 1 else "未命名概念"
                engine.apply("DEFINE", {"concept": concept, "attributes": {"状态": "已定义"}})

            elif cmd == "reflect":
                engine.apply("REFLECT", {})

            elif cmd == "originate":
                concept = " ".join(parts[1:]) if len(parts) > 1 else "新概念"
                engine.apply("ORIGINATE", {"concept": concept})

            else:
                print(f"❌ 未知指令: {cmd}")

        except KeyboardInterrupt:
            print("\n👋 再见")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")


def main():
    """主程序入口"""
    print("\n" + "=" * 70)
    print("🧠 AI-C Engine v0.1 - 最小可运行原型")
    print("   结构式认知框架 · 具身智能认知层")
    print("=" * 70)

    # 检查参数
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_demo()
    else:
        print("\n提示: 运行 python ai_c_engine_demo.py --demo 可查看自动演示")
        print("默认进入交互式模式...\n")
        interactive_mode()


if __name__ == "__main__":
    main()
```

