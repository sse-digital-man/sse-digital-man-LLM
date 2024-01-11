import sys
sys.path.append(".")

from pymilvus import Collection, utility
from config import db_config
import time
from core.db_operate.connection_handler import open_connection
from core.db_operate.connection_handler import close_connection
from core.db_operate.create_collection import create_collection
from core.db_operate.create_embeddings import create_embeddings
from core.db_operate.search import search
from core.llm_core.Bot import Bot as Bot
from core.voice_input_core.AudioRecorder import AudioRecorder
from core.voice_input_core.stt.oss_handler import upload
from core.voice_input_core.stt.file_stt import fileTrans

if __name__ == '__main__':
    open_connection()

    # initialize

    if not utility.has_collection(db_config.COLLECTION_NAME): # 如果collection不存在,创建collection
        create_collection(db_config.COLLECTION_NAME)

    collection = Collection(db_config.COLLECTION_NAME)

    if collection.num_entities == 0: # 如果无embedding,创建embedding
        create_embeddings(db_config.COLLECTION_NAME)


    # search

    print("请输入:")
    while True:
        user_input = input()

        if user_input.startswith('in '):
            # 提取'in '后面的字符串
            question = user_input[3:]
            search_result = search(question)
            bot = Bot()
            answer = bot.answer(question, search_result)
            print(answer)

        elif user_input.strip() == 'mic':
            recorder = AudioRecorder()
            print("输入start开始，输入stop结束")
            while True:
                mic_op = input()
                if mic_op == 'start':
                    recorder.start()
                elif mic_op == 'stop':
                    recorder.stop()
                    recorder.save('./core/voice_input_core/input.wav')
                    break
                else:
                    print("无效命令，请重新输入")

            url = upload('./core/voice_input_core/input.wav', 'voice_input/input.wav')

            stt_start_time = time.time()
            question = fileTrans(url)
            stt_end_time = time.time()
            stt_elapsed_time = stt_end_time - stt_start_time
            print()

            search_result = search(question)
            bot = Bot()
            answer = bot.answer(question, search_result)
            print(answer)

        elif user_input == 'exit':
            break
        else:
            print("无效命令，请重新输入")

    close_connection()
