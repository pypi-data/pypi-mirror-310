import json

class MessageFormatter:
    """
    A utility class for formatting and serializing messages.
    """

    @staticmethod
    def format_job_message(title, description, created_at):
        """
        Formats a job message as a dictionary.
        
        Args:
            title (str): The title of the job posting.
            description (str): The description of the job posting.
            created_at (str): The creation timestamp of the job posting.

        Returns:
            dict: A formatted dictionary containing the job details.
        """
        return {
            "title": title,
            "description": description,
            "created_at": created_at,
        }

    @staticmethod
    def to_json(message):
        """
        Converts a message dictionary to a JSON string.
        
        Args:
            message (dict): The message to convert.

        Returns:
            str: The message as a JSON string.
        """
        try:
            return json.dumps(message)
        except TypeError as e:
            raise ValueError(f"Failed to serialize message to JSON: {e}")

    @staticmethod
    def from_json(json_string):
        """
        Parses a JSON string into a Python dictionary.
        
        Args:
            json_string (str): The JSON string to parse.

        Returns:
            dict: The parsed dictionary.
        """
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON string: {e}")
