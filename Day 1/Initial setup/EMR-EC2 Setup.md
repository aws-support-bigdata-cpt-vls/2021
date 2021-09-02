# Environment setup

1. Switch the region to eu-west-1 - Ireland.

![console0.png](./resources/Console0.PNG)

2. Download the CloudFormation template [here](https://raw.githubusercontent.com/aws-support-bigdata-cpt-vls/2021/main/Day%201/Initial%20setup/vls-cpt-sep-cfn-one.yaml).
3. Search for CloudFormation on the service list.

![console1.png](./resources/Console1.PNG)

4. Select "Create stack".

![console2.png](./resources/Console2.PNG)

5. Select the template downloaded in step 2 above and click Next.

![console3.png](./resources/Console3.PNG)

6. Provide the stack as below and click Next.

![console4.png](./resources/Console4.PNG)

7. Scroll down and click Next.

![console5.png](./resources/Console5.PNG)

8. Acknowledge the creation of IAM Roles and create the stack.

![console6.png](./resources/Console6.PNG)

9. Environment creation is initiated.

![console7.png](./resources/Console7.PNG)

10. Once the stack has finished creating, search for EMR from the service list, navigate to the EMR page and click on the Clusters >> Select your cluster >> Hardware tab >> Master Instance group:

![console8.png](./resources/Console8.PNG)

11. Click the master instance to navigate to the EC2 Console:

![console9.png](./resources/Console9.PNG)

12. To connect to the instance, we use Session Manager. Click the check box and click connect:

![console10.png](./resources/Console10.PNG)

13. Select the Session Manager tab and click connect:

![console11.png](./resources/Console11.PNG)

14. Change user to Hadoop for the EMR Cluster (sudo su - hadoop) or ec2-user (sudo su - ec2-user) for the EC2 instance as below.

![console12.png](./resources/Console12.PNG)

