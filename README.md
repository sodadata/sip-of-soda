# Take a sip of Soda

The content of this repository supports the onboarding tutorial and guides in [Soda documentation](https://docs.soda.io). <br />
Access the [Take a sip of Soda](https://docs.soda.io/soda/quick-start-sip.html) tutorial to use the example data in this repo to set up and run a simple Soda scan for data quality.


## Build the example data source

Refer to the full instructions in the [Take a sip of Soda](https://docs.soda.io/soda/quick-start-sip.html) tutorial.

To enable you to take a first sip of Soda, you can use Docker to quickly build an example PostgreSQL data source against which you can run scans for data quality. The example data source contains data for AdventureWorks, an imaginary online e-commerce organization.

1. Clone this repo locally. Use Terminal to navigate to the newly-cloned repo in your local environment.
2. If it is not already running in your local environment, start Docker.
3. In Terminal, run the following command to set up the prepared example data source.
`docker-compose up`
4. When the output reads `data system is ready to accept connections`, your data source is set up and you are ready to proceed with the [tutorial](https://docs.soda.io/soda/quick-start-sip.html).


## What is Soda?

Soda is a platform that enables Data Engineers to test data for quality where and when they need to.

Is your data fresh? Is it complete or missing values? Are there unexpected duplicate values? Did something go wrong during transformation? Are all the data values valid? These are the questions that Soda answers for Data Engineers. [Read more.](https://docs.soda.io/soda/product-overview.html)

* Learn how to add Soda data quality checks to your [CI/CD workflow](https://docs.soda.io/soda/quick-start-dev.html).
* Learn how to add Soda data quality checks to your [data pipeline](https://docs.soda.io/soda/quick-start-prod.html) after ingestion and transformation.
* Learn how to [set up Soda](https://docs.soda.io/soda/quick-start-end-user.html) to empower Data Analysts and Scientists to write their own checks for data quality.


Need help? Join the [Soda community](https://community.soda.io/slack) on Slack.