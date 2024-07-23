# Chunk Usage Guide and Prompt Templates

## Introduction

This guide provides examples and templates for using the chunked iOS project content with AI models. By following these templates, you can efficiently navigate and utilize the chunked content for various development tasks.

## General Usage Pattern

1. Start by loading the `index.md` file to understand the project structure.
2. Based on the task, determine which chunks you need to load.
3. Use the provided prompts to guide the AI in assisting you with your task.

## Use Cases and Prompts

### 1. Feature Implementation

#### Prompt Template:
```
I'm working on the following JIRA task: [TASK_NAME]

Based on this task, I need assistance in implementing a new feature. Please ask me which chunks of the project you need to see to help with this task. Once I provide the chunks, analyze them and guide me through the implementation process.
```

#### Example:
```
Human: I'm working on the following JIRA task: IOS-1234 Implement User Authentication

Based on this task, I need assistance in implementing a new feature. Please ask me which chunks of the project you need to see to help with this task. Once I provide the chunks, analyze them and guide me through the implementation process.

AI: Certainly! To assist you with implementing user authentication (JIRA task IOS-1234), I'll need to see relevant parts of your project. Could you please provide me with the following chunks:

1. Any existing authentication-related files (e.g., UserAuthentication_chunk_1.md, UserAuthentication_chunk_2.md, etc.)
2. The AppDelegate or SceneDelegate file chunks
3. Any existing user model or user data handling file chunks
4. The main view controller or initial screen file chunks

Once you provide these chunks, I'll analyze them and guide you through the implementation process. If there are any specific authentication methods or requirements mentioned in the JIRA task, please let me know as well.
