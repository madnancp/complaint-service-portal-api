from langchain_community.chat_models import ChatLlamaCpp
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_classic.schema import StrOutputParser
from src.config.settings import settings
from src.schemas.llm import ComplaintAnalysis


class LLMInferenceService:
    def __init__(self):
        print("[INFO] Initializing LLM inference service...")

        print(
            f"[INFO] Loading LlamaCPP model from {settings.MODEL_PATH / settings.LLM_MODEL_FILE_NAME}"
        )
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

        print("[INFO] Initializing Pydantic parser...")
        self.parser = PydanticOutputParser(pydantic_object=ComplaintAnalysis)

        print("[INFO] Setting up prompt template...")
        self.prompt = self._setup_chat_template()

        print("[INFO] LLM inference service initialized.")

    def inference(self, query: str) -> ComplaintAnalysis:
        """Run inference and return parsed JSON."""
        print(f"[INFO] Starting inference for: {query}")
        chain = self.prompt | self.llm | StrOutputParser()

        print("[INFO] Invoking chain with user input")
        raw_output = chain.invoke({"complaint": query})

        print(f"[INFO] Raw LLM Outpu received : {raw_output}")

        try:
            print("Attempting to parse output into ComplaintAnalysis schema...")
            parsed = self.parser.parse(raw_output)
            print("Parsing successful. Returning structured response.")

            return parsed

        except Exception as e:
            print(
                "Initial parsing failed. Attempting JSON correction... Error: %s",
                str(e),
            )
            fix_prompt = f"""
            The following model output is invalid JSON. 
            Fix ONLY the JSON content and return valid JSON.

            Output:
            {raw_output}

            Return corrected JSON ONLY.
            """
            print("Sending correction prompt to LLM...")
            fixed_output = self.llm.invoke(fix_prompt).content
            print(f"Corrected LLM output: {fixed_output}")

            parsed = self.parser.parse(fixed_output)
            print("JSON correction successful. Returning parsed output.")

            return parsed

    def _setup_chat_template(self) -> ChatPromptTemplate:
        """Create structured prompt with instructions + parser format."""

        print("Generating format instructions for prompt...")
        format_instructions = self.parser.get_format_instructions()

        print("Creating structured system/user messages for the prompt...")
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

        print("Prompt template created successfully.")
        return ChatPromptTemplate.from_messages(
            [
                ("system", system_message),
                ("user", user_message),
            ]
        ).partial(format_instructions=format_instructions)
