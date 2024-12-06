import logging

from langchain_core.language_models import BaseChatModel

from ceo.prompt.prompt import Prompt

log = logging.getLogger('ceo.prompt')


class QueryResolverPrompt(Prompt):
    def __init__(self, query: str, ext_context: str = ''):
        prompt = (f'Precondition: There is a user query: "{query}"\n'
                  "Task: What you need to do is to tell user's intention based on [user query]. \n"
                  "Task Redeclare: To tell user's intention based on [user query]. "
                  "Not your (you are the assistant) intention.\n"
                  "Additional: For any details mentioned by the user, you should preserve them in full, "
                  "especially specific information with accuracy requirements such as numbers, dates, etc.\n"
                  "Firstly, deduce the user's query step by step; "
                  "Secondly break user's intention down into several minimum steps;\n"
                  'Output format: Step[n]:[Action of the step]\n'
                  'Example output: Step1:Open the door;Step2:Go into the room;Step3:Find the toys in the room;\n')
        self.__query = query
        super().__init__(prompt, ext_context)
        log.debug(f'QueryResolverPrompt: {self.prompt}')

    def invoke(self, model: BaseChatModel) -> tuple[str, str]:
        if self.__query == '':
            return f"User's intention: Don't do anything.", f"User's query(Step by step): Don't do anything."
        user_query_by_step = model.invoke(self.prompt).content
        summary_prompt = ("Task: Summarize user's query into a short sentence "
                          "which includes all the key information from user's query"
                          "(User's query is provided below at [User's query])\n"
                          f"User's query: \"{user_query_by_step}\"\n"
                          "Output format: string(summarization of [User's query])\n"
                          "Output example: To find toys for you in the room.\n")
        summary = model.invoke(summary_prompt).content
        return f"User's intention: {summary}", f"User's query(Step by step): {user_query_by_step}"
