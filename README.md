# sprint_03_menu-generator
가장 기초적으로 구현해야 할 코드를 공유합니다.

## 개발내용
- 음식카테고리(한/중/일)
- 메뉴판 테마(화사/다크)
- 메뉴명, 메뉴설명, 메뉴 가격

## 개발환경
- Overlay (메뉴명/메뉴설명/메뉴가격)
- SDXL (background 이미지)
- Stable Diffusion2 Inpainting

## 환경설정
```
# 프로젝트 생성
uv init -p 3.12 --bare
uv sync

# 폰트 다운로드
wget https://github.com/notofonts/noto-cjk/raw/main/Sans/OTC/NotoSansCJK-Regular.ttc -O assets/fonts/NotoSansCJK-Regular.ttc


# 라이브러리 설치
## SDXL
uv add torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
uv add diffusers transformers accelerate safetensors
uv add pillow

## 번역
uv add googletrans==4.0.0-rc1
```
