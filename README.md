# Softsensor_MVP_with_EDDI
This repository provides code example for for using [EDDI in multivariate time-series missing value imputation (MVP)](https://techcommunity.microsoft.com/t5/ai-customer-engineering-team/fill-the-gap-eddi-for-multivariate-time-series-missing-value/ba-p/3289782) in use cases like Soft Sensor Modeling.

Please refer to the corresponding blog post, [Fill the Gap: Eddi for Multivariate Timeseries Missing Value Imputation](https://techcommunity.microsoft.com/t5/ai-customer-engineering-team/fill-the-gap-eddi-for-multivariate-time-series-missing-value/ba-p/3289782), for more informaiton and concrete explanation of the use case and best practices.


## Background on EDDI
Microsoft's research team at Cambridge developed a technology based on a partial VAE algorithm [6], allowing Missing Value Prediction by using probabilistic Deep Learning. The code is [open source](https://github.com/microsoft/project-azua) as a part of the [Data-Efficient Decision-Making project](https://www.microsoft.com/en-us/research/project/project_azua). The team also developed an easy-to-use API, which is currently in private preview. If you are interested in evaluating the API for your scenario, please email the team at azua-request@microsoft.com. 

## Code Structure
This repository contains code samples for using EDDI API for Soft Sensor Modeling using SaaS and code base experience: 

- The code template for using EDDI as a service (SaaS: Software as a Service) experience is in [eddi_azure_saas](https://github.com/mry-tvk/Softsensor_MVP_with_EDDI/tree/main/eddi_azure_saas) directory. 

- The code template for using EDDI API through Data-Efficient Decision-Making code base [4] is placed in [eddi_azua_repo](https://github.com/mry-tvk/Softsensor_MVP_with_EDDI/tree/main/eddi_azua_repo) directory. 

## References

### Related Blogs:
For more information on the following topics, please refer to the corresponding blog post:

[1] Best practices for EDDI in Multivariate Timeseries: [Fill the Gap: Eddi for Multivariate Timeseries Missing Value Imputation](https://techcommunity.microsoft.com/t5/ai-customer-engineering-team/fill-the-gap-eddi-for-multivariate-time-series-missing-value/ba-p/3289782)

[2] Soft sensor modeling: [A Solution Template for Soft Sensor Modeling on Azure](https://techcommunity.microsoft.com/t5/ai-customer-engineering-team/a-solution-template-for-soft-sensor-modeling-on-azure/ba-p/3265959)

[3] Using EDDI for Next Best Question: [Using AI to know which question to ask, and when to ask it](https://techcommunity.microsoft.com/t5/ai-customer-engineering-team/using-ai-to-know-which-question-to-ask-and-when-to-ask-it/ba-p/2768799)

### Related Git-Repo:
[4] Data-Efficient Decision-Making Project repository: https://github.com/microsoft/project-azua

[5] A Solution Template for Soft Sensor Modeling on Azure: https://github.com/vilcek/Soft_Sensors_on_Azure

### Related Paper:
Please refer to the original paper for more technical explanation on EDDI model. Also, if you are using EDDI model through this code base, please consider citing the following paper:

[6] (PVAE and information acquisition) Chao Ma, Sebastian Tschiatschek, Konstantina Palla, Jose Miguel Hernandez-Lobato, Sebastian Nowozin, and Cheng Zhang. "EDDI: Efficient Dynamic Discovery of High-Value Information with Partial VAE." In International Conference on Machine Learning, pp. 4234-4243. PMLR, 2019.
