# I used here some of the code in this repo
# https://github.com/arapfaik/scraping-glassdoor-selenium/blob/master/glassdoor%20scraping.ipynb
# I made several changes in the structure and fixed some issues

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd


class GlassdoorJobScraper(object):
    def __init__(self, webdriver_path, driver_options , chrome=False, firefox=False):
        print(webdriver_path)
        print(driver_options)
        try:
            if chrome:
                self.driver = webdriver.Chrome(executable_path=webdriver_path, options=driver_options)
            elif firefox:
                self.driver =  webdriver.Firefox(executable_path=webdriver_path, options=driver_options)
            else:
                raise Exception("You need to specify a valid webdriver either Chrome or Firfox")
        except Exception as err:
            print(err)
            
    def scrape(self, jobs_keywords, jobs_num=50 ):
        
        if type(jobs_keywords ) != list: raise TypeError
        if len(jobs_keywords) < 1: raise Exception("Invalid keywords!!")
        
        keywords = "+".join(jobs_keywords).replace(" ", "+")
        self.driver.set_window_size(1200,1000)
        path = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&includeNoSalaryJobs=false&typedKeyword="+keywords+"&sc.keyword="+keywords+"&locT=&locId=&jobType="
        self.driver.get(path)
        # time.sleep(2)
        jobs = []
        count = 0
        
        #for detecting if we reached the last page
        finished = False
        current_page = 1
        
        while len(jobs) < jobs_num or finished:
            time.sleep(3)
            self.__skip_signup()
            job_buttons = self.driver.find_elements_by_class_name("jl")
            # print(job_buttons, len(job_buttons))
            page_max = self.driver.find_element_by_xpath('//*[@id="ResultsFooter"]/div[1]').text
            page_max = int(page_max.split(" of ")[1])
            for j in job_buttons:
                if len(jobs) >= jobs_num: break
                count += 1
                print("progress {} of {}".format(len(jobs) + 1, jobs_num))
                try:
                    j.click()
                except:
                    continue
                
                time.sleep(1)
                collected_successfully = False
            
                while not collected_successfully:
                    try:
                        company_name = self.driver.find_element_by_xpath('.//div[@class="employerName"]').text
                        location = self.driver.find_element_by_xpath('.//div[@class="location"]').text
                        job_title = self.driver.find_element_by_xpath('.//div[contains(@class, "title")]').text
                        job_description = self.driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
                        collected_successfully = True
                    except:
                        time.sleep(5)
                        continue
    
                try:
                    salary_estimate = self.driver.find_element_by_xpath('//*[@id="HeroHeaderModule"]/div[3]/div[1]/div[4]/span').text
                except NoSuchElementException:
                    salary_estimate = -1 #You need to set a "not found value. It's important."
                    #here I only want a data with salary estimate, skips the rest
                    collected_successfully = True
                    continue
                try:
                    rating = self.driver.find_element_by_xpath('.//span[@class="rating"]').text
                except NoSuchElementException:
                    rating = -1 #You need to set a "not found value. It's important."
    

                try:
                    self.driver.find_element_by_xpath('.//div[@class="tab" and @data-tab-type="overview"]').click()
    
                    try:

                        headquarters = self.driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
                    except NoSuchElementException:
                        headquarters = -1
    
                    try:
                        size = self.driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                    except NoSuchElementException:
                        size = -1
    
                    try:
                        founded = self.driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                    except NoSuchElementException:
                        founded = -1
    
                    try:
                        type_of_ownership = self.driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
                    except NoSuchElementException:
                        type_of_ownership = -1
    
                    try:
                        industry = self.driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                    except NoSuchElementException:
                        industry = -1
    
                    try:
                        sector = self.driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                    except NoSuchElementException:
                        sector = -1
    
                    try:
                        revenue = self.driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
                    except NoSuchElementException:
                        revenue = -1
    
                    try:
                        competitors = self.driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
                    except NoSuchElementException:
                        competitors = -1
    
                except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
                    headquarters = -1
                    size = -1
                    founded = -1
                    type_of_ownership = -1
                    industry = -1
                    sector = -1
                    revenue = -1
                    competitors = -1
    
                jobs.append({"Job Title" : job_title,
                "Salary Estimate" : salary_estimate,
                "Job Description" : job_description,
                "Rating" : rating,
                "Company Name" : company_name,
                "Location" : location,
                "Headquarters" : headquarters,
                "Size" : size,
                "Founded" : founded,
                "Type of ownership" : type_of_ownership,
                "Industry" : industry,
                "Sector" : sector,
                "Revenue" : revenue,
                "Competitors" : competitors})
                #add job to jobs

            if current_page >= page_max:
                finished = True
                break
            try:
                current_btn = self.driver.find_element_by_xpath('.//li[@class="next"]//a')
                current_page += 1
                current_btn.click()
                time.sleep(1)
            except NoSuchElementException:
                print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(jobs_num, len(jobs)))
                break
    
        return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.
                
        
        
    def __skip_signup(self):
        try:
            self.driver.find_element_by_class_name("selected").click()
        except ElementClickInterceptedException:
            pass
        
        try:
            exit_btn = self.driver.find_element_by_xpath('//*[@id="JAModal"]/div/div[2]/span')
            self.driver.execute_script("arguments[0].click();", exit_btn)
        except NoSuchElementException:
            pass
        time.sleep(1)


        
