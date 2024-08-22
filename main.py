import logging
import yaml
from dotenv import load_dotenv
from src.linkedin_login import LinkedInLogin
from src.job_search import JobSearch
from src.job_apply import JobApply

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='linkedin_job_applier.log'
    )

def load_config():
    with open('config.yml', 'r') as file:
        return yaml.safe_load(file)

def main():
    setup_logging()
    load_dotenv()  # Load environment variables
    config = load_config()
    
    linkedin = LinkedInLogin(config['linkedin'])
    driver = linkedin.login()
    
    job_search = JobSearch(driver, config['job_search'])
    job_listings = job_search.search()
    
    job_apply = JobApply(driver, config['application'])
    job_apply.apply_to_jobs(job_listings)

if __name__ == "__main__":
    main()