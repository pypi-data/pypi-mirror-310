# GenAI REST Builder

The **GenAI REST Builder** is a tool for creating RESTful services around AI models with minimal effort. It allows you to define service configurations in a YAML file and generates a FastAPI-based project structure to deploy AI-powered endpoints.

---

## **Version History**

### **v0.2.2 - AWS Chat-Based Service with Memory Management**

#### **Key Features**
- Introduced **chat-based services** for AWS with memory management using **DynamoDB**.
- Added `chatApp` property, available only for AWS services:
  - Set `chatApp: Y` to enable chat-based functionality.
  - Requires the `dynamoDbTableName` property to specify the DynamoDB table used for storing chat histories.
  - Removes the need for the `prompt` property when `chatApp` is `Y`.
- **DynamoDB Integration**:
  - Table must have a primary key of `SessionId` (string).
  - Stores and retrieves chat histories linked to session IDs.

#### **YAML Format**
```yaml
PromptServices:
  - <service_name>:
      chatApp: Y  # Available only for AWS services
      dynamoDbTableName: <DynamoDB_Table_Name>  # Required when chatApp is Y
      model:
        provider: aws
        modelId: <model_id>
        temperature: <value>
        maxTokens: <value>
```

If `chatApp` is omitted or its value is not `Y`, the `prompt` property becomes mandatory.

---

### **v0.2.1 - Core Features**

#### **Key Features**
- Introduced foundational functionality to define RESTful services using YAML configuration.
- Added support for **custom prompts** via the `prompt` property.
- Supported **AWS** and **Azure** providers for model integration.
- Automated **FastAPI-based project generation**.
- Introduced the `apiVersion` property for Azure-specific models.

#### **YAML Format**
```yaml
PromptServices:
  - <service_name>:
      chatApp: N  # Optional; default behavior for prompt-based services
      prompt: <prompt_template>  # Required if chatApp is omitted or not Y
      model:
        provider: [aws/azure]
        modelId: <model_id>
        temperature: <value>
        maxTokens: <value>
        apiVersion: <api_version>  # Azure only
```

---

## **Installation Instructions**

### 1. Install the Builder
```bash
pip install pyyaml genai-rest-builder
```

### 2. Generate Project Structure
```bash
genai-rest-proj-build
```
- Reads from the `prompt_service.yaml` file to generate project files.

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Server
```bash
python serve_app.py
```
- Default host: `localhost:8080`.

---

## **Generated Project Structure**
The project structure remains consistent across versions:

```
.  
├── service_chains/  
│   ├── base_chains/                     # Base and provider-specific chain definitions  
│   │   ├── base_chain.py                # Abstract base class for chains  
│   │   ├── aws_chain.py                 # AWS-specific chain implementation  
│   │   ├── azure_chain.py               # Azure-specific chain implementation  
│   │   ├── __init__.py                  # Exports for base_chains module  
│   ├── <servicename>_chain.py           # Service-specific chain implementation  
│   ├── utils.py                         # Utility functions for service configurations  
│   ├── __init__.py                      # Package initialization file for service_chains  
├── serve_app.py                         # Main FastAPI application  
├── .env                                 # Environment configuration file with host/port settings  
├── requirements.txt                     # Project dependencies file  
├── prompt_service.yaml                  # YAML configuration file (user-defined)  
```

---

## **Accessing API Documentation**
Once the server is running, OpenAPI documentation can be accessed at:

```
http://<GENAI_SERVER_HOST>:<GENAI_SERVER_PORT>/docs
```

---

## **Invoking Services**
Each service is available via a unique REST API path based on its name in `prompt_service.yaml`:

```
http://<GENAI_SERVER_HOST>:<GENAI_SERVER_PORT>/<service_name>
```

---

## **Upgrade Notes**

### **From v0.2.1 to v0.2.2**
- **For AWS Services**:
  - Use `chatApp: Y` to enable chat-based services.
  - Provide `dynamoDbTableName` to store message histories.
  - If `chatApp` is `Y`, the `prompt` property is no longer required.
- **For Azure Services**:
  - Continue using `prompt` as required for prompt-based services.
  - Ensure the `apiVersion` property is provided for Azure models.
- **General Rule**:
  - If `chatApp` is omitted or not set to `Y`, the `prompt` property must be included.