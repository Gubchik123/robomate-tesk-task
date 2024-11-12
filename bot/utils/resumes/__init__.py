from .scraper import JobSiteScraper
from .work_ua.scraper import WorkUaScraper


def get_resume_scraper_by_(site_name: str) -> JobSiteScraper:
    """Returns a resume scraper by the given site name."""
    return {"work.ua": WorkUaScraper}[site_name]
