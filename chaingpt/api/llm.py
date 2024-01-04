# Standard lib
from operator import itemgetter
from dataclasses import dataclass

# 3rd party
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain_core.output_parsers import StrOutputParser
from langchain.callbacks import get_openai_callback

# Local


LLM_MODEL = "gpt-3.5-turbo-1106"


document_prompt = """
    You are scanning the contents of a large file from a GitHub repository
    located at the path {file_path}. You are analyzing the file chunk by chunk in order
    to answer the question '{question}'. Summarize the provided chunk, including
    any information relevant to the question. If the chunk contains no relevant information,
    respond with an empty string.

    Chunk:

    {chunk}
    """

summarize_prompt = """
    You are scanning the contents of a large file from a GitHub repository located at
    the path {file_path}. You scanned the file chunk by chunk, summarizing each chunk
    for information to answer the question '{question}'. The summarized chunks are provided below.
    Using these summaries, answer the provided question. If the summaries do not contain information
    relevant to the question, reply that there is not enough information in the file to provide an answer.

    summaries:

    {summaries}
    """

llm = ChatOpenAI(model=LLM_MODEL, temperature=0)

document_chain = ({
    "file_path": itemgetter("file_path"),
    "question": itemgetter("question"),
    "chunk": itemgetter("chunk")}
    | PromptTemplate.from_template(document_prompt)
    | llm
    | StrOutputParser()
)

summarize_chain = ({
    "file_path": itemgetter("file_path"),
    "question": itemgetter("question"),
    "summaries": lambda x: "\n\n".join(x["summaries"])}
    | PromptTemplate.from_template(summarize_prompt)
    | llm
    | StrOutputParser()
)


@dataclass
class LLMResponse():
    """
    A object representing the response from a LLM.

    output (str): The raw string output.
    model (str): The model used.
    input_tokens (str): The number of input tokens sent.
    output_tokens (str): The number of output token generated.
    """
    output: str
    model: str
    input_tokens: int
    output_tokens: int


def text_qa_refine(question: str, text: str,
                   file_path: str="unknown",
                   chunk_size: int=10000,
                   chunk_overlap: int=500) -> LLMResponse:
    """
    Uses an LLM to analyze a body of text according to a question. Text
    is split into chunks and analyzed using a refinement method.

    Args:
        question (str): The question to ask.
        text (str): The text to analyze.
        file_path (str, optional): The file path that the text originates from. Provides the LLM with additional context.
        chunk_size (int, optional): The chunk size to use when splitting the text.
        chunk_overlap (int, optional): The size of the overlap between chunks.
    
    Returns:
        An `LLMResponse` object containing the response from the LLM.
    
    Raises:
        ValueError: If the `chunk_size` is not smaller than the length of `text`.
    """
    if len(text) <= chunk_size:
        raise ValueError(f"The length of `text` must be greater than `chunk_size`. {len(text)} is not > {chunk_size}")
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,
                                              chunk_overlap=chunk_overlap)
    docs = splitter.split_text(text)
    
    inputs = [{
        "file_path": file_path,
        "question": question,
        "chunk": doc
    } for doc in docs]
    
    with get_openai_callback() as cb:
        summaries = document_chain.batch(inputs)
    
        output = summarize_chain.invoke({
            "file_path": file_path,
            "question": question,
            "summaries": summaries
        })

        return LLMResponse(output=output,
                           model=LLM_MODEL,
                           input_tokens=cb.prompt_tokens,
                           output_tokens=cb.completion_tokens)


qa_prompt = """
    You are scanning the contents of a file from a GitHub repository located at
    the path {file_path}. You are trying to answer the question '{question}'. Use only the provided
    content below. If the content does not contain any information relevant to the question, reply that
    there is not enough information in the file to provide an answer.

    content:

    {content}
    """


qa_chain = ({
    "file_path": itemgetter("file_path"),
    "question": itemgetter("question"),
    "content": lambda x: "\n\n".join(x["content"])}
    | PromptTemplate.from_template(qa_prompt)
    | llm
    | StrOutputParser()
)


def text_qa(question: str, text: str,
            file_path: str="unknown") -> LLMResponse:
    """
    Uses an LLM to analyze a body of text according to a question.

    Args:
        question (str): The question to ask.
        text (str): The text to analyze.
        file_path (str, optional): The file path that the text originates from. Provides the LLM with additional context.
    
    Returns:
        An `LLMResponse` object containing the response from the LLM.
    """
    inputs = {
        "file_path": file_path,
        "question": question,
        "content": text
    }

    with get_openai_callback() as cb:
        output = qa_chain.invoke(inputs)
        return LLMResponse(output=output,
                           model=LLM_MODEL,
                           input_tokens=cb.prompt_tokens,
                           output_tokens=cb.completion_tokens)
