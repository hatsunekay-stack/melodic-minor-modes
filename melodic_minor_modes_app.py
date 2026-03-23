import streamlit as st

# ノート変換テーブル
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

semi_note = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']


def note_to_semi(note):
    n = note.strip().replace('♭', 'b').replace('♯', '#')

    if '/' in n:
        parts = [p.strip() for p in n.split('/')]
        flat_candidate = None
        for p in parts:
            if 'b' in p:
                flat_candidate = p
                break
        n = flat_candidate if flat_candidate else parts[0]

    n = n.upper()
    return note_semi.get(n)


def semi_to_note(s):
    return semi_note[s % 12]


# モード定義
modes = [
    {"degree": 1, "name": "メロディックマイナー"},
    {"degree": 2, "name": "ドリアン b2"},
    {"degree": 3, "name": "リディアン オーギュメント"},
    {"degree": 4, "name": "リディアン b7（リディアン ドミナント）"},
    {"degree": 5, "name": "ミクソリディアン b6"},
    {"degree": 6, "name": "ロクリアン #2"},
    {"degree": 7, "name": "オルタード"}
]

# メロディックマイナーのインターバル
mm_intervals = [0, 2, 3, 5, 7, 9, 11]

# ドロップダウンには日本語名だけ
mode_options = [m["name"] for m in modes]

st.title("メロディックマイナー モード対応表")
st.markdown("ルート音とモードを選ぶと、同じ親スケール内の全7モードが表示されます。")

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
    degree = None
    for m in modes:
        if selected_mode == m["name"]:
            degree = m["degree"]
            break

    if degree is None:
        st.error("モードが認識できませんでした。")
    else:
        root_s = note_to_semi(root_input)

        if root_s is None:
            st.error("ルート音が無効です。")
        else:
            offset = mm_intervals[degree - 1]
            parent_s = (root_s - offset) % 12
            parent_note = semi_to_note(parent_s)

            st.success(f"親スケール：**{parent_note} メロディックマイナー**")

            parent_notes = [semi_to_note(parent_s + i) for i in mm_intervals]

            st.markdown("### 全7モード対応表")

            for d in range(1, 8):
                mode_info = modes[d - 1]
                mode_root_s = (parent_s + mm_intervals[d - 1]) % 12
                mode_root = semi_to_note(mode_root_s)

                start_idx = parent_notes.index(mode_root)
                mode_notes = parent_notes[start_idx:] + parent_notes[:start_idx]
                notes_str = " - ".join(mode_notes)

                st.markdown(f"**{d}番目の音から開始**：{mode_root} {mode_info['name']}")
                st.code(f"({notes_str})", language=None)

st.sidebar.markdown("### アプリについて詳しく知る")
st.sidebar.markdown(
    "[GitHub READMEを見る 📖](https://github.com/hatsunekay-stack/melodic-minor-modes/blob/main/README.md)"
)
