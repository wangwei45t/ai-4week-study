import asyncio
import httpx
from typing import Optional

# Ollama配置
OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
MODEL_NAME = "qwen2.5:7b-instruct-q4_K_M"


async def ollama_stream_chat(prompt: str):
    """
    异步流式调用Ollama，SSE逐块输出
    """
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": True  # True开启流式SSE；False一次性返回完整结果
    }

    full_content = ""

    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream("POST", OLLAMA_URL, json=payload) as response:
            # 重点：aiter_lines() 异步迭代，不是 iter_lines()
            async for line in response.aiter_lines():
                if not line:
                    continue
                # ollama SSE每行是json字符串
                import json
                chunk = json.loads(line)
                delta = chunk.get("message", {}).get("content", "")
                if delta:
                    # 实时打印，不换行，模拟打字效果
                    print(delta, end="", flush=True)
                    full_content += delta
                # 判断是否结束
                if chunk.get("done", False):
                    break
    print("\n")
    return full_content


async def ollama_normal_chat(prompt: str) -> Optional[str]:
    """非流式：一次性等待全部结果返回"""
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }
    async with httpx.AsyncClient(timeout=None) as client:
        resp = await client.post(OLLAMA_URL, json=payload)
        data = resp.json()
        return data["message"]["content"]


async def main():
    print("==== Day2 Ollama非流式测试 ====")
    answer = await ollama_normal_chat("简单解释什么是SSE流式输出？")
    print(f"完整回答:\n{answer}\n")

    print("==== Day2 Ollama流式SSE测试 ====")
    await ollama_stream_chat("简单解释什么是async异步编程？")


if __name__ == "__main__":
    asyncio.run(main())
