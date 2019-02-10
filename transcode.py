

import os
import subprocess
import re
# import fcntl

# path_ffmpeg = 
path_ffmpeg = r'C:\work\ffmpeg\ffmpeg-3.4.2-win64-static\bin\ffmpeg.exe'
dir_ts_files = r'E:\ts'
dir_output = r'E:\hb'
path_lock = r'C:\work\ffmpeg\encode.lock'

def get_work_base(f_base):
    re_num = re.compile(r'(\d+)\-.+')
    r = re_num.search(f_base)
    res = ''
    if r:
        print(r.group(1))
        res = r.group(1)
    else:
        print('error... cant find f_base.')
    return res

def chk_tmp_file(f_tmp):
    pass

def get_file_base(path):
    fname = os.path.basename(path)
    return fname.split('.ts')[0]

def _exec_transcode(path):
    f_base = get_file_base(path)
    work_base = get_work_base(f_base)

    f_in = os.path.join(dir_ts_files, f_base + '.ts')
    f_tmp = os.path.join(dir_output, work_base + '_tmp.m4v')
    f_out = os.path.join(dir_output, f_base + '.m4v')
        
    #opt = '-i %(f_in)s -vf scale=720:-1 -c:v libx264 -preset faster -crf 27 -c:a aac -b:a 96k -filter_complex channelsplit %(f_tmp)s'
    #opt = '-i %(f_in)s -vf scale=720:-1,yadif=0:-1:1 -c:v libx264 -preset faster -crf 27 -g 1 -c:a aac -b:a 96k -filter_complex channelsplit %(f_tmp)s'
    opt = '-i "%(f_in)s" -vf scale=720:-1,yadif=0:-1:1 -c:v libx264 -preset faster -crf 27 -c:a aac -b:a 96k -filter_complex channelsplit "%(f_tmp)s"'
    #opt = '-i %(f_in)s -vf scale=840:-1,yadif=0:-1:1 -c:v libx264 -preset faster -crf 26 -c:a aac -b:a 96k -filter_complex channelsplit %(f_tmp)s'
    enc_args = opt % vars()

    if os.path.exists(f_tmp):
        os.remove(f_tmp)

    # cmd = ' '.join([ffmpeg, f_in, f_out])
    cmd = path_ffmpeg + ' ' + enc_args
    print(cmd)
    # res = subprocess.run([ffmpeg, enc_args], stdout=subprocess.PIPE)
    res = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
    #return res
    if res and res.returncode == 0:
        print('Well done. encoding .....')
        print('rename')
        os.rename(f_tmp, f_out)
    else:
        print('failed .....    remove tmp-file')
        os.remove(f_tmp)
    return

def del_files():
    pass

def itr_ts_files():
    # [print(path) for path in os.listdir(dir_ts) if path.endswith('.ts')]
    for path in os.listdir(dir_ts_files):
        if path.endswith('.ts'):
            yield path

def transcode():
    # 複数プロセス起動を防ぐためファイルロックを利用。x-modeでopen (for Windows)
    #os.remove(path_lock)
    #return
    try:
        with open(path_lock, 'x') as fl:
            for path in itr_ts_files():
                print('\nStart transcode [%s]' % path)
                _exec_transcode(path)
        os.remove(path_lock)
        print('Finish transcode [%s]' % path)
    except FileExistsError as e:
        # print('ロックを獲得できませんでした... エンコード中')
        print(e)
    return


# TODO
# tmp-file をロック。できなければ終了。
# f_out があれば、終了。
# f_in を削除 (正常終了の場合)
# ts ファイルのステータスチェック(録画済か録画中か？)
# ts ファイルをみつけて、エンコード開始


if __name__ == '__main__':
    transcode()
