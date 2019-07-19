# Virtual Study Coordinator
This is a repository of code to support studies that involve wearable sensors conducted repotely (without on-site visits by participants).
The repository contains a number of scripts and supporting files needed for a study in which 
participants are recruited for a 7-day observational period during which they ware a Fitbit
capable of monitoring heart rate and respond to Ecologic Momemntary Assessment (EMA) surveys 
(every two hours) sent to them via Twilio text messaging and
respond to cognitive tasks over the telephone using Twilio interactive voice response system.

Note: Each study participant needs to be issued unique Twilio numbers for performing cognitive tasks. 
This part of the project is not yet automated. 
Twilio numbers can be generated using the Twilio web interface or Twilio API. In our pilot implementation,
we used Twilio web service to set up a single number that we used to text participants with EMA reminders
to take the survey. We also set up two separate numbers for each participoant - one for each 
cognitive task (math and verbal fluency) used in the study. More numbers would need to be set up for more
tasks (or recycled using Twilio API).

- `analysis/` - scripts for interacting with the redcap API and for synthesizing results from fitbit JSON and redcap tables
- `coordinator/` - scripts/web interfaces for scheduling EMAs and collecting fitbit data
- `redcap/' - data dictionaries used to set up participant data including consent and EMA surveys
- `twilio/' - Twilio Markup Language scripts for administering the math and verbal fluency tasks
