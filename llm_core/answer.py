import csv
import openai

SYS_PROMPT = '''你是一个电商主播，现在担任连州市丰阳镇的直播带货主播，请注意态度要风趣幽默，文明礼貌。请控制回答字数在40字以内。'''
QUERY_PROMPT = "你现在知道这些知识：{}\n有观众问你这个问题：{}\n作为连州市丰阳镇的直播带货主播，请用口语化文本清晰地回答观众提出的问题，并一定要控制回答在40字以内！你的回答："

SORRY_PROMPT = "{}\n以上是观众向你问的问题，如果该问题是日常交流中可能会出现的问题，请正常回答他" \
    "如果该问题不属于日常交流，请再考虑一下是否需要回答这个问题。" \
    "如果问题与你直播带货主播的身份不相关，请委婉地拒绝他。" \

threshold = 0.8

keyword_list = []
document_list = []
with open("data.csv", newline='') as file:
    reader = csv.reader(file, delimiter=',')
    next(reader, None)  # 跳过首行
    for row in reader:
        keyword_list.append(row[0])
        document_list.append(row[1])

def answer(search_result):
    avg_similarity = sum(item[1] for item in search_result) / len(search_result)

    for id_similarity_pair in search_result:
        print("搜索结果:" + str(id_similarity_pair[0]) + ", 相似度:" + str(id_similarity_pair[1]))

    print("平均相似度:" + str(avg_similarity))

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYS_PROMPT},
            {"role": "user", "content": cur_prompt},
        ],
        temperature=0
    )
    print(response['choices'][0]['message']['content'])

if __name__ == '__main__':
    answer()