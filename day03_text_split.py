import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def split_text(text: str, chunk_size: int = 200, overlap: int = 30):
    """
    文本切片
    :param text: 原始长文本
    :param chunk_size: 每段最大字符数
    :param overlap: 两段之间重叠字符，保留上下文
    :return: chunk列表
    """
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        # 移动窗口，减去重叠
        start = end - overlap
    return chunks

if __name__ == "__main__":
    # 把刚才PDF提取出来的文本粘贴在这里测试
    raw_text = """asdfasdfju儿童和防御抗击非典和饥饿阿尔戈完全阿阿尔嘎地方 vb噶尔个阿地方嘎地方噶尔阿尔嘎地方
干部vadfggb日起阿额嘎的法担任副嘎阿尔托嘎的如果阿斯顿广泛阿尔"""
    chunk_list = split_text(raw_text, chunk_size=80, overlap=10)
    logger.info(f"一共切出 {len(chunk_list)} 个片段")
    for idx, seg in enumerate(chunk_list):
        print(f"\n--- chunk {idx+1} ---")
        print(seg)
