from PIL import Image, ImageDraw, ImageFont
import textwrap

# 기존 메뉴판 템플릿 불러오기
img = Image.open("template_menu.png").convert("RGBA")
draw = ImageDraw.Draw(img)
font_title = ImageFont.truetype("assets/fonts/NotoSansCJK-Regular.ttc", size=40)
font_item = ImageFont.truetype("assets/fonts/NotoSansCJK-Regular.ttc", size=28)

# 좌표 매핑 (예시)
positions = {
    "Soup": [(100, 200), (100, 300), (100, 400)],
    "Spicy": [(400, 200), (400, 300)],
    "Salad": [(700, 200), (700, 300)]
}

# 새로운 메뉴 데이터
menus = {
    "Soup": [
        {"name": "된장찌개", "price": 9000, "description": "조상 대대로 내려온 된장을 이용한 깊은 맛의 찌개"},
        {"name": "계란말이", "price": 5000, "description": "장인이 선별한 계란으로 만든 부드러운 계란말이"},
        {"name": "소고기국밥", "price": 10000, "description": "소고기가 듬뿍 들어간 따뜻한 국밥"}
    ],
    "Spicy": [
        {"name": "닭도리탕", "price": 15000, "description": "매콤한 양념에 푹 졸인 닭도리탕"},
        {"name": "곱창전골", "price": 15000, "description": "곱창과 채소가 어우러진 얼큰한 전골"}
    ]
}

# 텍스트 덮어쓰기
for category, items in menus.items():
    for (item, pos) in zip(items, positions[category]):
        x, y = pos
        # 메뉴명 + 가격
        draw.text((x, y), f"{item['name']}  {item['price']}원", font=font_item, fill="black")
        y += 35
        # 설명 줄바꿈 처리
        for line in textwrap.wrap(item['description'], width=25):
            draw.text((x, y), line, font=font_item, fill="gray")
            y += 30

img.save("outputs-3/updated_menu.png")
print("✅ 메뉴판 업데이트 완료: outputs-3/updated_menu.png")
