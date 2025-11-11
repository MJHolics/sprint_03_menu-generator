import torch
from diffusers import AutoPipelineForText2Image
from PIL import Image, ImageDraw, ImageFont
import textwrap

# 1. SDXL-Turbo로 배경 + 패널 생성
def generate_background_with_panel(prompt, output_path="outputs/base.png"):
    pipe = AutoPipelineForText2Image.from_pretrained(
        "stabilityai/sdxl-turbo",
        torch_dtype=torch.float16,
        variant="fp16"
    ).to("cuda")

    image = pipe(
        prompt=prompt,
        num_inference_steps=6,
        guidance_scale=0.0,
        height=512,
        width=512
    ).images[0]

    image.save(output_path)
    print(f"✅ 배경+패널 생성 완료: {output_path}")
    return output_path

# 2. 메뉴 텍스트 오버레이
def overlay_menus(image_path, menus, font_path="assets/fonts/NotoSansCJK-Regular.ttc"):
    img = Image.open(image_path).convert("RGBA")
    draw = ImageDraw.Draw(img)
    W, H = img.size

    font_title = ImageFont.truetype(font_path, size=int(W*0.05))
    font_item = ImageFont.truetype(font_path, size=int(W*0.03))

    # 타이틀
    draw.text((int(W*0.05), int(H*0.05)), "메뉴판", font=font_title, fill="black")

    # 메뉴 반복 출력
    y = int(H*0.15)
    for item in menus:
        draw.text((int(W*0.05), y), f"{item['name']}  {item['price']}원", font=font_item, fill="black")
        y += int(W*0.05)

        for line in textwrap.wrap(item['description'], width=30):
            draw.text((int(W*0.05), y), line, font=font_item, fill="gray")
            y += int(W*0.04)

        y += int(W*0.03)

    img.convert("RGB").save("outputs/final_menu.png")
    print("✅ 최종 메뉴판 저장 완료: outputs/final_menu.png")

# 3. 실행
if __name__ == "__main__":
    menus = [
        {'name': '된장찌개', 'price': 9000, 'description': '된장찌개는 예로부터 조상 대대로 내려온 된장을 이용하여 만든 찌개'},
        {'name': '계란말이', 'price': 5000, 'description': '장인이 한땀 한땀 고른 계란을 선별하여 만든 계란을 이용한 말이'},
        {'name': '소고기국밥', 'price': 10000, 'description': '소고기가 듬뿍 들어있어 남녀노소 누구나 좋아하는 소고기 국밥'},
    ]

    # Step 1: 배경+패널 생성
    bg_path = generate_background_with_panel(
        "bright Korean restaurant interior with a clean rectangular panel at the bottom for menu text"
    )

    # Step 2: 메뉴 텍스트 오버레이
    overlay_menus(bg_path, menus)
