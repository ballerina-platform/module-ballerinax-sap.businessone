## Overview

[SAP Business One](https://www.sap.com/products/erp/business-one.html) is an enterprise resource planning (ERP)
solution designed for small and midsize businesses by SAP SE.

The SAP Business One Business Partners connector provides APIs for the business partner master data of SAP Business One: customers, vendors, leads, contacts, and related setup, exposed through the [SAP Business One Service Layer](https://help.sap.com/doc/056f69366b5345a386bb8149f1700c19/10.0/en-US/Service%20Layer%20API%20Reference.html) (OData).

### Key Features

- Create, read, update, and delete business partners
- Manage contact persons and business partner groups
- Maintain payment terms, priorities, and industries

## Setup guide

The connector requires an SAP Business One installation with the Service Layer component enabled.

To connect, you need three values from the SAP Business One desktop client's login screen: the company database,
your user name, and your password.

Click the company name at the top of the SAP Business One desktop application, or contact your administrator.

![SAP Business One Choose Company window showing the User ID, Password, and Database fields used to configure the connection](https://raw.githubusercontent.com/ballerina-platform/module-ballerinax-sap.businessone/main/docs/resources/images/sap-b1-choose-company.png)

The Service Layer endpoint follows the pattern `https://<host>:50000/b1s/v1`.

## Quickstart

To use the `sap.businessone.businesspartners` connector in your Ballerina application, modify the `.bal` file as follows:

### Step 1: Import the module

```ballerina
import ballerinax/sap.businessone.businesspartners;
```

### Step 2: Instantiate a new connector

The connector authenticates with the Service Layer session protocol: it logs in with the configured company
database, user name, and password, tracks the `B1SESSION`/`ROUTEID` cookies, and transparently re-logs in once
when the session expires. Place the credentials in a `Config.toml` (never commit credentials to source control):

```toml
serviceUrl = "https://<host>:50000/b1s/v1"
companyDb = "<COMPANY_DB>"
username = "<USER>"
password = "<PASSWORD>"
```

```ballerina
configurable string serviceUrl = ?;
configurable string companyDb = ?;
configurable string username = ?;
configurable string password = ?;

businesspartners:Client b1Client = check new (
    {companyDb, username, password},
    serviceUrl = serviceUrl
);
```

### Step 3: Invoke the connector operation

```ballerina
businesspartners:BusinessPartners_CollectionResponse response = check b1Client->businessPartnersList();
```

### Step 4: Run the Ballerina application

```bash
bal run
```

## Examples

The SAP Business One connectors provide practical examples illustrating usage in various scenarios. Explore these
[examples](https://github.com/ballerina-platform/module-ballerinax-sap.businessone/tree/main/examples), covering
use cases like listing open sales orders, reporting inventory stock, and logging CRM activities.
