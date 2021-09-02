# Environment setup

1. Switch the region to eu-west-1 - Ireland.

![console0.png](./resources/Console0.png)

2. Download the CloudFormation template [here](https://raw.githubusercontent.com/aws-support-bigdata-cpt-vls/2021/main/Day%201/Initial%20setup/vls-cpt-sep-cfn-one.yaml).
3. Search for CloudFormation on the service list.

![console1.png](./resources/Console1.png)

4. Select "Create stack".

![console2.png](./resources/Console2.png)

5. Select the template downloaded in step 2 above and click Next.

![console3.png](./resources/Console3.png)

6. Provide the stack as below and click Next.

![console4.png](./resources/Console4.png)

7. Scroll down and click Next.

![console5.png](./resources/Console5.png)

8. Acknowledge the creation of IAM Roles and create the stack.

![console6.png](./resources/Console6.png)

9. Environment creation is initiated.

![console7.png](./resources/Console7.png)

10. Once the stack has finished creating, search for EMR from the service list, navigate to the EMR page and click on the Clusters >> Select your cluster >> Hardware tab >> Master Instance group:

![console8.png](./resources/Console8.png)

11. Click the master instance to navigate to the EC2 Console:

![console9.png](./resources/Console9.png)

12. To connect to the instance, we use Session Manager. Click the check box and click connect:

![console10.png](./resources/Console10.png)

13. Select the Session Manager tab and click connect:

![console11.png](./resources/Console11.png)

14. Change user to Hadoop for the EMR Cluster (sudo su - hadoop) or ec2-user (sudo su - ec2-user) for the EC2 instance as below.

![console12.png](./resources/Console12.png)

