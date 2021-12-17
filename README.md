# Database Migration Assistant (DMA) for Azure Cosmos DB API for MongoDB

## About Database Migration Assistant (DMA)
Database Migration Assistant assists you through the pre-migration stage while migrating MongoDB workloads from self-hosted or Atlas instances to Azure Cosmos DB API for MongoDB by -

- Gathering source environment info
- Gathering source workload info and creating a data estate spreadsheet
- Running assessment for incompatibilities and warnings.


Details gathered by the migration assistant currently include:

- Source environment info: MongoDB version, License Type, IsSharded and Shards list.
- Source workload info at database level: Database names, Collection counts, Doc count, Average document size, Data size, Index count and Index size.
- Source workload info at collection level: Database Name, Collection Name, Doc count, Average document size, Data size, Index count, Index size and Index definitions.

These details are printed as an output in the notebook as well as saved to csv files - *environment_info.csv*, *workload_database_details.csv* and *workload_collection_details.csv*.

Once the above details are gathered, DMA runs assessment on the gathered workload info. \
Assessments run by the migration assistant currently include:

- Unsupported features: Text index
- Partially supported features: Unique index only allowed on empty collection, Compound/Unique indexes with nested fields only allowed on nested doc fields and not arrays, TTL index only supported on _ts field
- Limit warnings: Unsharded collection reaching fixed collection limit, Databases with >25 collections are not recommended for shared database throughput setting.

Assessment results are printed as an output in the notebook as well as saved to csv file - *assessment_result.csv* 

**Note**:

- DMA does not modify any of the existing configuration, databases, collections or index, it only reads the environment info and workload stats.
- No data is automatically uploaded or sent to Microsoft at any step in the DMA notebook. The credentials you enter will only be used locally on your machine. \
You can manually review the final DMA_output.zip file prior to sharing it with Microsoft representatives.

## How to run the DMA

### Pre-requisites

- Git
- Python 3 (will be prompted for installation if not already available)
- The client machine from where you are running DMA should have access to the source MongoDB endpoint either over private or public network over the specified IP or hostname.

### Setup steps

- Download and install [Azure Data Studio](https://docs.microsoft.com/en-us/sql/azure-data-studio/download-azure-data-studio?view=sql-server-ver15) on the machine.
- Clone the [DMA repo](https://github.com/AzureCosmosDB/Cosmos-DB-Migration-Assistant-for-API-for-MongoDB.git) locally on the machine. You can even do this from Azure Data Studio (ADS) as below by entering the repo url and clicking "Clone from URL"
![Clone Cosmos DB DMA repo](/images_for_setup_doc/dma_clone_repo.jpg "Clone DMA repo")
- Once done, click on open repository and click ADS Notebooks icon on the left, that should bring up the Jupyter Notebook *database_migration_assistant.ipynb*.
- When the notebook opens, you will be asked to choose the Python runtime. At this point you can either perform fresh install of python or choose an existing path. On the next step, will also be prompted to install 'jupyter' package. Proceed with the selection/installation.
![Select Python runtime](/images_for_setup_doc/python_runtime.jpg "Select python runtime")
- You would need to install additional dependencies by clicking on 'Manage packages' as below:
![Manage packages](/images_for_setup_doc/manage_packages.jpg "Manage packages")
- Here click on 'Add new' and install packages *pymongo*, *pandas*, *dnspython*. Wait until the installation for these packages has completed in the terminal.
![Add packages](/images_for_setup_doc/add_packages.jpg "Add packages")

### Running the DMA Notebook

- The notebook would be ready to run when the kernel 'Python 3' and attach to 'localhost' are showing up correctly as below. Also mark the notebook as 'trusted':
![Ready to run](/images_for_setup_doc/notebook_ready.jpg "Notebook is ready to run")
- In the first cell, update the *source_connection_string* parameter with the MongoDB source endpoint connection string in the format **mongodb://username:password@hostnameOrIP:port/** or
**mongodb+srv://username:password@hostname/**. \
The username used should be that of a *clusteradmin* role that would have access to the server info and all databases, collections in the source environment.\
The hostname or IP should be one either privately or publicly accessible from the client machine.
- Then run the cells one by one or click "Run cells" on top of the notebook.

## How to use the DMA output

DMA creates 4 output files - *environment_info.csv*, *workload_database_details.csv*, *workload_collection_details.csv* and *assessment_result.csv*. It also zips together these outputs into DMA_output.zip file.

- Use the assessment results output from the notebook or the assessment_results.csv to determine changes or work-arounds you need to do during the migration.
- Use the workload_collection_details.csv and/or workload_database_details.csv as you data estate spreadsheet for planning and tracking the migration further.
You may add additional columns to this sheet such as 'shard key', 'throughput setting', 'shared or dedicated throughput', 'migration method', 'migration status', 'migration date', etc to help with the planning and tracking as needed.
- If you have been in touch with Microsoft points of contact regarding the migration, share the DMA_output.zip file with them to help with the discussion.
