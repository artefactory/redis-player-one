
# **Ask' Yves**
<div align="center">
    <a href="https://github.com/RedisVentures/redis-arXiv-search"><img src="assets/askyves.png" width="30%"><img></a>
    <br />
    <br />
<div display="inline-block">
    <a href="https://docsearch.redisventures.com"><b>Hosted Demo</b></a>&nbsp;&nbsp;&nbsp;
    <a href="https://github.com/RedisVentures/redis-arXiv-search"><b>Code</b></a>&nbsp;&nbsp;&nbsp;
  </div>
    <br />
    <br />
</div>

TODO: Clean image

Yves Saint Laurent was one of the greatest minds of french history. He spent a lot of time reading scientific papers on arXiv.

Ask him anything. He will have an answer. Probably not the right one, but you might be surprised 😅

## Getting Started

# TODO - How to use the app + Screenshots


## Contribute

## **TODO: Retrieve articles from Kaggle + setup Redis DB + Do the embeddings**

TODO

+ References of original redis demo repo

## **Run the app locally**

**1. Setup python environment:**

Run the following command to create a virtual environment and install all requirements:
```bash
make env
make install_requirements
```

**2. Fill credentials in environment:**

You'll need to export the following variables in your environment. Check `credentials/env.sh.exemple` to have the list of variables to fill:
```bash
export REDIS_HOST="redis_host_url"
export REDIS_PORT="1234"
export REDIS_DB="your-redis-database-name"
export REDIS_PASSWORD="redis-db-password"
```

**3. Run the app locally:**
To run the app in your local environment, just run the following command:
```bash
make run_app
```

It will open a Streamlit window on your web-browser:

# 
TO PUT: IMAGE OF BROWSER
#


## **Run the app on a Saturn Cloud Deployment instance**

You can easily create a deployment instance to run your app in Saturn Cloud by copying the recipe stored in the file `saturn-deployment-recipe.json` at the root of the project. Here is the instruction to create your own instance:

1. First, you'll need to parametrize your credentials in Saturn Cloud so your instance can access them. Go to "Secrets" > "New", and create a secret for the 4 credentials variables you exported earlier.

2. Then, go to "Resources" > "New Deployment" > "Use a Recipe", and paste the content of `saturn-deployment-recipe.json` in the open window. A deployment instance will be created with app parameters.

3. Finally, you'll need to add the credentials that are necessary to run your app. After creating the instance, select it in "Resources", then go to "Secrets" > "Attach Secret Environment Variable", and select in the dropdown menu the secrets you defined in step 1. Be sure to assign corresponding environment variable name to them.

4. Now you're ready to go! Click on "Overview" > "Start", and once the app is running, you can access it by clicking on the provided public URL.

Note: The deployment instance will directly pull the main branch of this repo to run the app with, but you can modify the branch it pulls by modifying it in "Git Repos" section. 


### Interested in contributing?
This is a new project. Comment on an open issue or create a new one. We can triage it from there.


### Next steps
# TODO
