# AWS RAG with Bedrock and Knowledge Base - [Source](https://aws.amazon.com/blogs/machine-learning/elevate-rag-for-numerical-analysis-using-amazon-bedrock-knowledge-bases/)

In an effort to deepen understanding of AI and explore the wide range of AWS services, Dajani has taken on a challenge set by the California Department of Finance. This challenge is aimed at building internal knowledge and developing practical tools to support California agencies in adopting AI smoothly and effectively.

## CHALLENGE 2

Identify statewide efficiency opportunities through budget change proposal analysis Finance must review, analyze, and evaluate hundreds of budget change proposals (BCPs) each year. A state entity submits one BCP for each problem it is requesting funds to solve, and every BCP includes analysis and justification with both narrative and numerical data. How might Finance extract and leverage the data in all BCPs submitted in a given amount of time (e.g., current fiscal year, past 3 fiscal years) to:

- Gain robust insights about statewide funding and staffing needs (e.g., by agency/department, by program area, by policy area);
- Forecast potential areas of program development and staffing needs;
- Draw connections and trends between and across BCPs that aren’t readily apparent; and,
- Support the best value of the state’s investments through identifying opportunities for shared services (versus funding individual BCPs that may solve similar problems)?

Finance is particularly interested in hearing about solutions that use GenAI. This solution must serve as a support to the “human in the loop,” enabling analysts’ depth of work but not replacing a person.

### Resources and data

- [Department of Finance historical Budget Change Proposals library](https://bcp.dof.ca.gov/viewBcp.html)
- [How to write an effective budget change proposal](https://dof.ca.gov/budget/how-to-write-an-effective-budget-change-proposal-bcprev-03-00/)

## Implementation approach

When we began analyzing this problem, we explored several approaches to tackle the challenge effectively.

The first approach, using a traditional method, involved reading and extracting data from PDFs to transform unstructured information into a structured format, enabling better reporting and search capabilities. However, we encountered significant challenges with this method: across different fiscal years, the Budget Change Proposal (BCP) layouts, formats, and labels varied widely, making data extraction increasingly complex.

Another approach involved experimenting with [Amazon Q Business](https://docs.aws.amazon.com/amazonq/latest/qbusiness-ug/what-is.html), using S3 as an external data source. While we tested this with a sample of BCPs, it became evident that Amazon Q Business primarily provided semantic search capabilities. It struggled to interpret numerical data embedded within tables in the PDFs, limiting its effectiveness for our needs.

The most successful approach has been utilizing [AWS Bedrock with Knowledge Base](https://aws.amazon.com/bedrock/knowledge-bases/), which supports Retrieval-Augmented Generation (RAG). RAG has proven effective for this application, though it also has challenges, especially with numerical analysis in complex, nested tables. Fortunately, recent innovations in Amazon Bedrock Knowledge Base have introduced solutions to address these issues, making it a viable option for our project.

As part of [AWS Blogs](https://aws.amazon.com/blogs/machine-learning/) we found a really useful one that seemed to align with our proof of concept. ([Here you can checkout the details](https://aws.amazon.com/blogs/machine-learning/elevate-rag-for-numerical-analysis-using-amazon-bedrock-knowledge-bases/https:/)).

This is the solution overview at a high level.

![](https://d2908q01vomqb2.cloudfront.net/f1f836cb4ea6efb2a0b1b99f41ad8b103eff4b59/2024/09/13/image001-5.png)

The user call flow consists of the following steps:

1. The process begins with the user uploading one or more documents. This action initiates the workflow.
2. The Streamlit application, which designed to facilitate user interaction, takes these uploaded documents and stores them in an [Amazon Simple Storage Service](http://aws.amazon.com/s3) (Amazon S3) bucket.
3. After the documents are successfully copied to the S3 bucket, the event automatically invokes an [AWS Lambda](http://aws.amazon.com/lambda)
4. The Lambda function invokes the Amazon Bedrock knowledge base API to extract embeddings—essential data representations—from the uploaded documents. These embeddings are structured information that capture the core features and meanings of the documents.
5. With the documents processed and stored, the GUI of the application becomes interactive. Users can now engage with the application by asking questions in natural language through the user-friendly interface.
6. When a user submits a question, the application converts this query into query embeddings. These embeddings encapsulate the essence of the user’s question, which helps with retrieving the relevant context from the knowledge base.
7. you can use the Retrieve API to query your knowledge base with information retrieved directly from the knowledge base. The [RetrieveAndGenerate](https://aws.amazon.com/bedrock/knowledge-bases/) API uses the retrieved results to augment the foundation model (FM) prompt and returns the response.
8. Using a hybrid search method that combines keyword-based and semantic-based techniques, the application searches its knowledge base for relevant information related to the user’s query. This search aims to find contextual answers that match both the explicit terms and the intended meaning of the question.
9. When relevant context is identified, the application forwards this information—both the user’s query and the retrieved context—to the LLM module.
10. The LLM module processes the provided query and context to generate a response.
11. The application delivers the generated response back to the user through its GUI. This completes the loop of interaction, where the user’s initial query results in a comprehensive and contextually relevant response derived from the uploaded documents and the application’s knowledge base.
