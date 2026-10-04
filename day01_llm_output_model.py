from pydantic import BaseModel, Field
from typing import Optional, List
import logging

# ========== 1、日志全局配置 ==========
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


# ========== 2、Pydantic数据模型 ==========
class UserQuery(BaseModel):
    """用户提问输入校验模型"""
    query: str = Field(
        min_length=1,
        max_length=1000,
        description="用户问题，长度1~1000字符"
    )


class QAResult(BaseModel):
    """模拟大模型问答返回的结构化结果"""
    question: str = Field(description="用户原始问题")
    answer: str = Field(description="模型生成回答")
    source: Optional[List[str]] = Field(default=None, description="RAG引用的文档来源")
    confidence: float = Field(ge=0.0, le=1.0, description="置信度，0~1之间")


def main():
    logger.info("==== Day1程序开始运行 ====")

    # 模拟用户输入，作业1测试：赋值为空字符串 raw_input = ""
    raw_input = "什么是RAG检索增强生成"

    try:
        # 1.校验用户输入
        user_input = UserQuery(query=raw_input)
        logger.info(f"收到用户提问：{user_input.query}")

        # 2.模拟大模型输出结构化对象
        mock_llm_result = QAResult(
            question=user_input.query,
            answer="RAG即检索增强生成。先检索外部私有文档，把文档内容拼接到提示词，交给大模型生成答案，可以缓解大模型幻觉，让模型知道私有资料。",
            source=["rag_intro.pdf"],
            confidence=0.93
        )

        # 转为字典
        result_dict = mock_llm_result.model_dump()
        logger.info(f"转字典：{result_dict}")

        # 转为json字符串
        result_json = mock_llm_result.model_dump_json(indent=2)
        logger.info(f"转JSON:\n{result_json}")

        # ==========作业2新增代码==========
        print("\n-----作业2：model_dump()字典操作-----")
        print(f"从字典取answer字段：{result_dict['answer']}")
        print(f"从字典取confidence字段：{result_dict['confidence']}")

        print("\n-----作业2：model_dump_json 类型查看-----")
        print(f"result_json 的类型：{type(result_json)}")
        # ==========作业2新增代码结束==========

        print("\n========问答输出========")
        print(f"问题：{mock_llm_result.question}")
        print(f"回答：{mock_llm_result.answer}")
        print(f"来源：{mock_llm_result.source}")
        print(f"置信度：{mock_llm_result.confidence}")

    except Exception as e:
        logger.error(f"处理异常：{e}")


if __name__ == "__main__":
    main()
