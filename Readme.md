# Building a Search engine Agent using Langgraph 

This repository contains concept and code for building Daily use AI Agents using langgraph and langchain from absolute basics.

## Why do I need to use these ? Can't I just access them in my browser ? 
Yes, to be honest these wont perform better than what you can access from your browser. This is not a production level Project. This is a fun project made with intention of playing around langgraph and langchain. Its a really fun project to take up. 


## Table of contents : 
### 1. Model file
### 2. Tools
### 3. Main
### 4. Prompt Template


## Model File : 
This file contains the code to load the local LLM, even though I later changes it to using Gemini 2.5-flash later using API calls, the code does not change much. 

## Tools File : 
This file contains the necessary tools required to be called and used by the model. We have used native tool calling. 
The available tools are : 
###        Search Engine Tool : 
Using DuckDuckGo to access information from internet and also obtain as much privacy as possible.  