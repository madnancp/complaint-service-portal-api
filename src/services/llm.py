from langchain_community.chat_models import ChatLlamaCpp
from langchain.prompt import ChatPromptTemplate
from src.config.settings import settings


class LLMInferenceService:
    def __init__(self):
        self.llm = ChatLlamaCpp(
            model_path=str(settings.MODEL_PATH / settings.LLM_MODEL_FILE_NAME),
            streaming=True,
            top_k=settings.LLM_TOP_K,
            top_p=settings.LLM_TOP_P,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            verbose=False,
            n_threads=settings.LLM_N_THREADS,
            n_ctx=settings.LLM_N_CTX,
        )

    def inference(self, query: str):
        prompt = self._setup_chat_template()
        chain = prompt | self.llm
        return chain.invoke({"query": query})

    def _setup_chat_template(
        self,
    ) -> ChatPromptTemplate:
        prompt = ChatPromptTemplate.from_messages([("system", ""), ("user",)])
        return prompt
