# JobCat

JobCat keeps your application information organized and easy to access. It automatically scans and summarizes your job application status directly from your email inbox. It tracks the company, position, mode (remote, onsite, etc.), location, salary, application date, status (interview, offer, rejected, etc.), and job description for a job application.

## Installation 

Clone the repo.

Install dependencies:

```bash
`pip install -r requirements.txt`.
`pip install -r ai\requirements.txt`.
```

Migrate your database:

```bash
reflex db makemigrations
reflex db migrate
```

Run App:
```bash
reflex run
```

