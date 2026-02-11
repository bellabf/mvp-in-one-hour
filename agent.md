GOAL: refactor meal_planner.ipynb to be a python script. 


1) Divide the script in reusable parts.

---> get client should be configurable (different models for each different call i.e. the one that makes the shopping can use different model from the ones that make the meal planner)
--> divide the pydantic into a separate file.


2) Create a list of tests in a new file called test.py