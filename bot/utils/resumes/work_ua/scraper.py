from typing import Dict, Union, Optional, List

from bs4 import BeautifulSoup

from ..request import get_soup_by_
from ..scraper import JobSiteScraper


class WorkUaScraper(JobSiteScraper):
    """Class for scraping resumes from the work.ua."""

    base_url = "https://www.work.ua"
    params_mapping = {
        "experience": "experience",
        "salary_from": "salaryfrom",
        "salary_to": "salaryto",
    }

    @staticmethod
    def get_locations() -> Dict[str, str]:
        """Returns locations for the work.ua."""
        return {
            "All Ukraine": "",
            "Other countries": "other",
            "Remote": "remote",
        }

    @classmethod
    def get_url_by_(
        cls,
        position: str,
        location: str,
        params: Optional[Dict[str, Union[str, int]]] = None,
    ) -> str:
        """Returns the URL by the given position and location."""
        location = location.lower()
        position = position.replace(" ", "+").lower()
        if params is None:
            return f"{cls.base_url}/en/resumes-{location}-{position}/"
        params = "&".join(
            f"{cls.params_mapping[key]}={value}"
            for key, value in params.items()
        )
        return f"{cls.base_url}/en/resumes-{location}-{position}/?{params}"

    @staticmethod
    def get_experience_by_(url: str) -> Dict[str, str]:
        """Returns experience levels by the given URL."""
        soup = get_soup_by_(url)
        experience_selection = soup.find("ul", id="experience_selection")
        experience = {}
        for label in experience_selection.find_all("label"):
            spans = label.find_all("span")
            experience[f"{spans[0].text} ({int(spans[1].text)})"] = int(
                label.find("input").get("value")
            )
        return experience

    @staticmethod
    def get_salary(url: str, id: str) -> Optional[dict]:
        """Returns salary by the given URL and id."""
        soup = get_soup_by_(url)
        salary_selection = soup.find("select", id=f"salary{id}_selection")
        salary = {}
        for option in salary_selection.find_all("option"):
            salary[option.text.strip()] = int(option.get("value"))
        if max(salary.values()) == 0:
            return None
        return salary

    @classmethod
    def parse_resumes(cls, url: str) -> str:
        """Parses resumes from the given URL."""
        resumes = cls._parse_resumes(url)
        sorted_resumes = cls._sort_(resumes)
        return cls._format_message(sorted_resumes[:5])

    @classmethod
    def _sort_(cls, resumes: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Sorts resumes by the score."""
        for resume in resumes:
            resume["score"] = cls._calculate_score(resume)
        return sorted(resumes, key=lambda x: x["score"], reverse=True)

    @staticmethod
    def _calculate_score(resume: Dict[str, str]) -> int:
        """Calculates the score of the resume."""
        score = 0
        # Completeness of resume
        if resume.get("description"):
            score += 10
        if resume.get("experience"):
            score += 10
        if resume.get("resumes"):
            score += 5
        # Education level
        if "Higher education" in resume.get("description", ""):
            score += 10
        elif "Unfinished higher education" in resume.get("description", ""):
            score += 5
        elif "Specialized secondary education" in resume.get(
            "description", ""
        ):
            score += 3
        elif "Secondary education" in resume.get("description", ""):
            score += 2
        # Employment type
        if "Full-time" in resume.get("description", ""):
            score += 10
        elif "Part-time" in resume.get("description", ""):
            score += 5
        return score

    @staticmethod
    def _format_message(sorted_resumes: List[Dict[str, str]]) -> str:
        """Formats resumes into the HTML message."""
        message = ""
        for resume in sorted_resumes:
            message += (
                f"<a href='{resume['link']}'>{resume['position']}</a>\n"
                f"{resume['name']}\n"
            )
            if resume["description"]:
                message += f"{resume['description']}\n"
            if resume["experience"]:
                message += "<b>Experience:</b>\n"
                for e in resume["experience"]:
                    message += f"- <i>{e['position']}, {e['company']}</i>\n"
            if resume["resumes"]:
                message += "<b>Resumes:</b>\n"
                for res in resume["resumes"]:
                    message += (
                        f"- <a href='{res['link']}'>{res['position']}</a>"
                        f"{res['description']}\n"
                    )
            message += f"<b>Time:</b>\n\n"
        return message

    @classmethod
    def _parse_resumes(cls, url: str) -> List[Dict[str, str]]:
        """Parses resumes from the given URL."""
        resumes = []
        soup = get_soup_by_(url)
        pages = cls._get_pages(soup)

        for page in range(1, pages + 1):
            if page > 1:
                soup = get_soup_by_(f"{url}&page={page}")

            for resume in soup.find_all("div", class_="resume-link"):
                resumes.append(cls._parse_resume(resume))
        return resumes

    @staticmethod
    def _get_pages(soup: BeautifulSoup) -> int:
        """Returns the number of pages from pagination in the given soup."""
        pages = 1
        if pagination := soup.find("ul", class_="pagination"):
            pages = int(pagination.find_all("li")[-2].text)
        return pages

    @classmethod
    def _parse_resume(cls, resume: BeautifulSoup) -> dict[str, str]:
        """Parses the given resume."""
        paragraphs = resume.find_all("p")
        data = {
            "position": resume.find("h2").text.strip(),
            "link": cls.base_url + resume.find("h2").find("a").get("href"),
            "name": paragraphs[0].text.strip(),
            "description": (
                paragraphs[1].text.strip() if len(paragraphs) > 1 else ""
            ),
            "time": resume.find("time").get("datetime"),
            "experience": [],
            "resumes": [],
        }
        lists = resume.find("div").find_next_siblings("ul")
        if len(lists) >= 1:
            for li in lists[0].find_all("li"):
                li_info = li.text.strip().split(",")
                data["experience"].append(
                    {
                        "position": li_info[0].strip(),
                        "company": li_info[1].strip(),
                        "time": li_info[-1].strip(),
                    }
                )
        if len(lists) >= 2:
            for li in lists[1].find_all("li"):
                data["resumes"].append(
                    {
                        "link": cls.base_url + li.find("a").get("href"),
                        "position": li.find("a").text.strip(),
                        "description": li.find("span").text.strip(),
                    }
                )
        return data
