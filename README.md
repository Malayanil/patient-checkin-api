# patient-checkin-api

A simple environment segregated FastAPI to create, update, view and delete patients who are checking into and out of a clinic. The API is the functional backend of a pre-determined UI who is set to handle all the tasks. <br><br>

The API has extensive logging and exception handling to debug and fix issues. It is also set with an authorization mechanism to only allow known users/apps to interact with itself. <br><br>

Files:<br>
<ul>
  <li>main.py -> FastAPI server script.</li>
  <li>api_calls.py -> Sample API call script.</li>
  <li>dependencies/auth.py -> Authorization configuration script.</li>
  <li>requirements.txt -> Requirements file to run the API properly.</li>
  <li>logs -> Logging directory.</li>
  <li>user_data -> JSON dump directory for users being created in the runtime.</li>
</ul>

<br>
How to host API:<br>
<ul>
  <li>Clone the repository.</li>
  <li>Install the requirements.txt file</li>
  <li>Move to the root directory in the terminal and execute this: python3 -m uvicorn main:app --host 0.0.0.0 --port 8000</li>
  This will run the API on 8000 port, it can be customized as required. If it's on development phase, --reload would help to instantly reload any changes, NOT RECOMMENDED FOR PRODUCTION USE. 
  <li>Logs will be available as per API calls and executions.</li>
  <li>Once the customizations are in place and it works as per requirement, host it on a TMUX session or any other preferable method.</li>
</ul>
