""" aigens.blog module """
from .outline import BlogOutlineAPI
from .ideas import BlogIdeasAPI


__all__ = ['Blog']


class Blog:
    """ aigens.Blog Class """
    def __init__(self, api_key):
        """ Blog.__init__

        Initializes a Blog object which provides all wrapped
        RapidAPI calls.

        Arguments:
            api_key: RapidAPI key

        Returns:
            Initialized Blog object
        """
        self._api_key = api_key

        # Blog Outline generation submodule
        self._outline = BlogOutlineAPI(
            self._api_key,
            'blog-outline.p.rapidapi.com',
        )

        # Blog Idea generation submodule
        self._ideas = BlogIdeasAPI(
            self._api_key,
            'blog-ideas.p.rapidapi.com',
        )

    def generate_outline(self, topic):
        """ Blog.generate_outline

        Generate a blog outline from a user-supplied topic.

        Arguments:
            topic: Blog topic in string format

        Returns:
            List of strings
        """
        return self._outline.generate_outline(topic)

    def generate_idea(self, description):
        """ Blog.generate_idea

        Generate a blog idea from a user-supplied description.

        Arguments:
            description: Idea description in string format

        Returns:
            List of idea strings
        """
        return self._ideas.generate_idea(description)
