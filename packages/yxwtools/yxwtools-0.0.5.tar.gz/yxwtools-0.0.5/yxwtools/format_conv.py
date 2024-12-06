'''
将flac mp3音频转换为wav音频
'''
import os
from pydub import AudioSegment
from concurrent.futures import ThreadPoolExecutor, as_completed


def convert_file(mp3_file_path, wav_file_path,format="mp3"):
    # 读取MP3文件并转换为WAV文件
    audio = AudioSegment.from_file(mp3_file_path, format=format)
    audio.export(wav_file_path, format="wav")
    print(f"Converted {mp3_file_path} to {wav_file_path}")


def convert_flac_to_wav(input_dir, output_dir):
    # 检查并创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for filename in os.listdir(input_dir):
            if filename.endswith(".flac"):
                mp3_file_path = os.path.join(input_dir, filename)
                wav_file_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".wav")
                # 提交任务到线程池
                futures.append(executor.submit(convert_file, mp3_file_path, wav_file_path,"flac"))
        # 等待所有任务完成
        for future in as_completed(futures):
            future.result()




def convert_mp3_to_wav(input_dir, output_dir, max_workers=None):
    # 检查并创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for filename in os.listdir(input_dir):
            if filename.endswith(".mp3"):
                mp3_file_path = os.path.join(input_dir, filename)
                wav_file_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".wav")
                # 提交任务到线程池
                futures.append(executor.submit(convert_file, mp3_file_path, wav_file_path,"mp3"))
        # 等待所有任务完成
        for future in as_completed(futures):
            future.result()


def convert_m4a_to_wav(input_dir, output_dir):
    # 检查并创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for filename in os.listdir(input_dir):
            if filename.endswith(".m4a"):
                mp3_file_path = os.path.join(input_dir, filename)
                wav_file_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".wav")
                # 提交任务到线程池
                futures.append(executor.submit(convert_file, mp3_file_path, wav_file_path,"m4a"))
        # 等待所有任务完成
        for future in as_completed(futures):
            future.result()

def convert_to_wav(input_dir,output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    convert_m4a_to_wav(input_dir, output_dir)
    convert_mp3_to_wav(input_dir, output_dir)
    convert_flac_to_wav(input_dir, output_dir)
# 示例使用
# input_directory = "./mp3"
# output_directory = "./wav3"
# convert_mp3_to_wav(input_directory, output_directory)
#
# print("All FLAC files have been converted to WAV format.")
