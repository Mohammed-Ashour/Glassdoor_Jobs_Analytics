

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

jobs.to_csv("./salaries_cleaned.csv")