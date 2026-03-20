# Part 2 - Thought Exercise

**Q1:** The size of the URL list could grow infinitely. How might you scale this beyond the memory capacity of the system? 

Initially I thought about swapping SQLite (for testing) to PostgreSQL for production but considering that the URL list could grow “infinitely” then DynamoDB would be a better fit since it has better response times and can handle billions of rows. 

**Q2:** Assume that the number of requests will exceed the capacity of a single system, describe how might you solve this, and how might this change if you have to distribute this workload to an additional region, such as Europe. 

Since the app lives in a container, I would run it in an EKS cluster, a managed Kubernetes service in AWS with managed node groups which will scale automatically based on load. 
To distribute workload to Europe I would create another EKS cluster in that region and redirect European users to that region using Route 53. In this scenario we’d have to use DynamoDB Global Tables to serve both regions. 

**Q3:** What are some strategies you might use to update the service with new URLs? Updates may be as much as 5 thousand URLs a day with updates arriving every 10 minutes.

We can use bulk inserts in DynamoDB with batches of up to 25 inserts in parallel. 
A solution would be sending the 5k urls to an S3 bucket. A lambda function will put them in an SQS queue. Another Lambda function will take batches of 25 urls from the SQS queue and send the inserts to the DynamoDB table. I have an example of a serverless app that uses this decoupling concept with retries: https://github.com/victorhponcec/portfolio-3tier-serverless-pbc/blob/main/README.md

**Q4:** You’re woken up at 3am, what are some of the things you’ll look for in the app?

Since I mentioned that I would use EKS and managed node groups, I would create a secondary node group to run the observability tools like the kube-prometheus-stack that includes everything to monitor the EKS cluster. 
Additionally to infrastructure issues, I’d look to latency spikes and errors codes. 

**Q5:** Does that change anything you’ve done in the app?

Yes, as mentioned in the previous question I’d use Prometheus and OpenTelemetry for tracing.

**Q6:** What are some considerations for the lifecycle of the app?

In EKS we can configure the parameter terminationGracePeriodSeconds to let the app time to finish processing. 
For DynamoDB we can add TTL to the registries to let them expire after a certain period of time. 

**Q7:** You need to deploy a new version of this application. What would you do?

For this In EKS we can use a Canary release, where we run a new version of the app alongside the current version. We can start with a few pods of the new version and monitor with Prometheus and OpenTelemetry. We can use Argo Rollouts to distribute the load between current and new versions until the new version reaches 100%. 
