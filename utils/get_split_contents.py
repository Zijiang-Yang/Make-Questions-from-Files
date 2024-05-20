from langchain_text_splitters import MarkdownHeaderTextSplitter

headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
        ("####", "Header 4"),
    ]
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)

def document_to_text(document):
    # 提取文档的标题
    header=""
    title = document.metadata
    for i in range(1,5):
        if f"Header {i}" in title.keys():
            tt=title[f"Header {i}"].replace("*","")
            header=header + '#'*i + tt + "\n"
    content = document.page_content
    msg=header+content
    return msg

def get_data_list(content:str):
    data_list=[]
    md_header_splits = markdown_splitter.split_text(content)
    # Split
    for i in range(len(md_header_splits)):
        data_list.append(document_to_text(md_header_splits[i]))
    return data_list