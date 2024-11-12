from typing import Dict, Optional, List


class JobSiteScraper:
    """Base class for scraping resumes from job sites."""

    base_url: str
    params_mapping = {
        "experience": "",
        "salary_from": "",
        "salary_to": "",
    }

    @staticmethod
    def get_locations() -> Dict[str, str]:
        """Returns locations for the job site."""
        raise NotImplementedError

    @classmethod
    def get_url_by_(cls, position: str, location: str) -> str:
        """Returns the URL by the given position and location."""
        raise NotImplementedError

    @staticmethod
    def get_experience_by_(url: str) -> Dict[str, str]:
        """Returns experience levels by the given URL."""
        raise NotImplementedError

    @staticmethod
    def get_salary(url: str, id: str) -> Optional[dict]:
        """Returns salary by the given URL and id."""
        raise NotImplementedError

    @classmethod
    def parse_resumes(url: str) -> List[Dict[str, str]]:
        """Parses resumes from the given URL."""
        raise NotImplementedError
