from langchain_community.chat_models import ChatLlamaCpp
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_classic.schema import StrOutputParser
from src.config.settings import settings
from src.schemas.llm import ComplaintAnalysis


class LLMInferenceService:
    def __init__(self):
        self.llm = ChatLlamaCpp(
            model_path=str(settings.MODEL_PATH / settings.LLM_MODEL_FILE_NAME),
            streaming=False,
            top_k=settings.LLM_TOP_K,
            top_p=settings.LLM_TOP_P,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS,
            verbose=False,
            repeat_penalty=settings.LLM_REPENALTY,
            n_threads=settings.LLM_N_THREADS,
            n_ctx=settings.LLM_N_CTX,
        )

        self.parser = PydanticOutputParser(pydantic_object=ComplaintAnalysis)

        self.prompt = self._setup_chat_template()

    def inference(self, query: str) -> ComplaintAnalysis:
        """Run inference and return parsed JSON."""
        chain = self.prompt | self.llm | StrOutputParser()

        raw_output = chain.invoke({"complaint": query})

        try:
            return self.parser.parse(raw_output)

        except Exception:
            # Retry with JSON correction prompt
            fix_prompt = f"""
            The following model output is invalid JSON. 
            Fix ONLY the JSON content and return valid JSON.

            Output:
            {raw_output}

            Return corrected JSON ONLY.
            """
            fixed_output = self.llm.invoke(fix_prompt).content
            return self.parser.parse(fixed_output)

    def _setup_chat_template(self) -> ChatPromptTemplate:
        """Create structured prompt with instructions + parser format."""
        format_instructions = self.parser.get_format_instructions()

        system_message = """
            You are an AI assistant for a complaint processing system.
            Your task is to analyze a user complaint and extract the required structured fields:
            - emotion
            - accused_entities
            - category
            - department

            The output MUST follow the exact JSON structure provided.
            Do NOT add explanations or extra text.
            """

        user_message = """
            Complaint:
            {complaint}

            Follow these rules:
            1. Use plain JSON.
            2. No extra fields.
            3. No comments.
            4. No markdown.

            Return output in this exact format:
            {format_instructions}
            """

        return ChatPromptTemplate.from_messages(
            [
                ("system", system_message),
                ("user", user_message),
            ]
        ).partial(format_instructions=format_instructions)
