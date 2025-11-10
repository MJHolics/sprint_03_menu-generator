import torch
from diffusers import AutoPipelineForText2Image, StableDiffusionUpscalePipeline
from PIL import Image, ImageDraw, ImageFont
from translator import translate

# 1. SDXL-Turbo로 베이스 이미지 생성
def run_sdxl_turbo(prompt: str, output_path: str = "outputs/base.png"):
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
    print(f"✅ 베이스 이미지 생성 완료: {output_path}")
    return image

# 2. 업스케일러로 확대
def upscale_image(image, prompt: str, output_path: str = "outputs/upscaled.png"):
    upscaler = StableDiffusionUpscalePipeline.from_pretrained(
        "stabilityai/stable-diffusion-x4-upscaler",
        torch_dtype=torch.float16
    ).to("cuda")

    upscaled = upscaler(prompt=prompt, image=image).images[0]
    upscaled.save(output_path)
    print(f"✅ 업스케일 완료: {output_path}")
    return upscaled

# 3. 텍스트 오버레이
def overlay_text(image_path: str, category: str, theme: str, menus: list,
                 font_path="assets/fonts/NotoSansCJK-Regular.ttc",
                 output_path="outputs/final_menu.png"):
    img = Image.open(image_path).convert("RGBA")
    W, H = img.size
    draw = ImageDraw.Draw(img)

    # 테마 색상
    colors = {
        "bright": {"bg": "#F7F7F7E6", "text": "#1A1A1A", "accent": "#D35400"},
        "dark": {"bg": "#1C1C1CE6", "text": "#F0F0F0", "accent": "#FFD166"}
    }
    theme_colors = colors["bright"] if "화사함" in theme else colors["dark"]

    # 패널 영역
    line_height = int(W * 0.05)  # 한 줄 높이
    needed_lines = len(menus) * 3  # 이름/가격 + 설명 + 여백
    panel_h = line_height * needed_lines + int(W * 0.1)  # 타이틀 포함
    panel = Image.new("RGBA", (W, panel_h), theme_colors["bg"])
    img.alpha_composite(panel, (0, H - panel_h))

    # 폰트
    title_font = ImageFont.truetype(font_path, size=int(W * 0.05))
    item_font = ImageFont.truetype(font_path, size=int(W * 0.03))

    # 타이틀
    draw.text((int(W*0.05), H - panel_h + int(W*0.02)),
              f"{category} Menu", fill=theme_colors["accent"], font=title_font)

    # 메뉴 아이템
    y = H - panel_h + int(W*0.12)
    for item in menus:
        name, desc, price = item["name"], item["description"], item["price"]
        draw.text((int(W*0.05), y), f"{name}   {price:,}원",
                  fill=theme_colors["text"], font=item_font)
        y += int(W*0.05)
        draw.text((int(W*0.05), y), desc,
                  fill=theme_colors["text"], font=item_font)
        y += int(W*0.07)

    img.convert("RGB").save(output_path, quality=95)
    print(f"✅ 최종 메뉴판 저장 완료: {output_path}")
    return output_path

# 4. 실행
if __name__ == "__main__":
    category = 'Korean food'
    theme = '화사함'
    menus = [
        {'name': '된장찌개', 'price': 9000, 'description': '된장찌개는 예로부터 조상 대대로 내려온 된장을 이용하여 만든 찌개'},
        {'name': '계란말이', 'price': 5000, 'description': '장인이 한땀 한땀 고른 계란을 선별하여 만든 계란을 이용한 말이'},
        {'name': '소고기국밥', 'price': 10000, 'description': '소고기가 듬뿍 들어있어 남녀노소 누구나 좋아하는 소고기 국밥'},
    ]

    prompt = f"요청사항: 메뉴판 생성을 위한 백그라운드 이미지\n카테고리: {category}\n테마: {theme}"
    translated_prompt = translate(prompt)

    # base_img = run_sdxl_turbo(translated_prompt)
    # upscaled_img = upscale_image(base_img, translated_prompt)
    overlay_text("outputs/upscaled.png", category, theme, menus)


# # 유저 인풋 필드
# category = 'Korean food' # Japanese food, Chiness food, Italian food
# theme = '화사함' # 어두움, 산뜻함, 우울함
# # 메뉴명, 메뉴설명, 메뉴 가격