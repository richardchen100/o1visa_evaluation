Approach 1: one task to query all results
- **Set up endpoint**: Run `uvicorn main1go:app --reload `.
- **Example of sending a CV file to the endpoint**: Run `python testfileupload.py`， two examples of CV are included in the files.
- **Test run withou the end point**: Run `python test_crew1go` for testing locally outputing all results in one go.



Approach 2: separate tasks for each eligibility item
- **Set up endpoint**: Run `uvicorn main:app --reload `.
- **Example of sending a CV file to the endpoint**: Run `python testfileupload.py`， two examples of CV are included in the files.
- **Test run withou the end point**: Run `python test_crew.py` for testing locally separate tasks for each eligibility item.