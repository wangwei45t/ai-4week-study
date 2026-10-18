from PyPDF2 import PdfReader
import logging

# 日志配置（复用Day1知识）
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def extract_pdf_text(pdf_file_path: str) -> str:
    """读取PDF，提取全部文本"""
    full_text = ""
    try:
        reader = PdfReader(pdf_file_path)
        logger.info(f"PDF总页数：{len(reader.pages)}")

        for page_num, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text()
            if page_text:
                full_text += page_text
                logger.info(f"已读取第 {page_num} 页")
    except Exception as e:
        logger.error(f"PDF读取失败：{e}")
    return full_text


def main():
    # 你可以替换成自己pdf文件名，放在ai-4week-study文件夹内
    pdf_path = "test.pdf"
    text_result = extract_pdf_text(pdf_path)

    print("\n===== 提取的文本前500字符预览 =====")
    print(text_result[:500])


if __name__ == "__main__":
    main()
