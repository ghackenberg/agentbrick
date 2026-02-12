from langchain_ollama import ChatOllama
from logging import getLogger

logger = getLogger(__name__)


llama3_2_1b = ChatOllama(model="llama3.2:1b")
llama3_2_3b = ChatOllama(model="llama3.2:3b")
