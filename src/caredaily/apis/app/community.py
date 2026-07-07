# /// script
# requires-python = ">=3.8"
# dependencies = [
#   "requests",
# ]
# ///

from typing import Dict, List, Optional

from ...models import Result
from ..api import API


class Community(API):
    """
    Community API for managing community posts, comments, reactions, and files.

    This class provides methods to create, retrieve, update, and delete community posts,
    manage comments and reactions, and handle file uploads for community content.

    Reference:
        https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Community
    """

    def get_community_posts(
        self,
        location_id: int = None,
        community_id: int = None,
        post_id: int = None,
        limit: int = None,
    ) -> Result:
        """
        Retrieve community posts.

        Args:
            location_id: Filter by location ID
            community_id: Filter by community ID
            post_id: Filter by specific post ID
            limit: Maximum number of posts to retrieve

        Returns:
            Result: API response with list of posts

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Community/operation/Get%20Posts
        """
        params = {
            "locationId": location_id,
            "communityId": community_id,
            "postId": post_id,
            "limit": limit,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.get(
            "/cloud/json/communityPosts",
            ep_params=params,
        )
        return result

    def create_a_community_post(
        self,
        post_data: Dict,
        notification: bool = None,
    ) -> Result:
        """
        Create a new community post.

        Post Types:
        - 1: Individual
        - 2: Location
        - 3: Community

        Post Status:
        - 0: Private, visible for owner only, reminders are stopped
        - 1: Active, visible for users, reminders are enabled
        - 2: Rejected, reminders are stopped

        Args:
            post_data: Post data as JSON object with 'post' key containing post information
            notification: Send notifications to users for new location/community post

        Returns:
            Result: API response with created post data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Community/operation/Create%20Post
        """
        params = {
            "notification": notification,
        }
        params = {k: v for k, v in params.items() if v is not None}
        result: Result = self.adapter.post(
            "/cloud/json/communityPosts",
            ep_params=params,
            ep_json=post_data if post_data else None,
        )
        return result

    def update_a_community_post(
        self,
        post_id: int,
        post_data: Dict,
    ) -> Result:
        """
        Update an existing community post.

        Args:
            post_id: Post ID to update
            post_data: Post data as JSON object with 'post' key containing updated post information

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Community/operation/Update%20Post
        """
        result: Result = self.adapter.put(
            f"/cloud/json/communityPosts/{post_id}",
            ep_json=post_data if post_data else None,
        )
        return result

    def put_community_posts(
        self,
        posts_data: Dict,
    ) -> Result:
        """
        Update Community Posts.

        Update community posts at the collection level.

        Args:
            posts_data: Posts data as JSON object

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Community/operation/Update%20Community%20Posts
        """
        result: Result = self.adapter.put(
            "/cloud/json/communityPosts",
            ep_json=posts_data if posts_data else None,
        )
        return result

    def delete_community_posts(
        self,
        post_ids: Optional[List[int]] = None,
    ) -> Result:
        """
        Delete Community Posts.

        Delete community posts at the collection level.

        Args:
            post_ids: List of post IDs to delete (optional, if not provided deletes all)

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Community/operation/Delete%20Community%20Posts
        """
        params = {}
        if post_ids is not None:
            params["postId"] = post_ids
        result: Result = self.adapter.delete(
            "/cloud/json/communityPosts",
            ep_params=params if params else None,
        )
        return result

    def delete_a_community_post(
        self,
        post_id: int,
    ) -> Result:
        """
        Delete a community post.

        Args:
            post_id: Post ID to delete

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Community/operation/Delete%20Post
        """
        result: Result = self.adapter.delete(
            f"/cloud/json/communityPosts/{post_id}",
        )
        return result

    def create_community_post_comment(
        self,
        comment_data: Dict,
    ) -> Result:
        """
        Create a comment on a community post.

        Args:
            comment_data: Comment data as JSON object with 'comment' key

        Returns:
            Result: API response with comment data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Community/operation/Create%20Comment
        """
        result: Result = self.adapter.post(
            "/cloud/json/communityPostComments",
            ep_json=comment_data,
        )
        return result

    def delete_community_post_comment(
        self,
        comment_id: int,
    ) -> Result:
        """
        Delete a comment from a community post.

        Args:
            comment_id: Comment ID to delete

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Community/operation/Delete%20Comment
        """
        params = {
            "commentId": comment_id,
        }
        result: Result = self.adapter.delete(
            "/cloud/json/communityPostComments",
            ep_params=params,
        )
        return result

    def update_community_post_reaction(
        self,
        reaction_data: Dict,
    ) -> Result:
        """
        Add or update a reaction to a community post or comment.

        Args:
            reaction_data: Reaction data as JSON object

        Returns:
            Result: API response with reaction data

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Community/operation/Update%20Reaction
        """
        result: Result = self.adapter.put(
            "/cloud/json/communityPostReaction",
            ep_json=reaction_data,
        )
        return result

    def get_community_post_files(
        self,
        post_id: int,
    ) -> Result:
        """
        Get files for a community post.

        Args:
            post_id: Post ID (required)

        Returns:
            Result: API response with list of files

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Community/operation/Get%20Post%20Files
        """
        result: Result = self.adapter.get(
            f"/cloud/json/communityPosts/{post_id}/files",
        )
        return result

    def upload_community_post_file(
        self,
        post_id: int,
        file_type: int,
        content_type: str,
        file_data: Dict,
        ext: Optional[str] = None,
        thumbnail_content_type: Optional[str] = None,
    ) -> Result:
        """
        Upload File to Community Post.

        A client requests only a creation of the file record without immediate uploading
        of the file or thumbnail content.

        Args:
            post_id: Post ID (required)
            file_type: File type (0=any, 1=video, 2=image, 3=audio) (required)
            content_type: File content type (required)
            file_data: File data as JSON object
            ext: File extension
            thumbnail_content_type: Thumbnail content type

        Returns:
            Result: API response with upload URLs

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Community/operation/Upload%20File
        """
        params = {
            "type": file_type,
            "contentType": content_type,
        }
        if ext is not None:
            params["ext"] = ext
        if thumbnail_content_type is not None:
            params["thumbnailContentType"] = thumbnail_content_type
        result: Result = self.adapter.post(
            f"/cloud/json/communityPosts/{post_id}/files",
            ep_params=params,
            ep_json=file_data,
        )
        return result

    def update_community_post_file(
        self,
        post_id: int,
        file_id: int,
        file_data: Dict,
    ) -> Result:
        """
        Update a file for a community post.

        Args:
            post_id: Post ID (required)
            file_id: File ID (required)
            file_data: File data as JSON object

        Returns:
            Result: API response confirming update

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Community/operation/Update%20Post%20File
        """
        params = {
            "fileId": file_id,
        }
        result: Result = self.adapter.put(
            f"/cloud/json/communityPosts/{post_id}/files",
            ep_params=params,
            ep_json=file_data,
        )
        return result

    def delete_community_post_file(
        self,
        post_id: int,
        file_id: int,
    ) -> Result:
        """
        Delete a file from a community post.

        Args:
            post_id: Post ID (required)
            file_id: File ID (required)

        Returns:
            Result: API response confirming deletion

        Reference:
            https://app.peoplepowerco.com/cloud/apidocs/cloud.html#tag/Community/operation/Delete%20Post%20File
        """
        params = {
            "fileId": file_id,
        }
        result: Result = self.adapter.delete(
            f"/cloud/json/communityPosts/{post_id}/files",
            ep_params=params,
        )
        return result
