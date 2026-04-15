#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
from pathlib import Path
from typing import Dict, Any, Set, List

# 直接把你貼的 LABEL_PROMPTS 貼進來
LABEL_PROMPTS = {
    "booleans": {
        "心理問題": "你最近是否感到焦慮、沮喪或壓力大？",
        "RTW": "你是否正在考慮重返工作或擔心職場復歸？",
        "經濟與社會資源": "你是否想了解經濟補助或社會支持資源？",
        "危險字詞": "你現在是否出現緊急或危險症狀（例如出血、呼吸困難）？",
        "癌症復發": "你是否擔心病情復發或有相關疑慮？",
        "營養照護": "你是否吃東西困難、體重下降或擔心營養攝取不足？",
        "傷口與症狀照護": "你想獲得關於傷口或症狀照護的建議嗎？",
        "治療原因與安排": "你想更清楚治療的原因或安排流程嗎？",
        "口腔復健與身體活動": "你想了解復健或恢復身體活動的方法嗎？"
    },
    "focusp": {
        "F": "你希望家人能更參與或提供更多支持嗎？",
        "O": "你想保持或建立更正向的態度嗎？",
        "C": "你想加強面對疾病的因應能力嗎？",
        "U": "你想減少對病情或治療的不確定感嗎？",
        "S": "你想更好地管理身體症狀嗎？",
        "P": "你希望提升身體功能或活動力嗎？"
    },
    "treatment_phase": {
        "手術前": "目前是手術前的準備階段嗎？",
        "手術後": "目前是在手術後的恢復階段嗎？",
        "手術後化放療": "目前正在接受化學或放射治療嗎？",
        "存活期": "目前已完成主要治療、進入追蹤或存活期嗎？"
    },
    "functional_impact": {
        "咀嚼困難": "你吃東西時是否覺得咀嚼困難？",
        "吞嚥困難": "你吞嚥時是否感到困難或容易嗆到？",
        "發音說話困難": "你在說話或發音時有困難嗎？",
        "張口困難流口水": "你是否張嘴困難或容易流口水？",
        "皮膚紅腫口腔黏膜破損嚴重": "你是否有口腔黏膜紅腫、破損或潰瘍？",
        "口乾嚴重": "你是否覺得口乾嚴重、影響吃東西或說話？",
        "面部外觀改變": "你是否覺得外觀的改變讓你困擾？",
        "體重減輕營養不良": "你是否最近體重明顯下降或營養不良？",
        "鼻塞、耳鳴影響": "你是否有鼻塞或耳鳴影響生活？",
        "身體活動限制": "你是否覺得身體活動受到限制？",
        "睡眠問題": "你是否有睡眠困難或失眠的情況？",
        "聽力影響": "你是否發現聽力變差或影響溝通？",
        "疲倦": "你是否經常感到疲倦或容易累？",
        "體力下降": "你是否覺得體力明顯下降？"
    },
    "other_condition": {
        "其他狀況": "你是否還有其他健康狀況想補充？",
        "其他情況": "是否有其他想要讓我們了解的情況？"
    },
    "other_condition_text": {
        "詢問治療成功率": "你想了解治療的成功率或預後嗎？",
        "治療後生活安排問題": "你想知道治療後生活該如何安排嗎？",
        "生活習慣/方式調整問題": "你想了解生活方式應該如何調整嗎？",
        "口腔癌遺傳問題": "你想了解口腔癌是否與遺傳有關嗎？",
        "與小孩溝通問題": "你想知道如何與孩子溝通這件事嗎？",
        "家屬支持與溝通問題": "你希望獲得更多家屬支持或溝通建議嗎？",
        "為什麼會得口腔癌之提問": "你想了解為什麼會罹患口腔癌嗎？",
        "罹癌原因詢問": "你想了解造成口腔癌的可能原因嗎？",
        "與醫療團隊溝通問題": "你需要和醫療團隊更有效溝通的建議嗎？",
        "罹癌後生育問題": "你是否關心治療對生育的影響？",
        "治療後生活習慣調整問題": "你想知道治療後應如何調整生活習慣嗎？",
        "術後生活適應問題": "你想改善術後的生活適應嗎？",
        "家屬溝通問題": "你希望改善與家屬的溝通嗎？",
        "早期康復建議問題": "你想了解有哪些早期康復的方法嗎？",
        "詢問治療對生活的影響": "你想知道治療可能如何影響日常生活嗎？",
        "治療期間可否打疫苗詢問": "你想知道治療期間是否可以接種疫苗嗎？",
        "與家人溝通相關問題": "你想與家人討論罹癌相關話題嗎？",
        "家屬照顧問題": "你想了解家屬照顧的方式或負擔嗎？",
        "與家屬溝通相關問題": "你想獲得與家屬更好溝通的方法嗎？",
        "心理層次與角色功能相關問題": "你想討論心理壓力或社會角色的變化嗎？",
        "生活習慣詢問": "你想了解哪些生活習慣需要調整嗎？",
        "口腔癌型態詢問": "你想了解腫瘤的型態或分期嗎？",
        "口腔癌遺傳或是傳染問題": "你想知道口腔癌是否會遺傳或傳染嗎？",
        "罹癌後生活方式調整問題": "你想了解罹癌後生活方式該如何改變嗎？",
        "病情了解提問": "你想更清楚自己的病情與階段嗎？",
        "口腔癌分期治療詢問": "你想知道目前的分期對應的治療嗎？",
        "生活習慣調整詢問": "你想調整生活習慣來幫助恢復嗎？",
        "罹癌後生育計畫問題": "你是否正在考慮生育計畫？",
        "止痛藥使用成癮問題": "你是否擔心止痛藥使用過多或成癮？",
        "罹癌後本身慢性病照護方式提問": "你想了解罹癌後如何照顧慢性病嗎？",
        "與小孩溝通罹癌問題": "你想知道如何跟孩子談論罹癌的事嗎？",
        "口腔癌分期詢問": "你想知道目前口腔癌的分期嗎？",
        "治療成功率詢問": "你想知道治療的成功率與預後嗎？",
        "罹癌後生育計畫詢問": "你想在治療後規劃生育嗎？",
        "改善治療後身體狀況相關問題": "你想改善治療後的身體狀況嗎？",
        "詢問口腔癌是否會傳染": "你擔心口腔癌是否具有傳染性嗎？",
        "放射線治療照護詢問": "你想了解放療期間的照護要點嗎？",
        "術後生活影響問題詢問": "你想知道術後生活可能受到哪些影響嗎？",
        "口腔癌傳染問題": "你想確認口腔癌是否會傳染嗎？",
        "治療後照護事項詢問": "你想知道治療後的自我照護要點嗎？",
        "止痛藥副作用問題": "你是否擔心止痛藥會有副作用？",
        "治療後生活調整問題": "你想了解治療後生活該如何調整嗎？",
        "治療資料詢問": "你需要整理治療或病歷相關資料嗎？",
        "治療對生活的影響相關問題": "你想了解治療對生活品質的影響嗎？",
        "擔心止痛藥的副作用問題": "你是否擔心止痛藥帶來副作用？"
    }
}

BOOL_FIELDS = list(LABEL_PROMPTS["booleans"].keys())

def collect_labels_from_dataset(raw_dir: Path) -> Dict[str, Set[str]]:
    """
    掃 raw_data/*.json，蒐集：
    - booleans: 出現過的 bool 欄位名（欄位存在即可）
    - focusp: 出現過的 focusp code
    - treatment_phase: 出現過的 phase 值
    - functional_impact: 出現過的 FI 值
    """
    seen = {
        "booleans": set(),
        "focusp": set(),
        "treatment_phase": set(),
        "functional_impact": set(),
    }

    for p in raw_dir.glob("*.json"):
        obj = json.loads(p.read_text(encoding="utf-8"))

        # booleans: 欄位存在就算（不要求一定 True）
        for k in BOOL_FIELDS:
            if k in obj:
                seen["booleans"].add(k)

        # focusp
        fp = obj.get("focusp")
        if isinstance(fp, list):
            for v in fp:
                if v: seen["focusp"].add(str(v))

        # treatment_phase: string or list
        tp = obj.get("treatment_phase")
        if isinstance(tp, list):
            for v in tp:
                if v: seen["treatment_phase"].add(str(v))
        elif tp:
            seen["treatment_phase"].add(str(tp))

        # functional_impact: list
        fi = obj.get("functional_impact")
        if isinstance(fi, list):
            for v in fi:
                if v: seen["functional_impact"].add(str(v))

    return seen

def main():
    ap = argparse.ArgumentParser(description="Export clarification prompts to JSON and check coverage against dataset.")
    ap.add_argument("--dataset-root", required=True, help="例如 ./release_data")
    ap.add_argument("--raw-dir", default="raw_data")
    ap.add_argument("--out-path", default="schema/clarification_prompts.json")
    ap.add_argument("--check", action="store_true", help="掃 raw_data 檢查 prompts 覆蓋率")
    args = ap.parse_args()

    root = Path(args.dataset_root).resolve()
    raw_dir = (root / args.raw_dir).resolve()
    out_path = (root / args.out_path).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    out_path.write_text(json.dumps(LABEL_PROMPTS, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] wrote: {out_path}")

    if args.check:
        if not raw_dir.exists():
            raise SystemExit(f"[ERROR] raw_dir not found: {raw_dir}")

        seen = collect_labels_from_dataset(raw_dir)

        # coverage check: dataset labels should be covered by prompts
        def missing(dataset_set: Set[str], prompt_dict: Dict[str, Any]) -> List[str]:
            ps = set(prompt_dict.keys())
            return sorted([x for x in dataset_set if x not in ps])

        miss_focusp = missing(seen["focusp"], LABEL_PROMPTS["focusp"])
        miss_phase  = missing(seen["treatment_phase"], LABEL_PROMPTS["treatment_phase"])
        miss_fi     = missing(seen["functional_impact"], LABEL_PROMPTS["functional_impact"])

        print("[CHECK] coverage vs dataset:")
        print("  - focusp:        seen", len(seen["focusp"]), "missing", len(miss_focusp))
        print("  - treatment_phase: seen", len(seen["treatment_phase"]), "missing", len(miss_phase))
        print("  - functional_impact: seen", len(seen["functional_impact"]), "missing", len(miss_fi))

        if miss_focusp:
            print("    missing focusp:", miss_focusp)
        if miss_phase:
            print("    missing phases:", miss_phase)
        if miss_fi:
            print("    missing FI:", miss_fi)

        # booleans: 欄位名檢查（dataset 出現過的 bool 欄位是否在 prompt dict）
        miss_bool = sorted([x for x in seen["booleans"] if x not in LABEL_PROMPTS["booleans"]])
        print("  - booleans:      seen", len(seen["booleans"]), "missing", len(miss_bool))
        if miss_bool:
            print("    missing booleans:", miss_bool)

if __name__ == "__main__":
    main()