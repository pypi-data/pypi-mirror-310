import json
from pydantic import BaseModel, Field
from dhisana.utils.assistant_tool_tag import assistant_tool
from dhisana.utils.built_with_api_tools import get_company_info_from_builtwith
from dhisana.utils.dataframe_tools import get_structured_output
from dhisana.utils.serpapi_search_tools import search_google

class QualifyCompanyBasedOnTechUsage(BaseModel):
    company_name: str = Field(..., description="Name of the company")
    is_company_qualified: str = Field(..., description="True if the company satifises qualification criteria in input. False otherwise.")
    reason_for_qualification: str = Field(..., description="Reason for qualification")
    
     
@assistant_tool
async def find_tech_usage_in_company(
    company_domain: str,
    company_name: str,
    technology_to_look_for: str
):
    """
    Determine if a company is using a specific technology.

    Args:
        company_domain (str): The domain name of the company's website.
        company_name (str): The name of the company.
        technology_to_look_for (str): The technology to look for.

    Returns:
        str: A JSON string containing the structured output.
    """
    # Search for job postings on the company's website mentioning the technology
    company_domain_search = f"site:{company_domain} {company_name} jobs or careers having {technology_to_look_for}"
    search_google_results = await search_google(company_domain_search, 2)

    # Search LinkedIn for people at the company with skills in the technology
    linked_in_search = f"site:linkedin.com/in OR site:linkedin.com/jobs {company_name} having people with {technology_to_look_for} skills"
    people_with_skills_results = await search_google(linked_in_search, 2)

    # Get technologies used by the company from BuiltWith
    data = await get_company_info_from_builtwith(company_domain)
    technologies = get_technologies(data)
    tech_found_in_builtwith = any(
        tech.lower() == technology_to_look_for.lower() for tech in technologies
    )

    # Prepare the prompt for structured output
    prompt = f"""
        Mark the company as qualified in is_company_qualified if the company {company_name} is using technology {technology_to_look_for}.
        DO NOT make up information.
        Give reasoning why company is qualified based on one of the reasons:
        1. There is a job posting on the company website.
        2. There are people with that skill in the company.
        3. BuiltWith shows the company uses the tech.

        Google search on company careers:
        {search_google_results}

        Google search on LinkedIn for people with skills:
        {people_with_skills_results}

        BuiltWith shows technology used: {tech_found_in_builtwith}
    """

    # Get structured output based on the prompt
    output, _ = await get_structured_output(prompt, QualifyCompanyBasedOnTechUsage)
    return json.dumps(output.dict())

def get_technologies(data):
    """
    Extract the list of technologies from BuiltWith data.

    Args:
        data (dict): The data returned by BuiltWith API.

    Returns:
        List[str]: A list of technology names used by the company.
    """
    technologies = []
    results = data.get('Results', [])
    if results:
        paths = results[0].get('Result', {}).get('Paths', [])
        if paths:
            techs = paths[0].get('Technologies', [])
            for tech in techs:
                tech_name = tech.get('Name', '')
                if tech_name:
                    technologies.append(tech_name)
    return technologies