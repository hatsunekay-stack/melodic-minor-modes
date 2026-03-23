import streamlit as st

# ========== ノート変換テーブル ==========
# 内部では半音番号で処理し、表示はフラット系に統一
note_semi = {
    'C': 0,
    'C#': 1, 'DB': 1,
    'D': 2,
    'D#': 3, 'EB': 3,
    'E': 4,
    'F': 5,
    'F#': 6, 'GB': 6,
    'G': 7,
    'G#': 8, 'AB': 8,
    'A': 9,
    'A#': 10, 'BB': 10,
    'B': 11
}

# 表示はフラット系で固定
semi_note_flat = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']


def normalize_note_name(note: str) -> str:
    """
    入力された音名を正規化する。
    例:
    - 'Db' -> 'DB'
    - 'C#' -> 'C#'
    - 'C#/Db' -> 'DB'  （半音表示はフラットに統一）
    - '♭', '♯' にも対応
    """
    if not note:
        return ""

    n = note.strip().replace('♭', 'b').replace('♯', '#')

    # C#/Db のような表示が来たら、右側のフラット表記を優先
    if '/' in n:
        parts = [p.strip() for p in n.split('/')]
        flat_candidate = None
        for p in parts:
            if 'b' in p:
                flat_candidate = p
                break
        n = flat_candidate if flat_candidate else parts[0]

    # 1文字目は大文字、それ以降はそのまま整形して最後に大文字化
    n = n.upper()
    return n


def note_to_semi(note: str):
    normalized = normalize_note_name(note)
    return note_semi.get(normalized)


def semi_to_note_flat(semi: int) -> str:
    return semi_note_flat[semi % 12]


# ========== モード定義 ==========
modes = [
    {"degree": 1, "name": "メロディックマイナー", "alias": ["Melodic Minor"]},
    {"degree": 2, "name": "ドリアン b2", "alias": ["Dorian b2", "Dorian ♭2", "Dorian b9"]},
    {"degree": 3, "name": "リディアン オーギュメント", "alias": ["Lydian Augmented", "Lydian #5"]},
    {"degree": 4, "name": "リディアン b7 (リディアンドミナント)", "alias": ["Lydian b7", "Lydian Dominant"]},
    {"degree": 5, "name": "ミクソリディアン b6 (b13)", "alias": ["Mixolydian b6", "Mixolydian b13"]},
    {"degree": 6, "name": "ロクリアン #2 (ナチュラル2)", "alias": ["Locrian #2", "Locrian Natural 2"]},
    {"degree": 7, "name": "オルタード (スーパーロクリアン)", "alias": ["Altered", "Super Locrian"]}
]

# メロディックマイナーのインターバル（0始まり）
mm_intervals = [0, 2, 3, 5, 7, 9, 11]

# モード選択肢
mode_options = []
for m in modes:
    mode_options.append(m["name"])
    mode_options.extend(m["alias"])

# 重複除去
mode_options = list(dict.fromkeys(mode_options))


# ========== UI ==========
st.title("メロディックマイナー モード対応表")
st.markdown("ルート音とモードを選ぶと、同じ親スケール内の全7モードが表示されます。")
st.markdown("※ 半音ルートは **フラット表記（Db, Eb, Gb, Ab, Bb）** に統一しています。")

col1, col2 = st.columns(2)

with col1:
    root_input = st.selectbox(
        "ルート音",
        options=["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"],
        index=0
    )

with col2:
    selected_mode = st.selectbox(
        "現在のモード",
        options=mode_options
    )

if st.button("対応表を表示する", type="primary"):
    # 選択されたモードの degree を取得
    degree = None
    for m in modes:
        if selected_mode == m["name"] or selected_mode in m["alias"]:
            degree = m["degree"]
            break

    if degree is None:
        st.error("モードが認識できませんでした。もう一度選んでください。")
    else:
        root_s = note_to_semi(root_input)

        if root_s is None:
            st.error("ルート音が無効です。")
        else:
            # 親スケールのルートを計算
            offset = mm_intervals[degree - 1]
            parent_s = (root_s - offset) % 12
            parent_note = semi_to_note_flat(parent_s)

            st.success(f"親スケール：**{parent_note} メロディックマイナー**")

            # 親スケールの7音
            parent_notes = [semi_to_note_flat(parent_s + interval) for interval in mm_intervals]

            st.markdown("### 全7モード対応表")

            for d in range(1, 8):
                mode_info = modes[d - 1]
                mode_root_s = (parent_s + mm_intervals[d - 1]) % 12
                mode_root = semi_to_note_flat(mode_root_s)

                # モード音列を回転
                start_idx = parent_notes.index(mode_root)
                mode_notes = parent_notes[start_idx:] + parent_notes[:start_idx]
                notes_str = " - ".join(mode_notes)

                st.markdown(f"**{d}番目の音から開始**：{mode_root} {mode_info['name']}")
                st.code(f"({notes_str})", language=None)

            st.markdown("---")
            st.caption("同じ親スケールから7つのモードを確認できます。Jazz / Fusion の整理にも便利です。")