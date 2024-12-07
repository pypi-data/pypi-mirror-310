from fastmodels import Client

# 初始化客户端
client = Client(
    api_key="",
    project_id=""
)
stream = True
# 调用接口
response = client.agent.threads.create_and_run(
    agent_id="4ubpzdRYpJmwAeJZxJOhAd",
    messages=[
        {"role": "user", "content": "什么是复盘模型"},
    ],
    stream=stream
)

# 打印输出
if stream:
    for chunk in response:
        # 确保 chunk.delta、chunk.delta.content 存在且至少有一个元素
        if hasattr(chunk, 'delta') and chunk.delta and chunk.delta.content and len(chunk.delta.content) > 0:
            content = chunk.delta.content[0]
            # 确保 content.text 存在并有 value 属性
            if hasattr(content, 'text') and content.text and hasattr(content.text, 'value'):
                print(f"Content: {content.text.value}, Finish Reason: {chunk.finish_reason}")

                # 确保 content.text.annotations 存在且至少有一个元素
                if hasattr(content.text, 'annotations') and content.text.annotations and len(
                        content.text.annotations) > 0:
                    annotation = content.text.annotations[0]
                    # 确保 annotation.file_citation 存在并有 filename 属性
                    if hasattr(annotation, 'file_citation') and annotation.file_citation and hasattr(
                            annotation.file_citation, 'filename'):
                        print(f"File Citation: {annotation.file_citation.filename}")

else:
    print(response.content[0].text.value)
    print(response.content[0].text.annotations[0].file_citation.filename)




