import os
from dotenv import load_dotenv
import openai
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain

class gpt_summary:

    def __init__(self, model_name) -> None:
        load_dotenv()
        openai.api_key = os.environ['OPENAI_API_KEY']
        # template

        self.template = '''
            下記の記事の要点をITエンジニアが興味を持つような記述で、200字〜300字程度で箇条書きで作成してください。
            {text}
            '''
        self.prompt = PromptTemplate(
            input_variables=['text'],
            template=self.template
        )
        
        self.llm_chain = LLMChain(
            llm=ChatOpenAI(model_name=model_name, temperature=0.3),
            prompt=self.prompt,
            verbose=True,
        )
    
    def summary(self, text:str) -> str:
        """文章を要約する

        Args:
            text: 要約対象のテキスト
        Returns:
            str: 要約後テキスト        
        """

        res = self.llm_chain.predict(text=text)
        return res
