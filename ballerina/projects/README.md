## Overview

[SAP Business One](https://www.sap.com/products/erp/business-one.html) is an enterprise resource planning (ERP)
solution designed for small and midsize businesses by SAP SE.

The SAP Business One Project Management connector provides APIs for the project management objects of SAP Business One: projects, project management entities, and time sheets, exposed through the [SAP Business One Service Layer](https://help.sap.com/doc/056f69366b5345a386bb8149f1700c19/10.0/en-US/Service%20Layer%20API%20Reference.html) (OData).

### Key Features

- Manage financial project codes and project management projects
- Track project stages, phases, and tasks
- Record project time sheets

## Setup guide

The connector requires an SAP Business One installation with the Service Layer component enabled (available for
SAP Business One, version for SAP HANA, and SAP Business One on Microsoft SQL Server 9.3 PL10+). The Service Layer
endpoint is `https://<host>:50000/b1s/v1` by default. A Business One user with a license and the relevant object
authorizations is needed; sessions are opened against a specific company database (schema).

## Quickstart

To use the `sap.businessone.projects` connector in your Ballerina application, modify the `.bal` file as follows:

### Step 1: Import the module

```ballerina
import ballerinax/sap.businessone.projects;
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

projects:Client b1Client = check new (
    {companyDb, username, password},
    serviceUrl = serviceUrl
);
```

### Step 3: Invoke the connector operation

```ballerina
projects:ProjectManagements_CollectionResponse response = check b1Client->projectManagementsList();
```

### Step 4: Run the Ballerina application

```bash
bal run
```

## Examples

The SAP Business One connectors provide practical examples illustrating usage in various scenarios. Explore these
[examples](https://github.com/ballerina-platform/module-ballerinax-sap.businessone/tree/main/examples), covering
use cases like listing open sales orders, reporting inventory stock, and logging CRM activities.
