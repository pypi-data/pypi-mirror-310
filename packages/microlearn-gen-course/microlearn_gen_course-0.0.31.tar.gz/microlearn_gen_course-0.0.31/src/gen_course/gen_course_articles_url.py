import logging

from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import Html2TextTransformer
from langchain_openai import OpenAI

from .utils import get_native_languages, get_language_name_from_iso_639_1, extract_json_from_text
from .gen_course_articles_doc import GenCourseContentFromDoc

from llm_factory.llm_factory import LLMFactory


class GenCourseContentFromURL(GenCourseContentFromDoc):
    """
    Generator class for course's article's content in batch from a URL.
    """
    def __init__(self, llm, lang: str, verbose: bool = False):
        super().__init__(llm, lang, verbose)
        self.content_extractor = AccurateContentExtractor(verbose=verbose)

    def generate(self, url: str, articles_count: int = 10, max_words: int = 150, min_words: int = 40):
        html_content = self.content_extractor.extract_content(url)
        summaries = super()._gen_summaries(html_content)

        summaries_string = "\n\n".join(summaries)

        generated_content, json_output = self.generate_output(
            articles_count=articles_count,
            max_words=max_words,
            min_words=min_words,
            text=summaries_string
        )

        if self.output_lang not in get_native_languages():
            translated_content = self.translator.generate(
                title=generated_content["title"],
                description=generated_content["description"],
                articles=json_output,
                target_lang=get_language_name_from_iso_639_1(self.output_lang),
            )
            return translated_content

        return generated_content


class AccurateContentExtractor:
    """
    Class for accurate extraction of content from a URL using LangChain tools.
    """
    def __init__(self, verbose: bool = False):
        self.logger = logging.getLogger(__name__)
        self.verbose = verbose
        self.llm = OpenAI(temperature=0)  # LLM for tool-enhanced workflows


    def extract_content(self, url: str) -> str:
        """
        Extracts and preprocesses content from the given URL.

        Args:
            url (str): URL of the webpage to extract content from.

        Returns:
            str: Extracted main content text.
        """
        try:
            self.logger.debug(f"Attempting to extract content from URL: {url}")
            # Prompt to guide content extraction
            loader = AsyncChromiumLoader([url])
            docs = loader.load()

            html_to_text = Html2TextTransformer()
            docs_transformed = html_to_text.transform_documents(docs)
            result = docs_transformed[0].page_content

            return result
        except Exception as e:
            self.logger.error(f"Failed to extract content from URL {url}: {e}")
            raise
