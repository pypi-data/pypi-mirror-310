"""
为wenet训练框架加入musan噪音增强功能
"""
import os
import sys

import torch
import torchaudio

sys.path.insert(0, '../../../')
from gxl_ai_utils.utils import utils_file

# 先把musan音频搬运到nfs15
def do_copy_musan():
    source_dir = "/home/work_nfs8/asr_data/data/musan"
    partions = ["music", "noise"]
    output_dir = '/home/work_nfs15/asr_data/data/musan'
    utils_file.makedir_sil(output_dir)
    for partion in partions:
        print("processing {}".format(partion))
        output_dir_tmp = os.path.join(output_dir, partion)
        source_dir_tmp = os.path.join(source_dir, partion)
        utils_file.makedir_sil(output_dir_tmp)
        # 得到wav.scp
        wav_scp_path = os.path.join(output_dir_tmp, 'wav.scp')
        wav_dict = utils_file.get_scp_for_wav_dir(source_dir_tmp, recursive=True)
        new_wav_dict_for_write = {}
        for key, value in wav_dict.items():
            wav_name_with_suffix = os.path.basename(value)
            new_value = os.path.join(output_dir_tmp, wav_name_with_suffix)
            new_wav_dict_for_write[key] = new_value
        utils_file.write_dict_to_scp(new_wav_dict_for_write, wav_scp_path)
        # 开始复制数据
        num_thread = 20
        runner = utils_file.GxlFixedProcessPool(num_thread)
        wav_dict_list = utils_file.do_split_dict(wav_dict, num_thread)
        for i, wav_dict_item in enumerate(wav_dict_list):
            runner.add_thread(utils_file.little_func_for_cp_from_dict, [wav_dict_item, output_dir_tmp, i])
        runner.start()
def do_fix_scp_wav():
    source_dir = "/home/work_nfs15/asr_data/data/musan"
    partions = ["music", "noise"]
    for partion in partions:
        wav_scp_path = os.path.join(source_dir, partion, "wav.scp")
        wav_dict = utils_file.load_dict_from_scp(wav_scp_path)
        new_wav_dict = {}
        for key, value in wav_dict.items():
            new_wav_dict[key] = value +'.wav'
        utils_file.write_dict_to_scp(new_wav_dict, wav_scp_path)


# 得到对干净语音进行增强的函数
def do_noice_augment(input_clear_wav:torch.Tensor, input_noice_wav:torch.Tensor, snr:float=5):
    """

    :param input_clear_wav:(1,samples)
    :param input_noice_wav:(1,samples)
    :param snr: 信噪比
    :return:
    """
    # 要求噪音肯定要比干净语音长长， 如果不长，就一直翻倍，知道噪音比干净的声音大
    while input_noice_wav.size(1) < input_clear_wav.size(1):
        input_noice_wav = torch.cat([input_noice_wav, input_noice_wav], dim=1)
    # 先计算语音的功率（这里简单用均方来近似功率）
    clean_power = torch.mean(input_clear_wav ** 2)
    # 计算噪声的功率
    noise_power = torch.mean(input_noice_wav ** 2)
    # 根据信噪比公式推导出噪声需要缩放的因子
    scale_factor = torch.sqrt(clean_power / (noise_power * (10 ** (snr / 10))))
    # 对噪声张量进行缩放，以达到期望的信噪比
    scaled_noise_tensor = input_noice_wav * scale_factor
    # 确保噪声和语音长度一致（这里简单假设二者长度一样，如果不一样需要像前面示例那样裁剪等处理）
    min_length = min(input_clear_wav.shape[1], input_noice_wav.shape[1])
    clean_speech_tensor = input_clear_wav[:, :min_length]
    scaled_noise_tensor = input_noice_wav[:, :min_length]
    # 将缩放后的噪声张量和干净语音张量相加，实现添加噪声进行语音增强
    augmented_speech_tensor = clean_speech_tensor + scaled_noise_tensor
    torchaudio.save(f"./augmented_speech_snr_{snr}.wav", augmented_speech_tensor, sample_rate=16000)

if __name__ == '__main__':
    input_clear_wav = torch.load("/home/work_nfs15/asr_data/data/aishell_1/origin_wav/data_aishell/wav/test/S0764/BAC009S0764W0126.wav")
    input_noice_wav = torch.load("/home/work_nfs15/asr_data/data/musan/noise/noise-free-sound-0788.wav")
    utils_file.global_timer.start()
    do_noice_augment(input_clear_wav, input_noice_wav,0)
    utils_file.global_timer.stop_halfway_and_print()
    do_noice_augment(input_clear_wav, input_noice_wav,1)
    utils_file.global_timer.stop_halfway_and_print()
    do_noice_augment(input_clear_wav, input_noice_wav,2)
    utils_file.global_timer.stop_halfway_and_print()
    do_noice_augment(input_clear_wav, input_noice_wav,3)
    utils_file.global_timer.stop_halfway_and_print()
    do_noice_augment(input_clear_wav, input_noice_wav,4)
    utils_file.global_timer.stop_halfway_and_print()
    do_noice_augment(input_clear_wav, input_noice_wav,5)
    utils_file.global_timer.stop_halfway_and_print()
    do_noice_augment(input_clear_wav, input_noice_wav,6)
    utils_file.global_timer.stop_halfway_and_print()
