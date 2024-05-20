import tiktoken


def count_openai_tokens(content):
    encoding = tiktoken.encoding_for_model("gpt-4")
    #print('********************encoding')
    token_count = len(encoding.encode(content))
    #print('----------------------------token_count:',token_count,'\n')
    return token_count