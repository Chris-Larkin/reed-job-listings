# reed-scraper
This program scrapes and cleans job listings data from reed.co.uk for a given day. It extracts: 

```applications_ten``` -> whether there have been ten or fewer applicants
```job_country``` -> country where the job is located
```job_description``` -> free text description of the job provided by the poster
```job_locality``` -> city/town where the job is located
```job_postcode``` -> postcode for where the job is located
```job_region``` -> region where the job is located
```job_type``` -> full-time, part-time, temporary, contract, etc.
```job_type_disp``` -> job type as displayed to applicants
```link``` -> URL to the job listing
```salary_disp``` -> salary as displayed to the applicant
```salary_max``` -> maximum salary
```salary_min``` -> minimum salary
```salary_time``` -> time unit over which salary is reported (hourly, monthly, yearly)

It outputs a pandas data frame called reed_data.
