import os
from PIL import Image


def compress_image(input_path, output_folder, quality):
    # 입력 파일 이름과 확장자 분리
    base_name = os.path.basename(input_path)
    file_name, _ = os.path.splitext(base_name)

    # 출력 파일 경로 설정
    output_path = os.path.join(output_folder, f"{file_name}.jpg")

    # 이미지 열기
    with Image.open(input_path) as img:
        # JPEG 형식으로 저장하면서 품질 설정
        img.convert('RGB').save(output_path, 'JPEG', quality=quality)
        print(f"Saved compressed image to {output_path} with quality={quality}")


def compress_images_in_folder(input_folder, output_folder, quality):
    # 출력 폴더가 존재하지 않으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 입력 폴더의 모든 파일에 대해 압축 수행
    for file_name in os.listdir(input_folder):
        input_path = os.path.join(input_folder, file_name)
        if os.path.isfile(input_path) and input_path.lower().endswith('.png'):
            compress_image(input_path, output_folder, quality)


def test_compress_file():
    # 입력 파일 경로와 출력 폴더 설정
    input_path = '/Users/izowooi/git/curious-cookie/python_proj/origin_png/mommy_original/000035_mommy_2.png'  # 입력 파일 경로
    output_folder = '/Users/izowooi/git/curious-cookie/python_proj/origin_png/mommy_compress'  # 출력 폴더 경로
    quality = 50  # 압축 품질 (1-100, 낮을수록 압축률이 높음)

    # 출력 폴더가 존재하지 않으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 이미지 압축 및 저장
    compress_image(input_path, output_folder, quality)


def test_compress_folder():
    # 입력 폴더와 출력 폴더 설정
    input_folder = '/Users/izowooi/git/curious-cookie/python_proj/origin_png/mommy_original'
    output_folder = '/Users/izowooi/git/curious-cookie/python_proj/origin_png/mommy_compressed'
    quality = 50  # 압축 품질 (1-100, 낮을수록 압축률이 높음), 85 는 10분의 1, 50은 20분의 1

    # 폴더 내 모든 이미지 압축 및 저장
    compress_images_in_folder(input_folder, output_folder, quality)


def main():
    test_compress_folder()


if __name__ == "__main__":
    main()
