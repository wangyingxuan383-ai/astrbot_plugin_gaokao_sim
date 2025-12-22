import json
import os
import random
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger, AstrBotConfig
from astrbot.core.utils.astrbot_path import get_astrbot_data_path

# 尝试导入绘图库
try:
    from PIL import Image, ImageDraw, ImageFont
    import matplotlib.pyplot as plt
    HAS_VISUAL = True
except ImportError:
    HAS_VISUAL = False
    logger.warning("未安装 PIL 或 matplotlib，可视化功能将不可用。请运行 pip install pillow matplotlib")

# 常量定义
SUBJECTS_CONFIG = {
    "文科": {
        "subjects": ["语文", "数学", "英语", "政治", "历史", "地理"],
        "teachers": ["张", "李", "王", "赵", "钱", "孙"]
    },
    "理科": {
        "subjects": ["语文", "数学", "英语", "物理", "化学", "生物"],
        "teachers": ["刘", "陈", "杨", "黄", "周", "吴"]
    }
}

MONTHS = ["9月", "10月", "11月", "12月", "1月", "2月", "3月", "4月", "5月", "6月"]

# 扩展性格类型
PERSONALITY_TYPES = {
    "勤奋型": {"fail_chance": -0.20, "desc": "失败概率降低20%", "stress_resist": 0.1},
    "聪明型": {"success_bonus": 0.15, "desc": "成功时效果提升15%", "quiz_rate": 0.1},
    "乐观型": {"fail_penalty_reduce": 0.4, "desc": "失败时扣分减少40%", "stress_recovery": 0.2},
    "天才型": {"fail_chance": -0.1, "success_bonus": 0.1, "desc": "全面学习能力提升", "energy_cost": 0},
    "稳重型": {"fail_chance": -0.15, "fail_penalty_reduce": 0.2, "desc": "稳定发挥型选手", "stress_resist": 0.2},
    "冒险型": {"success_bonus": 0.25, "fail_chance": 0.1, "desc": "高风险高回报", "crit_rate": 0.1},
    "懒散型": {"fail_chance": 0.25, "desc": "失败概率增加25%", "energy_max": -1}, # 甚至可能减少体力上限
    "紧张型": {"fail_chance": 0.15, "fail_penalty_reduce": -0.2, "desc": "容易紧张失误", "stress_gain": 0.2},
    "普通型": {"desc": "无特殊效果"},
    "幸运型": {"success_bonus": 0.1, "fail_penalty_reduce": 0.2, "desc": "运气较好型", "event_luck": 0.2},
    "坚韧型": {"desc": "压力上限更高", "stress_max_bonus": 20}
}

# 事件描述（LLM 不可用时的兜底）
SUCCESS_EVENTS = [
    "认真听课收获颇丰",
    "刷题效果显著提升",
    "找到学习方法窍门",
    "模拟考试发挥出色",
    "课后复习巩固知识",
    "请教老师解决难题"
]

FAIL_EVENTS = [
    "上课走神错过重点",
    "考前紧张发挥失常",
    "学习方法不对路",
    "沉迷手机影响学习",
    "复习计划混乱",
    "熬夜太多状态不佳"
]

DYNAMIC_EVENT_RATE = 0.3

# 简约护眼主题色
THEME = {
    "bg": (238, 245, 232),
    "text": (47, 47, 47),
    "primary": (45, 106, 79),
    "secondary": (168, 203, 176),
    "border": (215, 227, 209),
}

FALLBACK_QUIZ_BANK = {
    "语文": {
        "question": "下列词语中有错别字的一项是：",
        "options": ["A. 万籁俱寂", "B. 迫不及待", "C. 应接不瑕", "D. 全神贯注"],
        "answer": "C",
        "analysis": "C 项应为“应接不暇”。"
    },
    "数学": {
        "question": "若 a=2，则 2a+3 的值为：",
        "options": ["A. 5", "B. 6", "C. 7", "D. 8"],
        "answer": "C",
        "analysis": "代入 a=2，2a+3=7。"
    },
    "英语": {
        "question": "Choose the correct word: I ____ to school every day.",
        "options": ["A. go", "B. goes", "C. going", "D. gone"],
        "answer": "A",
        "analysis": "主语 I 后用动词原形 go。"
    },
    "通用": {
        "question": "下列哪一项属于自然科学？",
        "options": ["A. 物理学", "B. 历史学", "C. 文学", "D. 哲学"],
        "answer": "A",
        "analysis": "物理学是自然科学。"
    }
}

def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(value, high))

# 大学分数线
UNIVERSITY_TIERS = {
    (650, 750): {"name": "顶尖985大学", "desc": "清华北大级别的顶尖学府！", "emoji": "🎓"},
    (600, 649): {"name": "优秀985大学", "desc": "985重点大学，前途光明", "emoji": "🏫"},
    (550, 599): {"name": "普通985/211大学", "desc": "不错的重点大学", "emoji": "📚"},
    (500, 549): {"name": "普通一本大学", "desc": "一本院校，继续努力", "emoji": "✅"},
    (450, 499): {"name": "二本大学", "desc": "二本院校，还有提升空间", "emoji": "📝"},
    (400, 449): {"name": "三本大学", "desc": "三本院校，需要加倍努力", "emoji": "⚠️"},
    (0, 399): {"name": "专科院校", "desc": "专科院校，建议复读", "emoji": "💔"}
}

class GaokaoGame:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.started = False
        self.current_month = 0
        self.subject_type = ""
        self.subjects: Dict[str, int] = {}
        self.teachers: Dict[str, str] = {}
        self.favorite_subject = ""
        self.dislike_subject = ""
        self.initial_scores: Dict[str, int] = {}
        self.personality = ""
        self.history_high_score = 0
        self.final_scores: Dict[str, int] = {}
        self.is_debug_mode = False
        self.group_id = ""
        
        # 新增属性
        self.stress = 0 # 压力值 0-100
        self.energy = 5 # 当前体力
        self.max_energy = 5 # 体力上限
        self.last_update_date = None # 上次操作日期 (用于每日重置体力)
        self.month_progress = 0 # 月份推进的行动计数
        
        self.pending_quiz_answer = None # 等待回答的测验答案 (A/B/C/D)
        self.quiz_subject = None
        self.pending_quiz_analysis = None
        self.history_scores_record = [] # 记录每月的总分，用于绘图

    def initialize_game(self, group_id: str = "", config: dict = None):
        """初始化游戏数据"""
        self.subject_type = random.choice(["文科", "理科"])
        subject_config = SUBJECTS_CONFIG[self.subject_type]
        self.group_id = group_id
        
        self.subjects = {}
        self.initial_scores = {}
        
        for subject in subject_config["subjects"]:
            # 基础分波动加大
            if subject in ["语文", "数学", "英语"]:
                score = random.randint(60, 110)
            else:
                score = random.randint(40, 70)
            self.subjects[subject] = score
            self.initial_scores[subject] = score
        
        # 记录初始成绩
        self.history_scores_record = [sum(self.subjects.values())]

        teacher_names = subject_config["teachers"]
        self.teachers = {}
        for i, subject in enumerate(subject_config["subjects"]):
            self.teachers[subject] = f"{teacher_names[i]}{subject[0]}老师"
        
        all_subjects = subject_config["subjects"].copy()
        self.favorite_subject = random.choice(all_subjects)
        all_subjects.remove(self.favorite_subject)
        self.dislike_subject = random.choice(all_subjects) if all_subjects else self.favorite_subject
        
        self.personality = random.choice(list(PERSONALITY_TYPES.keys()))
        
        # 应用性格对初始属性的影响
        self.max_energy = int(config.get("daily_energy", 5)) if config else 5
        if self.personality == "懒散型":
            self.max_energy = max(3, self.max_energy - 1)
        elif self.personality == "坚韧型":
            self.max_energy += 1
        self.max_energy = max(1, self.max_energy)

        self.energy = self.max_energy
        self.stress = 0
        self.current_month = 0
        self.month_progress = 0
        self.started = True
        self.last_update_date = datetime.now().date().isoformat()
        self.is_debug_mode = False
        self.pending_quiz_answer = None
        self.pending_quiz_analysis = None
        
        return self.get_welcome_message()

    def check_daily_reset(self):
        """检查并执行每日重置"""
        today = datetime.now().date().isoformat()
        if self.last_update_date != today:
            self.energy = self.max_energy
            # 每日自动降低少量压力
            stress_cap = 100 + PERSONALITY_TYPES.get(self.personality, {}).get("stress_max_bonus", 0)
            self.stress = clamp(self.stress - 10, 0, stress_cap)
            self.last_update_date = today
            return True
        return False

    def get_welcome_message(self) -> str:
        total_score = sum(self.subjects.values())
        personality_info = PERSONALITY_TYPES[self.personality]
        
        msg = [
            "🎓 欢迎来到高考模拟学习 v2.0！",
            f"📚 你的学科类型: {self.subject_type}",
            f"💫 你的性格: {self.personality} ({personality_info['desc']})",
            f"❤️ 喜欢的科目: {self.favorite_subject} (+20%效果)",
            f"\n📊 初始总分: {total_score}分",
            f"⚡ 今日体力: {self.energy}/{self.max_energy}",
            f"😫 当前压力: {self.stress}/100",
            "\n💡 新功能提示：",
            "1. 每天自动恢复体力，学习消耗体力，压力过高会影响发挥",
            "2. 使用 '/高考休息' 可以恢复状态",
            "3. 学习过程中可能会触发 AI 老师的随堂测验哦！"
        ]
        return "\n".join(msg)

    def to_dict(self) -> Dict:
        return {
            'started': self.started,
            'current_month': self.current_month,
            'subject_type': self.subject_type,
            'subjects': self.subjects,
            'teachers': self.teachers,
            'favorite_subject': self.favorite_subject,
            'dislike_subject': self.dislike_subject,
            'initial_scores': self.initial_scores,
            'personality': self.personality,
            'history_high_score': self.history_high_score,
            'final_scores': self.final_scores,
            'is_debug_mode': self.is_debug_mode,
            'group_id': self.group_id,
            'stress': self.stress,
            'energy': self.energy,
            'max_energy': self.max_energy,
            'last_update_date': self.last_update_date,
            'month_progress': self.month_progress,
            'history_scores_record': self.history_scores_record,
            'pending_quiz_answer': self.pending_quiz_answer,
            'quiz_subject': self.quiz_subject,
            'pending_quiz_analysis': self.pending_quiz_analysis
        }

    @classmethod
    def from_dict(cls, user_id: str, data: Dict) -> 'GaokaoGame':
        game = cls(user_id)
        game.started = data.get('started', False)
        game.current_month = data.get('current_month', 0)
        game.subject_type = data.get('subject_type', '')
        game.subjects = data.get('subjects', {})
        game.teachers = data.get('teachers', {})
        game.favorite_subject = data.get('favorite_subject', '')
        game.dislike_subject = data.get('dislike_subject', '')
        game.initial_scores = data.get('initial_scores', {})
        game.personality = data.get('personality', '普通型')
        game.history_high_score = data.get('history_high_score', 0)
        game.final_scores = data.get('final_scores', {})
        game.is_debug_mode = data.get('is_debug_mode', False)
        game.group_id = data.get('group_id', '')
        game.stress = data.get('stress', 0)
        game.energy = data.get('energy', 5)
        game.max_energy = max(1, int(data.get('max_energy', 5)))
        game.last_update_date = data.get('last_update_date', datetime.now().date().isoformat())
        game.month_progress = data.get('month_progress', 0)
        game.history_scores_record = data.get('history_scores_record', [])
        game.pending_quiz_answer = data.get('pending_quiz_answer')
        game.quiz_subject = data.get('quiz_subject')
        game.pending_quiz_analysis = data.get('pending_quiz_analysis')
        if game.energy > game.max_energy:
            game.energy = game.max_energy
        stress_cap = 100 + PERSONALITY_TYPES.get(game.personality, {}).get("stress_max_bonus", 0)
        game.stress = clamp(game.stress, 0, stress_cap)
        return game

@register("astrbot_plugin_gaokao_sim", "jinyao", "高考模拟学习插件", "2.1.0", "https://github.com/wangyingxuan383-ai/astrbot_plugin_gaokao_sim")
class GaokaoPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config
        self.games: Dict[str, GaokaoGame] = {}
        self.logger = logger
        # 数据持久化路径
        plugin_name = getattr(self, "name", None) or "gaokao"
        self.plugin_data_dir = Path(get_astrbot_data_path()) / "plugin_data" / plugin_name
        self.plugin_data_dir.mkdir(parents=True, exist_ok=True)
        self.data_path = self.plugin_data_dir / "gaokao_data.json"
        self.report_dir = self.plugin_data_dir / "reports"
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.load_data()
        
    def save_data(self):
        """保存数据到文件"""
        data = {uid: game.to_dict() for uid, game in self.games.items()}
        try:
            self.plugin_data_dir.mkdir(parents=True, exist_ok=True)
            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"保存高考数据失败: {e}")

    def load_data(self):
        """从文件加载数据"""
        if not os.path.exists(self.data_path):
            return
        try:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for uid, game_data in data.items():
                    self.games[uid] = GaokaoGame.from_dict(uid, game_data)
            self.logger.info(f"已加载 {len(self.games)} 个用户的高考数据")
        except Exception as e:
            self.logger.error(f"加载高考数据失败: {e}")

    def get_user_game(self, user_id: str) -> GaokaoGame:
        if user_id not in self.games:
            self.games[user_id] = GaokaoGame(user_id)
        return self.games[user_id]

    def extract_json_payload(self, text: str) -> Optional[Dict]:
        if not text:
            return None
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.replace("```json", "").replace("```", "").strip()
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return None
        cleaned = cleaned[start:end + 1]
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return None

    def normalize_quiz_data(self, data: Dict, subject: str) -> Optional[Dict]:
        if not isinstance(data, dict):
            return None
        question = str(data.get("question", "")).strip()
        options = data.get("options", [])
        answer = str(data.get("answer", "")).strip().upper()
        analysis = str(data.get("analysis", "")).strip()

        if isinstance(options, str):
            options = [opt.strip() for opt in options.split("\n") if opt.strip()]
        if not isinstance(options, list):
            return None
        if len(options) < 4:
            return None
        options = options[:4]

        if answer and answer[0] in ["A", "B", "C", "D"]:
            answer = answer[0]
        if answer not in ["A", "B", "C", "D"]:
            fallback = FALLBACK_QUIZ_BANK.get(subject) or FALLBACK_QUIZ_BANK["通用"]
            answer = fallback["answer"]

        if not question:
            return None

        return {
            "question": question,
            "options": options,
            "answer": answer,
            "analysis": analysis
        }

    def advance_month_progress(self, game: GaokaoGame) -> Tuple[Optional[str], bool]:
        progress_cap = max(1, game.max_energy)
        game.month_progress += 1
        if game.month_progress < progress_cap:
            return None, False

        game.month_progress = 0
        game.history_scores_record.append(sum(game.subjects.values()))

        if game.current_month < len(MONTHS) - 1:
            game.current_month += 1
            return f"📅 时间流逝... 进入了 {MONTHS[game.current_month]}", False

        return "📅 你完成了最后阶段的备考，等待最终结算...", True

    async def maybe_generate_dynamic_event(self, event: AstrMessageEvent, subject: str, is_success: bool) -> Optional[str]:
        if not self.config.get("enable_llm_features", True):
            return None
        if random.random() >= DYNAMIC_EVENT_RATE:
            return None
        umo = getattr(event, "unified_msg_origin", None)
        if not umo:
            return None
        provider_id = await self.context.get_current_chat_provider_id(umo=umo)
        if not provider_id:
            return None
        outcome = "成功" if is_success else "失利"
        prompt = f"""
请输出严格 JSON：
{{
  "event": "一句话描述一次{subject}学习的{outcome}剧情，不超过20字"
}}
不要包含多余文本。
"""
        try:
            resp = await self.context.llm_generate(chat_provider_id=provider_id, prompt=prompt)
            data = self.extract_json_payload(resp.completion_text)
            if data and "event" in data:
                return str(data["event"]).strip()
        except Exception as exc:
            self.logger.error(f"生成动态剧情失败: {exc}")
        return None
        
    # --- 指令处理函数 ---
    
    @filter.command("高考学习开始")
    async def start_game(self, event: AstrMessageEvent):
        user_id = event.get_sender_id()
        game = self.get_user_game(user_id)
        
        if game.started:
            month_label = MONTHS[min(game.current_month, len(MONTHS) - 1)]
            yield event.plain_result(f"⚠️ 游戏正在进行中！\n当前进度: {month_label}\n使用 '/高考状态' 查看详情")
            return
        
        welcome_msg = game.initialize_game(event.get_group_id(), self.config)
        self.save_data()
        yield event.plain_result(welcome_msg)

    @filter.command("高考状态")
    async def check_status(self, event: AstrMessageEvent):
        user_id = event.get_sender_id()
        game = self.get_user_game(user_id)
        
        if not game.started:
            yield event.plain_result("❌ 游戏尚未开始！使用 '/高考学习开始' 开始游戏")
            return
            
        if game.check_daily_reset():
            self.save_data()
        
        total_score = sum(game.subjects.values())
        initial_total = sum(game.initial_scores.values())
        improvement = total_score - initial_total
        month_label = MONTHS[min(game.current_month, len(MONTHS) - 1)]
        p_info = PERSONALITY_TYPES.get(game.personality, {})
        stress_cap = 100 + p_info.get("stress_max_bonus", 0)
        
        msg = [
            f"📊 {game.subject_type}学习状态 - {month_label}",
            f"⏳ 月进度: {game.month_progress}/{max(1, game.max_energy)}",
            f"⚡ 体力: {game.energy}/{game.max_energy} | 😫 压力: {game.stress}/{stress_cap}",
            f"💫 性格: {game.personality}",
            f"\n📈 各科成绩:",
            *[f"  {sub}: {score}分 ({'+' if score>=game.initial_scores[sub] else ''}{score-game.initial_scores[sub]})" 
              for sub, score in game.subjects.items()],
            f"\n📋 总分: {total_score}分 (总提升 {improvement})"
        ]
        yield event.plain_result("\n".join(msg))

    @filter.command("高考菜单")
    async def show_menu(self, event: AstrMessageEvent):
        """显示菜单"""
        menu_msg = f"""
📚 高考模拟学习菜单

✅ 可用命令:
/高考学习开始 - 开始新游戏
/高考学习 [科目] - 学习指定科目
/高考休息 - 休息放松
/高考状态 - 查看状态
/高考回答 [选项] - 回答测验题
/高考菜单 - 显示此菜单

📌 核心规则:
- 时间线: 9月到次年6月，共10个月
- 月推进: 每累计行动达到当前体力上限推进一个月
- 体力: 每日自动恢复到上限
- 压力: 过高会影响学习成功率
- AI: 学习时可能触发随堂测验与动态剧情
        """
        yield event.plain_result(menu_msg.strip())

    @filter.command("高考休息")
    async def rest(self, event: AstrMessageEvent):
        user_id = event.get_sender_id()
        game = self.get_user_game(user_id)
        
        if not game.started:
            yield event.plain_result("❌ 请先开始游戏")
            return
            
        if game.check_daily_reset():
            self.save_data()
        
        if game.energy < 1:
            yield event.plain_result("💤 体力不足！明天再来吧")
            return
            
        game.energy -= 1
        stress_reduce = random.randint(15, 25)
        p_info = PERSONALITY_TYPES.get(game.personality, {})
        stress_cap = 100 + p_info.get("stress_max_bonus", 0)
        stress_reduce = int(stress_reduce * (1 + p_info.get("stress_recovery", 0)))
        game.stress = clamp(game.stress - stress_reduce, 0, stress_cap)
        
        activities = ["打了一下午篮球", "去网吧开黑", "在寝室睡大觉", "去操场散步", "看了一场电影"]
        activity = random.choice(activities)
        
        progress_msg, finished = self.advance_month_progress(game)

        msg_lines = [
            f"🧘‍♂️ 你{activity}，心情舒畅！",
            f"⚡ 体力-1 | 😌 压力-{stress_reduce} (当前: {game.stress})"
        ]
        if progress_msg:
            msg_lines.append(progress_msg)

        self.save_data()
        yield event.plain_result("\n".join(msg_lines))

        if finished:
            await self.finish_game(event, game)

    @filter.command("高考学习")
    async def study(self, event: AstrMessageEvent):
        user_id = event.get_sender_id()
        game = self.get_user_game(user_id)
        
        if not game.started:
            yield event.plain_result("❌ 请先开始游戏")
            return
            
        if game.check_daily_reset():
            self.save_data()
        
        if game.energy < 1:
            yield event.plain_result("💤 体力不足！请休息或明天再来")
            return
            
        # 参数解析
        msg = event.message_str.strip()
        parts = msg.split()
        if len(parts) < 2:
            yield event.plain_result(f"❌ 请指定科目！\n可用: {', '.join(game.subjects.keys())}")
            return
        subject = parts[1]
        
        if subject not in game.subjects:
            yield event.plain_result("❌ 科目不存在")
            return

        # 消耗及结算
        game.energy -= 1
        stress_inc = random.randint(5, 10)
        
        # 压力过高惩罚
        success_rate = 0.6
        if game.stress > 80:
            success_rate = 0.3
            yield event.plain_result("⚠️ 压力过高，你感到头晕眼花，学习效率极低！建议先休息！")
        elif game.stress > 60:
            success_rate = 0.45
            
        # 性格影响
        p_info = PERSONALITY_TYPES.get(game.personality, {})
        stress_cap = 100 + p_info.get("stress_max_bonus", 0)
        success_rate -= p_info.get("fail_chance", 0)
        success_rate = clamp(success_rate, 0.05, 0.95)
        stress_inc = int(stress_inc * (1 + p_info.get("stress_gain", 0) - p_info.get("stress_resist", 0)))
        stress_inc = max(1, stress_inc)
        
        is_success = random.random() < success_rate
        score_change = 0
        event_desc = ""
        
        if is_success:
            score_change = random.randint(5, 15)
            score_change = int(score_change * (1 + p_info.get("success_bonus", 0)))
            if subject == game.favorite_subject:
                score_change = int(score_change * 1.2)
            game.stress = clamp(game.stress + stress_inc, 0, stress_cap)
            event_desc = "学习不仅高效，还掌握了新知识点！"
        else:
            score_change = random.randint(-5, 2) # 有小概率增加一点点
            if "fail_penalty_reduce" in p_info:
                score_change = int(score_change * (1 - p_info.get("fail_penalty_reduce", 0)))
            game.stress = clamp(game.stress + stress_inc + 5, 0, stress_cap)
            event_desc = "走神了，看书看串行了..."

        dynamic_event = await self.maybe_generate_dynamic_event(event, subject, is_success)
        if dynamic_event:
            event_desc = dynamic_event
            
        # 更新分数
        old_score = game.subjects[subject]
        max_score = 150 if subject in ["语文", "数学", "英语"] else 100
        new_score = max(0, min(old_score + score_change, max_score))
        game.subjects[subject] = new_score
        
        # 是否触发AI测验
        trigger_quiz = False
        quiz_rate = float(self.config.get("quiz_trigger_rate", 0.3))
        quiz_rate = clamp(quiz_rate, 0.0, 1.0)
        if self.config.get("enable_llm_features", True) and random.random() < quiz_rate:
            trigger_quiz = True
        if game.pending_quiz_answer:
            trigger_quiz = False
            
        result_msg = [
            f"📚 学习科目: {subject}",
            f"🎯 结果: {'成功' if is_success else '一般'} ({'+' if new_score>=old_score else ''}{new_score-old_score})",
            f"📝 事件: {event_desc}",
            f"😫 压力 +{stress_inc} | ⚡ 体力 -1"
        ]
        
        progress_msg, finished = self.advance_month_progress(game)
        if progress_msg:
            result_msg.append(progress_msg)

        self.save_data()
        yield event.plain_result("\n".join(result_msg))

        if finished:
            await self.finish_game(event, game)
            return

        # 触发测验 (异步)
        if trigger_quiz and self.config.get("enable_llm_features", True):
            quiz_msg = await self.trigger_ai_quiz(event, game, subject)
            if quiz_msg:
                yield event.plain_result(quiz_msg)

    async def trigger_ai_quiz(self, event: AstrMessageEvent, game: GaokaoGame, subject: str) -> Optional[str]:
        """触发 AI 测验"""
        umo = getattr(event, "unified_msg_origin", None)
        if not umo:
            return None
        provider_id = await self.context.get_current_chat_provider_id(umo=umo)
        if not provider_id:
            return None

        prompt = f"""
请出一道高中{subject}科目的单项选择题。
严格输出 JSON，不要包含多余文本：
{{
  "question": "题目内容",
  "options": ["A. xxx", "B. xxx", "C. xxx", "D. xxx"],
  "answer": "A",
  "analysis": "解析..."
}}
"""
        try:
            resp = await self.context.llm_generate(chat_provider_id=provider_id, prompt=prompt)
            data = self.extract_json_payload(resp.completion_text)
            data = self.normalize_quiz_data(data, subject) if data else None
            if not data:
                data = FALLBACK_QUIZ_BANK.get(subject) or FALLBACK_QUIZ_BANK["通用"]

            game.pending_quiz_answer = data["answer"]
            game.quiz_subject = subject
            game.pending_quiz_analysis = data.get("analysis", "")
            self.save_data()

            msg = [
                f"👨‍🏫 {game.teachers.get(subject, '老师')} 突然把你叫起来回答问题！",
                f"❓ {data['question']}",
                "\n".join(data["options"]),
                "\n💡 请使用 '/高考回答 A/B/C/D' 作答！答对奖励分数！"
            ]
            return "\n".join(msg)
        except Exception as e:
            self.logger.error(f"生成测验失败: {e}")
        return None
            
    @filter.command("高考回答")
    async def answer_quiz(self, event: AstrMessageEvent):
        user_id = event.get_sender_id()
        game = self.get_user_game(user_id)
        
        if not game.pending_quiz_answer:
            yield event.plain_result("❓ 当前没有需要回答的问题")
            return
            
        msg = event.message_str.strip().split()
        if len(msg) < 2:
            yield event.plain_result("❌ 请输入答案，例如：/高考回答 A")
            return
            
        user_ans = msg[1].upper()
        correct_ans = game.pending_quiz_answer
        subject = game.quiz_subject or ""
        max_score = 150 if subject in ["语文", "数学", "英语"] else 100
        
        stress_cap = 100 + PERSONALITY_TYPES.get(game.personality, {}).get("stress_max_bonus", 0)

        if user_ans == correct_ans:
            bonus = 5
            if subject in game.subjects:
                game.subjects[subject] = clamp(game.subjects[subject] + bonus, 0, max_score)
            msg_lines = [f"✅ 回答正确！{subject}成绩 +{bonus} 分！"]
        else:
            game.stress = clamp(game.stress + 5, 0, stress_cap)
            msg_lines = [f"❌ 回答错误！正确答案是 {correct_ans}。压力 +5"]

        if game.pending_quiz_analysis:
            msg_lines.append(f"📌 解析: {game.pending_quiz_analysis}")
            
        game.pending_quiz_answer = None
        game.pending_quiz_analysis = None
        self.save_data()
        yield event.plain_result("\n".join(msg_lines))

    async def finish_game(self, event: AstrMessageEvent, game: GaokaoGame):
        """游戏结束结算"""
        total_score = sum(game.subjects.values())
        game.final_scores = game.subjects.copy()
        if total_score > game.history_high_score:
            game.history_high_score = total_score
        if not game.history_scores_record or game.history_scores_record[-1] != total_score:
            game.history_scores_record.append(total_score)
        
        # 1. 基础文字结算
        tier_info = None
        for (min_s, max_s), info in UNIVERSITY_TIERS.items():
            if min_s <= total_score <= max_s:
                tier_info = info
                break
        if not tier_info: tier_info = UNIVERSITY_TIERS[(0, 399)]
        
        initial_total = sum(game.initial_scores.values())
        improvement = total_score - initial_total

        summary = [
            "🎉 高考结束！成绩单已出炉！",
            f"🏆 总分: {total_score} (提升 {improvement})",
            f"🎓 录取档次: {tier_info['name']}",
            f"📝 评价: {tier_info['desc']}",
            f"📈 历史最高分: {game.history_high_score}"
        ]
        
        yield event.plain_result("\n".join(summary))
        
        # 2. 生成图片
        if HAS_VISUAL and self.config.get("enable_image_generation", True):
            try:
                img_path = await self.generate_report_card_image(event.get_sender_name(), total_score, tier_info['name'], game)
                if img_path:
                    yield event.image_result(img_path)

                chart_path = await self.generate_score_trend_chart(game, tier_info['name'])
                if chart_path:
                    yield event.image_result(chart_path)
            except Exception as e:
                self.logger.error(f"图片生成失败: {e}")
                
        # 3. LLM 志愿建议
        if self.config.get("enable_llm_features", True):
            umo = getattr(event, "unified_msg_origin", None)
            if not umo:
                provider_id = None
            else:
                provider_id = await self.context.get_current_chat_provider_id(umo=umo)
            if provider_id:
                scores_str = ", ".join([f"{k}:{v}" for k,v in game.subjects.items()])
                prompt = f"""
                考生高考总分{total_score}，科目成绩：{scores_str}。
                性格：{game.personality}。
                如果不理想，请给予安慰。
                如果成绩不错，请根据其优势科目推荐2个适合的专业方向，并给出简短的职业规划建议。
                200字以内。
                """
                yield event.plain_result("🤖 正在咨询 AI 志愿填报顾问...")
                resp = await self.context.llm_generate(chat_provider_id=provider_id, prompt=prompt)
                yield event.plain_result(f"💡 志愿顾问建议：\n{resp.completion_text}")

        # 重置游戏状态
        game.started = False
        game.month_progress = 0
        game.pending_quiz_answer = None
        game.pending_quiz_analysis = None
        self.save_data()

    async def generate_report_card_image(self, name: str, score: int, university: str, game: GaokaoGame) -> str:
        """生成成绩单图片"""
        width, height = 900, 1100
        image = Image.new("RGB", (width, height), THEME["bg"])
        draw = ImageDraw.Draw(image)

        font_candidates = [
            "C:\\Windows\\Fonts\\simhei.ttf",
            "C:\\Windows\\Fonts\\msyh.ttc",
            "C:\\Windows\\Fonts\\simsun.ttc"
        ]
        font_path = next((p for p in font_candidates if os.path.exists(p)), None)

        try:
            title_font = ImageFont.truetype(font_path, 56) if font_path else ImageFont.load_default()
            text_font = ImageFont.truetype(font_path, 32) if font_path else ImageFont.load_default()
            score_font = ImageFont.truetype(font_path, 88) if font_path else ImageFont.load_default()
            small_font = ImageFont.truetype(font_path, 24) if font_path else ImageFont.load_default()
        except Exception:
            title_font = ImageFont.load_default()
            text_font = ImageFont.load_default()
            score_font = ImageFont.load_default()
            small_font = ImageFont.load_default()

        def draw_centered(text: str, y: int, font, fill):
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            draw.text(((width - text_width) / 2, y), text, font=font, fill=fill)

        # 边框
        draw.rectangle([40, 40, width - 40, height - 40], outline=THEME["border"], width=3)

        # 标题与徽章
        draw_centered("高考录取通知书", 90, title_font, THEME["primary"])
        badge_box = [width - 180, 80, width - 80, 180]
        draw.ellipse(badge_box, outline=THEME["primary"], width=4)
        draw.text((width - 165, 115), "录取", font=small_font, fill=THEME["primary"])

        # 信息卡片
        card_box = [80, 220, width - 80, 480]
        draw.rectangle(card_box, outline=THEME["border"], width=2, fill=(246, 251, 243))
        draw.text((110, 250), f"考生姓名: {name}", font=text_font, fill=THEME["text"])
        draw.text((110, 300), f"学科类型: {game.subject_type}", font=text_font, fill=THEME["text"])
        draw.text((110, 350), f"性格类型: {game.personality}", font=text_font, fill=THEME["text"])
        draw.text((110, 410), f"录取院校: {university}", font=text_font, fill=THEME["text"])

        # 总分
        draw_centered("总分", 520, text_font, THEME["text"])
        draw_centered(str(score), 570, score_font, THEME["primary"])

        # 各科成绩
        start_y = 720
        start_x = 120
        col_gap = 260
        row_gap = 70
        for i, (sub, s) in enumerate(game.subjects.items()):
            x = start_x + (i % 3) * col_gap
            y = start_y + (i // 3) * row_gap
            draw.text((x, y), f"{sub}: {s}", font=text_font, fill=THEME["text"])

        # 底部
        issue_date = datetime.now().strftime("%Y-%m-%d")
        draw.text((80, height - 120), f"签发日期: {issue_date}", font=small_font, fill=THEME["text"])
        draw.text((80, height - 80), "高考模拟系统", font=small_font, fill=THEME["text"])

        filename = f"{game.user_id}_{int(datetime.now().timestamp())}_report.png"
        filepath = self.report_dir / filename
        image.save(filepath)
        return str(filepath)

    async def generate_score_trend_chart(self, game: GaokaoGame, tier_name: str) -> Optional[str]:
        """生成成绩趋势折线图"""
        if not game.history_scores_record:
            return None

        scores = game.history_scores_record[:]
        labels = ["初始"] + MONTHS
        if len(scores) > len(labels):
            scores = scores[:len(labels)]
        else:
            labels = labels[:len(scores)]

        plt.rcParams["font.sans-serif"] = ["SimHei"]
        plt.rcParams["axes.unicode_minus"] = False

        fig, ax = plt.subplots(figsize=(8, 4.5), dpi=150)
        fig.patch.set_facecolor("#EEF5E8")
        ax.set_facecolor("#EEF5E8")

        ax.plot(labels, scores, color="#2D6A4F", linewidth=2.5, marker="o")
        ax.grid(True, color="#D7E3D1", linewidth=0.8, linestyle="--", alpha=0.8)

        ax.set_title("成绩趋势", color="#2D6A4F", fontsize=14, pad=12)
        ax.set_xlabel("月份", color="#2F2F2F")
        ax.set_ylabel("总分", color="#2F2F2F")
        ax.tick_params(axis="x", rotation=0, colors="#2F2F2F")
        ax.tick_params(axis="y", colors="#2F2F2F")

        last_score = scores[-1]
        ax.annotate(f"{last_score}", xy=(len(scores) - 1, last_score),
                    xytext=(0, 8), textcoords="offset points",
                    ha="center", color="#2D6A4F", fontsize=10)
        fig.text(0.5, 0.02, f"最终录取档次: {tier_name}", ha="center", color="#2F2F2F", fontsize=10)

        filename = f"{game.user_id}_{int(datetime.now().timestamp())}_trend.png"
        filepath = self.report_dir / filename
        fig.savefig(filepath, bbox_inches="tight")
        plt.close(fig)
        return str(filepath)
