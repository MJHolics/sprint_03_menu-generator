import streamlit as st
import json
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="메뉴판 생성 API 테스트", layout="wide")

st.title("메뉴판 생성 시스템 - API 테스트 페이지")

# 사이드바 설정
st.sidebar.header("테마 설정")

theme_style = st.sidebar.selectbox(
    "스타일",
    ["modern", "classic", "elegant", "casual"]
)

color_scheme = st.sidebar.selectbox(
    "색상 구성",
    ["warm", "cool", "vibrant"]
)

language = st.sidebar.selectbox(
    "언어",
    ["ko", "en", "bilingual"]
)

layout_preference = st.sidebar.selectbox(
    "레이아웃",
    ["grid", "list", "card"]
)

# 메인 영역
st.header("1. 메뉴 아이템 입력")

# 메뉴 개수 선택
num_items = st.number_input("메뉴 개수", min_value=1, max_value=10, value=2)

menu_items = []

for i in range(num_items):
    st.subheader(f"메뉴 {i+1}")

    col1, col2 = st.columns([1, 2])

    with col1:
        uploaded_file = st.file_uploader(
            f"이미지 업로드 {i+1}",
            type=["jpg", "jpeg", "png"],
            key=f"image_{i}"
        )

        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption=f"메뉴 {i+1} 이미지", use_container_width=True)

            # base64 인코딩
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
        else:
            img_str = None

    with col2:
        category = st.selectbox(
            "카테고리",
            ["Soup", "Salad", "Spicy", "Dessert", "Main", "Appetizer"],
            key=f"category_{i}"
        )

        name_ko = st.text_input("한글 이름", key=f"name_ko_{i}", placeholder="예: 속초 원터 아목장골")
        name_en = st.text_input("영문 이름", key=f"name_en_{i}", placeholder="예: Dried pollack korean-style soup")
        description = st.text_area("설명", key=f"desc_{i}", placeholder="메뉴에 대한 설명을 입력하세요")

        highlights_input = st.text_input("강조 키워드 (쉼표로 구분)", key=f"highlights_{i}", placeholder="예: 매콤한, 건강한, 인기메뉴")
        highlights = [h.strip() for h in highlights_input.split(",")] if highlights_input else []

        price = st.number_input("가격 (선택)", min_value=0, value=0, step=1000, key=f"price_{i}")

    # 메뉴 아이템 데이터 구성
    if name_ko or name_en:
        menu_item = {
            "image": img_str if img_str else "no_image",
            "category": category,
            "name_ko": name_ko,
            "name_en": name_en,
            "description": description,
            "highlights": highlights,
            "price": price if price > 0 else None
        }
        menu_items.append(menu_item)

    st.divider()

# API 요청 데이터 구성
st.header("2. API 요청 데이터 (Request)")

request_data = {
    "theme": {
        "style": theme_style,
        "color_scheme": color_scheme,
        "language": language
    },
    "menu_items": menu_items,
    "layout_preference": layout_preference,
    "timestamp": datetime.now().isoformat()
}

# 이미지 데이터는 미리보기에서 제외 (너무 길어서)
preview_data = request_data.copy()
for item in preview_data["menu_items"]:
    if item["image"] != "no_image":
        item["image"] = f"<base64_encoded_image_{len(item['image'])}bytes>"

st.json(preview_data)

# 다운로드 버튼
json_str = json.dumps(request_data, ensure_ascii=False, indent=2)
st.download_button(
    label="Request JSON 다운로드",
    data=json_str,
    file_name=f"menu_request_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
    mime="application/json"
)

st.divider()

# API 응답 시뮬레이션
st.header("3. API 응답 (Response) - 시뮬레이션")

if st.button("API 호출 시뮬레이션", type="primary"):
    with st.spinner("메뉴판 생성 중..."):
        import time
        time.sleep(1)

        response_data = {
            "menu_pdf_url": "https://example.com/menu_20250110_123456.pdf",
            "menu_html": "<html><body><h1>Generated Menu</h1></body></html>",
            "preview_image": "base64_encoded_preview_image",
            "status": "success",
            "processing_time": 2.3,
            "items_processed": len(menu_items),
            "timestamp": datetime.now().isoformat()
        }

        st.success("메뉴판 생성 완료")
        st.json(response_data)

st.divider()

# 통계 정보
st.header("4. 입력 데이터 통계")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("전체 메뉴 수", len(menu_items))

with col2:
    images_count = sum(1 for item in menu_items if item.get("image") != "no_image")
    st.metric("이미지 업로드", images_count)

with col3:
    categories = set(item["category"] for item in menu_items if item.get("category"))
    st.metric("카테고리 수", len(categories))

with col4:
    with_price = sum(1 for item in menu_items if item.get("price"))
    st.metric("가격 입력", with_price)

# 카테고리별 그룹핑 미리보기
if menu_items:
    st.header("5. 카테고리별 그룹핑 미리보기")

    from collections import defaultdict
    grouped = defaultdict(list)

    for item in menu_items:
        grouped[item["category"]].append(item)

    for category, items in grouped.items():
        with st.expander(f"{category} ({len(items)}개)", expanded=True):
            for item in items:
                col1, col2 = st.columns([1, 3])
                with col1:
                    if item["image"] != "no_image":
                        st.write("이미지 있음")
                    else:
                        st.write("이미지 없음")
                with col2:
                    st.write(f"**{item['name_ko']}** / {item['name_en']}")
                    st.write(f"_{item['description']}_")
                    if item["highlights"]:
                        st.write(f"키워드: {', '.join(item['highlights'])}")
                st.divider()

# Footer
st.divider()
st.caption("메뉴판 생성 API 테스트 페이지 v1.0")
