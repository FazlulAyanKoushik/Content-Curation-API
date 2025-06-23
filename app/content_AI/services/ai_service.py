# services/ai_service.py
import os
from typing import Dict, Any

from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq


class AIService:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0.2,
            model_name="mixtral-8x7b-32768",
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

    async def analyze_content(self, content: str) -> Dict[str, Any]:
        """Perform all analyses in one call for efficiency"""
        prompt_template = """
        Perform the following analyses on the given content:
        1. Generate a concise summary (2-3 sentences)
        2. Determine sentiment (positive/negative/neutral)
        3. Extract 3-5 main topics as comma-separated values

        Return as JSON with these keys: summary, sentiment, topics

        Content: {content}
        """

        prompt = ChatPromptTemplate.from_template(prompt_template)
        parser = JsonOutputParser()
        chain = prompt | self.llm | parser

        try:
            result = await chain.ainvoke({"content": content})
            return {
                "summary": result.get("summary", ""),
                "sentiment": result.get("sentiment", "neutral").lower(),
                "topics": result.get("topics", "")
            }
        except Exception as e:
            # Fallback to individual analyses if batch fails
            return await self._analyze_individually(content)

    async def _analyze_individually(self, content: str) -> Dict[str, Any]:
        """Fallback individual analysis if batch fails"""
        summary = await self._generate_summary(content)
        sentiment = await self._analyze_sentiment(content)
        topics = await self._extract_topics(content)
        return {
            "summary": summary,
            "sentiment": sentiment,
            "topics": topics
        }

    async def _generate_summary(self, content: str) -> str:
        prompt = ChatPromptTemplate.from_template(
            "Summarize this content in 2-3 concise sentences:\n\n{content}"
        )
        chain = prompt | self.llm | StrOutputParser()
        return await chain.ainvoke({"content": content})

    async def _analyze_sentiment(self, content: str) -> str:
        prompt = ChatPromptTemplate.from_template(
            "Analyze the sentiment of this content. Respond with ONLY one word: positive, negative, or neutral:\n\n{content}"
        )
        chain = prompt | self.llm | StrOutputParser()
        return (await chain.ainvoke({"content": content})).lower()

    async def _extract_topics(self, content: str) -> str:
        prompt = ChatPromptTemplate.from_template(
            "Extract 3-5 main topics from this content as comma-separated values. Respond with ONLY the topics:\n\n{content}"
        )
        chain = prompt | self.llm | StrOutputParser()
        return await chain.ainvoke({"content": content})