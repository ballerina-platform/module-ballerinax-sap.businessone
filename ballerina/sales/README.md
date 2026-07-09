## Overview

[SAP Business One](https://www.sap.com/products/erp/business-one.html) is an enterprise resource planning (ERP)
solution designed for small and midsize businesses by SAP SE.

The SAP Business One Sales (A/R) connector provides APIs for the sales (A/R) documents of SAP Business One: quotations, orders, deliveries, returns, invoices, credit memos, and dunning, exposed through the [SAP Business One Service Layer](https://help.sap.com/doc/056f69366b5345a386bb8149f1700c19/10.0/en-US/Service%20Layer%20API%20Reference.html) (OData).

### Key Features

- Create, read, update, close, and cancel sales documents
- Work with document lines, expenses, and serial/batch allocations
- Manage blanket agreements and sales tax invoices
- Drive document flows such as order-to-invoice

## Setup guide

The connector requires an SAP Business One installation with the Service Layer component enabled.

To connect, you need three values from the SAP Business One desktop client's login screen: the company database,
your user name, and your password.

Click the company name at the top of the SAP Business One desktop application, or contact your administrator.

![SAP Business One Choose Company window showing the User ID, Password, and Database fields used to configure the connection](../../docs/resources/images/sap-b1-choose-company.png)

The Service Layer endpoint follows the pattern `https://<host>:50000/b1s/v1`.

## Quickstart

To use the `sap.businessone.sales` connector in your Ballerina application, modify the `.bal` file as follows:

### Step 1: Import the module

```ballerina
import ballerinax/sap.businessone.sales;
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

sales:Client b1Client = check new (
    {companyDb, username, password},
    serviceUrl = serviceUrl
);
```

### Step 3: Invoke the connector operation

```ballerina
sales:Orders_CollectionResponse response = check b1Client->ordersList();
```

### Step 4: Run the Ballerina application

```bash
bal run
```

## Examples

The SAP Business One connectors provide practical examples illustrating usage in various scenarios. Explore these
[examples](https://github.com/ballerina-platform/module-ballerinax-sap.businessone/tree/main/examples), covering
use cases like listing open sales orders, reporting inventory stock, and logging CRM activities.
