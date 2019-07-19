This directory contains PHP and TwiML code for presenting the math stressor (serialsevens) and the verbal fluency (vftask) tasks
over the telphone. The entry points (PHP scripts that need to be pointed to from Twilio) are ss_entrypoint.php for the Serial Sevens 
task and vfmeter_fitbit.php for the Verbal Fluency task. The code in this folder need to be accessible via an HTTP service.

- `serialsevens/` - scripts and materials for the Serial Sevens subtraction task
- `vftak/` - scripts for administering verba fluency task
- `twilio-php` - PHP support - needs to be updated with the newest from Twilio
