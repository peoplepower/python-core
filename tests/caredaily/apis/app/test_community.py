import unittest
from unittest.mock import MagicMock
from caredaily.apis.app import Community

class TestCommunity(unittest.TestCase):
    def setUp(self):
        self.community = Community()
        self.mock_adapter = MagicMock()
        self.community.adapter = self.mock_adapter

    def test_get_community_posts(self):
        self.mock_adapter.get.return_value = 'posts-result'
        result = self.community.get_community_posts(location_id=1, limit=10)
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'posts-result')

    def test_get_community_posts_with_all_params(self):
        self.mock_adapter.get.return_value = 'posts-result'
        result = self.community.get_community_posts(
            location_id=1,
            community_id=2,
            post_id=3,
            limit=10
        )
        self.mock_adapter.get.assert_called_once()
        self.assertEqual(result, 'posts-result')

    def test_create_a_community_post(self):
        post_data = {'post': {'text': 'Test post'}}
        self.mock_adapter.post.return_value = 'create-result'
        result = self.community.create_a_community_post(post_data=post_data)
        self.mock_adapter.post.assert_called_once()
        self.assertEqual(result, 'create-result')

    def test_create_a_community_post_with_notification(self):
        post_data = {'post': {'text': 'Test post'}}
        self.mock_adapter.post.return_value = 'create-result'
        result = self.community.create_a_community_post(
            post_data=post_data,
            notification=True
        )
        self.mock_adapter.post.assert_called_once()
        self.assertEqual(result, 'create-result')

    def test_update_a_community_post(self):
        post_data = {'post': {'text': 'Updated post'}}
        self.mock_adapter.put.return_value = 'update-result'
        result = self.community.update_a_community_post(post_id=1, post_data=post_data)
        self.mock_adapter.put.assert_called_once()
        self.assertEqual(result, 'update-result')

    def test_delete_a_community_post(self):
        self.mock_adapter.delete.return_value = 'delete-result'
        result = self.community.delete_a_community_post(post_id=1)
        self.mock_adapter.delete.assert_called_once()
        self.assertEqual(result, 'delete-result')

    def test_create_community_post_comment(self):
        """Test creating a comment on a community post"""
        comment_data = {'comment': {'text': 'Test comment', 'postId': 1}}
        self.mock_adapter.post.return_value = 'comment-result'
        result = self.community.create_community_post_comment(comment_data=comment_data)
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/communityPostComments')
        self.assertEqual(kwargs['ep_json'], comment_data)
        self.assertEqual(result, 'comment-result')

    def test_create_community_post_comment_with_reply(self):
        """Test creating a reply comment on a community post"""
        comment_data = {'comment': {'text': 'Reply comment', 'postId': 1, 'parentCommentId': 2}}
        self.mock_adapter.post.return_value = 'reply-result'
        result = self.community.create_community_post_comment(comment_data=comment_data)
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_json'], comment_data)
        self.assertEqual(result, 'reply-result')

    def test_delete_community_post_comment(self):
        """Test deleting a comment from a community post"""
        comment_id = 2
        self.mock_adapter.delete.return_value = 'delete-comment-result'
        result = self.community.delete_community_post_comment(comment_id=comment_id)
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/communityPostComments')
        self.assertEqual(kwargs['ep_params']['commentId'], comment_id)
        self.assertEqual(result, 'delete-comment-result')

    def test_update_community_post_reaction(self):
        """Test adding/updating a reaction to a community post"""
        reaction_data = {'reaction': 'like', 'postId': 1}
        self.mock_adapter.put.return_value = 'reaction-result'
        result = self.community.update_community_post_reaction(reaction_data=reaction_data)
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/communityPostReaction')
        self.assertEqual(kwargs['ep_json'], reaction_data)
        self.assertEqual(result, 'reaction-result')

    def test_update_community_post_reaction_to_comment(self):
        """Test adding/updating a reaction to a comment"""
        reaction_data = {'reaction': 'like', 'postId': 1, 'commentId': 2}
        self.mock_adapter.put.return_value = 'reaction-result'
        result = self.community.update_community_post_reaction(reaction_data=reaction_data)
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(kwargs['ep_json'], reaction_data)
        self.assertEqual(result, 'reaction-result')

    def test_get_community_post_files(self):
        """Test getting files for a community post"""
        post_id = 1
        self.mock_adapter.get.return_value = 'files-result'
        result = self.community.get_community_post_files(post_id=post_id)
        args, kwargs = self.mock_adapter.get.call_args
        self.assertEqual(args[0], f'/espapi/cloud/json/communityPosts/{post_id}/files')
        self.assertEqual(result, 'files-result')

    def test_upload_community_post_file(self):
        """Test uploading a file to a community post"""
        post_id = 1
        file_type = 2  # image
        content_type = 'image/jpeg'
        file_data = {'fileName': 'test.jpg'}
        self.mock_adapter.post.return_value = 'file-upload-result'
        result = self.community.upload_community_post_file(
            post_id=post_id,
            file_type=file_type,
            content_type=content_type,
            file_data=file_data
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(args[0], f'/espapi/cloud/json/communityPosts/{post_id}/files')
        self.assertEqual(kwargs['ep_params']['type'], file_type)
        self.assertEqual(kwargs['ep_params']['contentType'], content_type)
        self.assertEqual(kwargs['ep_json'], file_data)
        self.assertEqual(result, 'file-upload-result')

    def test_upload_community_post_file_with_optional_params(self):
        """Test uploading a file with optional parameters"""
        post_id = 1
        file_type = 1  # video
        content_type = 'video/mp4'
        file_data = {'fileName': 'test.mp4'}
        ext = 'mp4'
        thumbnail_content_type = 'image/jpeg'
        self.mock_adapter.post.return_value = 'file-upload-result'
        result = self.community.upload_community_post_file(
            post_id=post_id,
            file_type=file_type,
            content_type=content_type,
            file_data=file_data,
            ext=ext,
            thumbnail_content_type=thumbnail_content_type
        )
        args, kwargs = self.mock_adapter.post.call_args
        self.assertEqual(kwargs['ep_params']['ext'], ext)
        self.assertEqual(kwargs['ep_params']['thumbnailContentType'], thumbnail_content_type)
        self.assertEqual(result, 'file-upload-result')

    def test_update_community_post_file(self):
        """Test updating a file for a community post"""
        post_id = 1
        file_id = 123
        file_data = {'fileName': 'updated.jpg'}
        self.mock_adapter.put.return_value = 'file-update-result'
        result = self.community.update_community_post_file(
            post_id=post_id,
            file_id=file_id,
            file_data=file_data
        )
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], f'/espapi/cloud/json/communityPosts/{post_id}/files')
        self.assertEqual(kwargs['ep_params']['fileId'], file_id)
        self.assertEqual(kwargs['ep_json'], file_data)
        self.assertEqual(result, 'file-update-result')

    def test_delete_community_post_file(self):
        """Test deleting a file from a community post"""
        post_id = 1
        file_id = 123
        self.mock_adapter.delete.return_value = 'delete-file-result'
        result = self.community.delete_community_post_file(post_id=post_id, file_id=file_id)
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], f'/espapi/cloud/json/communityPosts/{post_id}/files')
        self.assertEqual(kwargs['ep_params']['fileId'], file_id)
        self.assertEqual(result, 'delete-file-result')

    def test_put_community_posts(self):
        """Test Case ID: TC-Community-001
        Title: Update Community Posts at Collection Level
        Priority: P1
        """
        posts_data = {'posts': [{'id': 1, 'text': 'Updated'}]}
        self.mock_adapter.put.return_value = {'resultCode': 0}
        result = self.community.put_community_posts(posts_data=posts_data)
        self.mock_adapter.put.assert_called_once()
        args, kwargs = self.mock_adapter.put.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/communityPosts')
        self.assertEqual(kwargs['ep_json'], posts_data)
        self.assertEqual(result, {'resultCode': 0})

    def test_delete_community_posts(self):
        """Test Case ID: TC-Community-002
        Title: Delete Community Posts at Collection Level
        Priority: P1
        """
        post_ids = [1, 2, 3]
        self.mock_adapter.delete.return_value = {'resultCode': 0}
        result = self.community.delete_community_posts(post_ids=post_ids)
        self.mock_adapter.delete.assert_called_once()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertEqual(args[0], '/espapi/cloud/json/communityPosts')
        self.assertEqual(kwargs['ep_params']['postId'], post_ids)
        self.assertEqual(result, {'resultCode': 0})

    def test_delete_community_posts_all(self):
        """Test Case ID: TC-Community-003
        Title: Delete All Community Posts
        Priority: P2
        """
        self.mock_adapter.delete.return_value = {'resultCode': 0}
        result = self.community.delete_community_posts()
        args, kwargs = self.mock_adapter.delete.call_args
        self.assertIsNone(kwargs.get('ep_params'))
        self.assertEqual(result, {'resultCode': 0})
