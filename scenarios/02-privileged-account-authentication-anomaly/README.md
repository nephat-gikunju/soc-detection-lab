# SC-002: Privileged-Account Authentication Anomaly

## Scenario

Five failed sign-in attempts target a synthetic platform administrator account.
Three minutes later, the account signs in successfully from a different
external test address. This is an investigation signal, not proof of
compromise.

## Run

~~~text
make lab-2
~~~

## Expected result

The detector raises SOC-002 at critical severity because a privileged
identity receives repeated failures followed by success from a new source.

## Analyst outcome

Follow PB-002 to verify the identity-provider history, MFA result, device
context, change records, emergency-access approval, and subsequent activity.
Coordinate with business operations before disabling an account that could be
needed for critical business service.

All identities, session references, and addresses are synthetic.
