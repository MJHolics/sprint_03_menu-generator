import torch
from diffusers import AutoPipelineForText2Image, StableDiffusionUpscalePipeline

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
