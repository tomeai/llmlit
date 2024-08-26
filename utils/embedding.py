from typing import List

from zhipuai import ZhipuAI

from config.settings import settings


class ZhiPuEmbedding:
    def __init__(self):
        self.client = ZhipuAI(api_key=settings.ZHIPU_API_KEY)

    def embed_documents(self, texts: List[str]):
        """Compute doc embeddings using a modelscope embedding model.

        Args:
            texts: The list of texts to embed.

        Returns:
            List of embeddings, one for each text.
            :param texts:
            :param model:
        """
        response = self.client.embeddings.create(
            model="embedding-2",
            input=texts,
        )

        return [x.embedding for x in response.data]

    def embed_query(self, text: str):
        """Compute query embeddings using a modelscope embedding model.

        Args:
            text: The text to embed.

        Returns:
            Embeddings for the text.
            :param text:
        """
        response = self.client.embeddings.create(
            model="embedding-2",
            input=text,
        )
        return response.data[0].embedding
