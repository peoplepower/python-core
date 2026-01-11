import unittest
from unittest.mock import MagicMock
from caredaily.apis.app import RAG

class TestRAG(unittest.TestCase):
    def setUp(self):
        self.rag = RAG()
        self.mock_adapter = MagicMock()
        self.rag.adapter = self.mock_adapter

    def test_upload_document(self):
        document_data = {'document': {'text': 'Test document'}}
        self.mock_adapter.post.return_value = 'upload-result'
        result = self.rag.upload_document(document_data=document_data)
        self.mock_adapter.post.assert_called_once()
        self.assertEqual(result, 'upload-result')

    def test_get_documents(self):
        self.mock_adapter.get.return_value = 'documents-result'
        result = self.rag.get_documents()
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'documents-result')

    def test_get_documents_with_location_id(self):
        self.mock_adapter.get.return_value = 'documents-result'
        result = self.rag.get_documents(location_id=1)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'documents-result')

    def test_get_documents_with_all_params(self):
        self.mock_adapter.get.return_value = 'documents-result'
        result = self.rag.get_documents(
            location_id=1,
            document_id=2,
            limit=10
        )
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'documents-result')

    def test_update_document(self):
        document_data = {'document': {'text': 'Updated document'}}
        self.mock_adapter.put.return_value = 'update-result'
        result = self.rag.update_document(doc_id=1, document_data=document_data)
        self.mock_adapter.put.assert_called_once()
        self.assertEqual(result, 'update-result')

    def test_delete_document(self):
        self.mock_adapter.delete.return_value = 'delete-result'
        result = self.rag.delete_document(doc_id=1)
        self.mock_adapter.delete.assert_called_once()
        self.assertEqual(result, 'delete-result')

    def test_post_questions(self):
        questions_data = {'question': 'What is this?'}
        self.mock_adapter.post.return_value = 'questions-result'
        result = self.rag.post_questions(questions_data=questions_data)
        self.mock_adapter.post.assert_called_once()
        self.assertEqual(result, 'questions-result')

    def test_get_questions(self):
        self.mock_adapter.get.return_value = 'questions-result'
        result = self.rag.get_questions()
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'questions-result')

    def test_get_questions_with_location_id(self):
        self.mock_adapter.get.return_value = 'questions-result'
        result = self.rag.get_questions(location_id=1)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'questions-result')

    def test_get_questions_with_all_params(self):
        self.mock_adapter.get.return_value = 'questions-result'
        result = self.rag.get_questions(
            location_id=1,
            question_id=2,
            limit=10
        )
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'questions-result')

    def test_update_questions(self):
        questions_data = {'question': 'Updated question'}
        self.mock_adapter.put.return_value = 'update-questions-result'
        result = self.rag.update_questions(questions_data=questions_data)
        self.mock_adapter.put.assert_called_once()
        self.assertEqual(result, 'update-questions-result')
