import pandas as pd

jobs = pd.read_csv("./jobs_clean.csv")

                    
#cleaning company name
jobs["Company Name"] = jobs["Company Name"].apply(lambda x : x[:-3])

#remove duplicates
# jobs.drop_duplicates(keep="first", inplace=True)
#avg salary
jobs = jobs[jobs["Salary Estimate"] != "-1"]
salaries = jobs["Salary Estimate"]
salaries = salaries.apply(lambda x : x.split("\n(")[0].replace("K", "").replace("$",""))
min_sal, max_sal = salaries.apply( lambda x : x.split("-")[0]),\
                    salaries.apply(( lambda x: x.split("-")[1]))
jobs["min_salary"], jobs["max_salary"] = min_sal.apply(lambda x : int(x)), max_sal.apply(lambda x : int(x))

jobs["avg_salary"] = (jobs["min_salary"] + jobs["max_salary"])/2
jobs["Size"] = jobs["Size"].apply(lambda x : x.replace(" employees",""))
jobs["Size"] = jobs["Size"].apply(lambda x : (int(x.split(" to ")[0]) + int(x.split(" to ")[1]))//2 \
                                  if "to" in x else x.replace("+", "") )
jobs["Size"] = jobs["Size"].apply(lambda x : int(x) if x != "Unknown" else 50 )
    
#company age

jobs["company_age"] = jobs["Founded"].apply(lambda x : 2020 - int(x) if x != -1 else x)
#if the offer to work in the headquarters
jobs["is_headquarters"] = jobs["Location"] == jobs["Headquarters"]
jobs["is_headquarters"] = jobs["is_headquarters"].apply(lambda x: 1 if x else 0)

jobs["Job Title"] = jobs["Job Title"].apply(lambda x : x.lower())
# jobs["seniority"] = jobs["title"]
def seniority(title):
    if "junior"in title or "jr" in title or "jr" in title or "jun" in title:
        return "jr"
    elif "ii" in title or "level 2" in title or "2" in title :
        return "mid-level"
    elif "senior" in title or "sr." in title or "sr" in title :
        return "sr"
    elif "lead" in title or "principal" in title or "staff" in title:
        return "lead"
    else: 
        return "not mentioned"
def clean_titles(title):

    if "data scientist" in title or "data science" in title:
        return "data scientist"
    elif "software engineer" in title:
        return "software engineer"
    elif "ml engineer" in title or "machine learning" in title or "deep learning" in title:
        return "ml engineer"
    elif "computer vision" in title:
        return "ml engineer"
    elif "data engineer" in title or "data management":
        return "data engineer"
    else:
        return title

jobs["seniority"] = jobs["Job Title"].apply(seniority)
jobs["Job Title"] = jobs["Job Title"].apply(clean_titles)
    
jobs["comp_num"] = jobs["Competitors"].apply(lambda x: len(x.split(",")) if x != "-1" else 0)
jobs.to_csv("./salaries_cleaned.csv")