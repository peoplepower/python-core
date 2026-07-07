# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

from typing import Dict

from ...models import Result
from ..api import API


class RAG(API):
    """
    RAG (Retrieval-Augmented Generation) API for managing documents and questions.

    This class provides methods to upload, retrieve, update, and delete RAG documents,
    as well as manage questions for RAG-based queries.

    Reference:
        https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/RAG
    """

    def upload_document(
        self,
        document_data: Dict,
    ) -> Result:
        """
        Upload RAG Document.

        Upload a new document for RAG-based retrieval.

        Args:
            document_data: Document data as JSON object

        Returns:
            Result: API response with upload result

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/RAG
        """
        result: Result = self.adapter.post(
            "/cloud/json/rag/documents",
            ep_json=document_data if document_data else None,
        )
        return result

    def get_documents(
        self,
        location_id: int = None,
        document_id: int = None,
        limit: int = None,
    ) -> Result:
        """
        Get RAG Documents.

        Retrieve RAG documents with optional filtering.

        Args:
            location_id: Filter by location ID
            document_id: Filter by specific document ID
            limit: Maximum number of documents to retrieve

        Returns:
            Result: API response with list of documents

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/RAG
        """
        params = {
            "locationId": location_id,
            "docId": document_id,
            "limit": limit,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/cloud/json/rag/documents",
            ep_params=params,
        )
        return result

    def update_document(
        self,
        doc_id: int,
        document_data: Dict,
    ) -> Result:
        """
        Update RAG Document.

        Update an existing RAG document.

        Args:
            doc_id: Document ID to update
            document_data: Document data as JSON object with updated information

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/RAG
        """
        result: Result = self.adapter.put(
            f"/cloud/json/rag/documents/{doc_id}",
            ep_json=document_data if document_data else None,
        )
        return result

    def delete_document(
        self,
        doc_id: int,
    ) -> Result:
        """
        Delete RAG Document.

        Delete a RAG document.

        Args:
            doc_id: Document ID to delete

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/RAG
        """
        result: Result = self.adapter.delete(
            f"/cloud/json/rag/documents/{doc_id}",
        )
        return result

    def post_questions(
        self,
        questions_data: Dict,
    ) -> Result:
        """
        Post RAG Questions.

        Submit questions for RAG-based query processing.

        Args:
            questions_data: Questions data as JSON object

        Returns:
            Result: API response with query results

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/RAG
        """
        result: Result = self.adapter.post(
            "/cloud/json/rag/questions",
            ep_json=questions_data if questions_data else None,
        )
        return result

    def get_questions(
        self,
        location_id: int = None,
        question_id: int = None,
        limit: int = None,
    ) -> Result:
        """
        Get RAG Questions.

        Retrieve RAG questions with optional filtering.

        Args:
            location_id: Filter by location ID
            question_id: Filter by specific question ID
            limit: Maximum number of questions to retrieve

        Returns:
            Result: API response with list of questions

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/RAG
        """
        params = {
            "locationId": location_id,
            "questionId": question_id,
            "limit": limit,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/cloud/json/rag/questions",
            ep_params=params,
        )
        return result

    def update_questions(
        self,
        questions_data: Dict,
    ) -> Result:
        """
        Update RAG Questions.

        Update existing RAG questions.

        Args:
            questions_data: Questions data as JSON object with updated information

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/RAG
        """
        result: Result = self.adapter.put(
            "/cloud/json/rag/questions",
            ep_json=questions_data if questions_data else None,
        )
        return result
